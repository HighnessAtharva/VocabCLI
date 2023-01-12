from collections import Counter
from heapq import nlargest
from string import punctuation
import nltk
import pandas as pd
import regex as re
import requests
import rich
import spacy
import textstat
import torch
import trafilatura
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from spacy.lang.en.stop_words import STOP_WORDS
from spacytextblob.spacytextblob import SpacyTextBlob
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from rich.panel import Panel
from rich.table import Table
from rich import print, box
from rich.columns import Columns
from typing import *

from rich.progress import Progress, SpinnerColumn, TextColumn
 

# TODO: @atharva - add proper response headers and browser details to prevent false IP blocks.
# TODO: - revise docstrings and add wherever missing. @anay


def check_url_or_text(value: str) -> bool:
    """Checks if the value is a URL or a text

    Args:
        value (str): URL or text to be checked

    Returns:
        bool: True if the value is a URL, False if the value is a text
    """

    try:
        response = requests.get(value)
    except requests.exceptions.MissingSchema:
        return False
    except requests.exceptions.InvalidSchema:
        return False
    except requests.exceptions.InvalidURL:
        return False
    return True


def parse_text_from_web(webURL: str) -> str:
    """Extracts the text from the main content of the web page. Removes the ads, comments, navigation bar, footer, html tags, etc

    Args:
        webURL (str): URL of the web page

    Returns:
        str: clean text from the web page
    """

    downloaded = trafilatura.fetch_url(webURL)
    return trafilatura.extract(downloaded, include_comments=False, include_tables=False, with_metadata=False, include_formatting=True, target_language='en', include_images= False)


def cleanup_text(text: str) -> str:
    """Clean up the text by removing special characters, numbers, whitespaces, etc for further processing and to improve the accuracy of the model.

    Args:
        text (str): text to be cleaned up

    Returns:
        str: cleaned up text
    """

    text = re.sub("\xc2\xa0", "", text)  # Deal with some weird tokens
    text = re.sub(r'\d+', '', text)  # remove numbers
    text = re.sub(r'\s+', ' ', text)  # remove whitespaces
    # remove special characters except full stop and apostrophe
    text = re.sub(r'[^a-zA-Z0-9\s.]', '', text)
    # text = text.lower()  # convert text to lowercase
    text = text.strip()  # remove leading and trailing whitespaces
    text = text.encode('ascii', 'ignore').decode(
        'ascii')  # remove non-ascii characters
    
    # split text into words without messing up the punctuation
    text = re.findall(r"[\w']+|[.,!?;]", text)
    
    return text
    
    


# TODO: - show total count of censor words in the text for both strict and not strict
def censor_bad_words_strict(text: str) -> None:
    """Removes the bad words from the text and replaces them with asterisks completely and prints the censor text

    Args:
        text (str): text that needs to be censored
    """
    #----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="monkey", style="bold violet"),
        TextColumn("[progress.description]{task.description}", justify="left", style="bold cyan"),
        transient=True,
    ) as progress:
        progress.add_task(description="Censoring...", total=None)
    #----------------- Spinner -----------------#
    
    
        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(text):
            print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="URL detected 🌐")
                )
            text = parse_text_from_web(text)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="This is not a valid URL. Processing it as text... 📃")
                )
            
        text = cleanup_text(text)
        new_text = ''   
        offensive_words=0 

        with open('modules/_bad_words.txt', mode='r', encoding='utf-8') as f:
            bad_words = f.read().splitlines()
            bad_words_plural = [bad_words[i]+'s' for i in range(len(bad_words))]
            bad_words = bad_words + bad_words_plural
        
        for word in text:
            if word.lower() in bad_words:
                offensive_words+=1
                word = word.replace(word, '*' * len(word))
            new_text += f'{word} '
        new_text = new_text.replace(' .', '.')
        print(Panel(renderable=new_text,
                    padding=(2, 2), 
                    title="[reverse]Censored Text[/reverse]", 
                    border_style="bold violet",
                    box= box.DOUBLE_EDGE
            ))
          
        print(Panel(
            renderable=f"Offensive words censored:[bold red] {offensive_words} 😤[/bold red]",
            title="[reverse]Censored Words[/reverse]",
            
        ))


# TODO: - allow to pass an internet article url here and show percentage of offensive words in the article
def censor_bad_words_not_strict(text: str) -> None:
    """Removes the bad words from the text and replaces them with asterisks partially and prints the censor text

    Args:
        text (str): text that needs to be censored
    """
      #----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="monkey", style="bold violet"),
        TextColumn("[progress.description]{task.description}", justify="left", style="bold cyan"),
        transient=True,
    ) as progress:
        progress.add_task(description="Censoring...", total=None)
    #----------------- Spinner -----------------#
    
        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(text):
            print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="URL detected 🌐")
                )
            text = parse_text_from_web(text)
            

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="This is not a valid URL. Processing it as text... 📃")
                )
    

        with open('modules/_bad_words.txt', mode='r', encoding='utf-8') as f:
            bad_words = f.read().splitlines()
            bad_words_plural = [bad_words[i]+'s' for i in range(len(bad_words))]
            bad_words = bad_words + bad_words_plural
        
        
        text = cleanup_text(text)
        new_text = ''
        offensive_words = 0
        
        for word in text:
            word = str(word)
            if word.lower() in bad_words:
                offensive_words += 1
                if len(word) <= 3:
                    word = word.replace(word, '*' * len(word))
                elif len(word) <= 5:
                    # replace the middle character with asterisk
                    word = word.replace(word[1], '*')
                    word = word.replace(word[2], '*')
                    word = word.replace(word[3], '*')
                else:
                    word = word.replace(word[2:5], '***')
            new_text += f'{word} '
        new_text = new_text.replace(' .', '.')
        print(Panel(renderable=new_text,
                    padding=(2, 2), 
                    title="[reverse]Censored Text[/reverse]",
                    border_style="bold violet",
                    box= box.DOUBLE_EDGE
                    ))  
        print(Panel(renderable=f"Offensive words censored:[bold red] {offensive_words} 😤[/bold red] ",padding=(1, 1), title="[reverse]Censored Words[/reverse]"))


def readability_index(text: str) -> None:
    """Prints the readability index of the text and the summary of the index 

    Args:
        text (str): text to be analyzed
    """
       #----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold green"),
        TextColumn("[progress.description]{task.description}", justify="left", style="bold cyan"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing Text...", total=None)
    #----------------- Spinner -----------------#
    
        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(text):
            print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="URL detected 🌐")
                )
            text = parse_text_from_web(text)
            

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="This is not a valid URL. Processing it as text... 📃")
                )
    
        #@atharva check this

        readability_index = textstat.flesch_reading_ease(text)

        if readability_index > 90:
            index_desc = "Very Easy"
        elif readability_index > 80:
            index_desc = "Easy"
        elif readability_index > 70:
            index_desc = "Fairly Easy"
        elif readability_index > 60:
            index_desc = "Standard"
        elif readability_index > 50:
            index_desc = "Fairly Difficult"
        elif readability_index > 30:
            index_desc = "Difficult"
        else:
            index_desc = "Very Confusing"

        print(Panel(
            title="[b reverse]Readability Index[/b reverse]", 
            title_align="center", 
            padding=(2, 2), 
            border_style="bold magenta1",
            box= box.DOUBLE,
            renderable=f"[b r blue]Lexicon Count[/b r blue]: {textstat.lexicon_count(text, removepunct=True)}\n\n[b r green]Character Count[/b r green]: {textstat.char_count(text)}\n\n[b r yellow2]Sentence Count[/b r yellow2]: {textstat.sentence_count(text)}\n\n[b r gold1]Words Per Sentence[/b r gold1]: {textstat.avg_sentence_length(text)}\n\n[b r white]Readability Index[/b r white]: {textstat.flesch_reading_ease(text)}")
            )


def extract_difficult_words(text: str) -> None:
    """Extracts the difficult words from the text and prints them, uses the _most_common_words.txt file to determine the difficult words

    Args:
        text (str): text/url to be analyzed
    """
      #----------------- Spinner -----------------#
    with Progress(
        SpinnerColumn(spinner_name="aesthetic", style="bold gold1"),
        TextColumn("[progress.description]{task.description}", justify="left", style="bold white"),
        transient=True,
    ) as progress:
        progress.add_task(description="Extracting Tough Words...", total=None)
    #----------------- Spinner -----------------#
    
        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(text):
            print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="URL detected 🌐")
                )
            text = parse_text_from_web(text)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="This is not a valid URL. Processing it as text... 📃")
                )
            text = cleanup_text(text)
            text = ' '.join(text)

        with open(file='modules/_most_common_words.txt', mode='r', encoding='utf-8') as f:
            simple_words = f.read().splitlines()
        text = cleanup_text(text)
        article_word_count = len(text)

        # remove full stop from the words
        text = [word for word in text if '.' not in word]
        difficult_words = [word for word in text if word.lower() not in simple_words]
        filter_words = ['didnt', 'couldnt', 'wouldnt', 'shouldnt', 'isnt',
                        'wasnt', 'arent', 'werent', 'dont', 'doesnt', 'didnt', 'hasnt', 'hadnt']
        difficult_words = [
            word for word in difficult_words if word not in filter_words]
        # filter out duplicate words
        difficult_words = list(set(difficult_words))

        # remove plurals of the same word
        for word in difficult_words:
            if word[-1] == 's' and word[:-1] in difficult_words:
                difficult_words.remove(word)

        # remove plurals of which singular is in the simple words list
        for word in difficult_words:
            if word[-1] == 's' and word[:-1] in simple_words:
                difficult_words.remove(word)

        # TODO: Function has scope for imporvement (low value but high effort):
        # 1. Elminiate proper nouns -> Remove words that start with a capital letter but are not in the simple words list and not preceeded by a full stop. Because first word of a sentence is always capitalized.
        # 2. Remove gerunds (ing), past participles (ed) of the words that are in the simple words list. Those are not difficult words. (eg. "I am reading" -> "factories" is not detected as a difficult word but "factory" is.)

        difficult_words.sort()
        print(Panel(title="[b reverse navajo_white1]  Success!  [/b reverse navajo_white1]",
                    title_align="center",
                    padding=(1, 1),
                    border_style="navajo_white1",
                    box= box.DOUBLE,
                    renderable=f"Content Length: [bold blue]{article_word_count}[/bold blue] words\nExtracted [bold blue]{len(difficult_words)}[/bold blue] difficult words"),       
            )

        difficult_words = [
            Panel(f"[thistle1]{word}[thistle1]", expand=True, box=box.ROUNDED, border_style="pale_violet_red1")
            for word in difficult_words
        ]
        print(Columns(difficult_words, equal=True, expand=True))


def sentiment_score_to_summary(sentiment_score: int) -> str:
        """
        Converts the sentiment score to a summary

        Args:
            sentiment_score (int): sentiment score

        Returns:
            str: summary of the sentiment score
        """

        if sentiment_score == 1:
            return "Extremely Negative"
        elif sentiment_score == 2:
            return "Somewhat Negative"
        elif sentiment_score == 3:
            return "Generally Neutral"
        elif sentiment_score == 4:
            return "Somewhat Positive"
        elif sentiment_score == 5:
            return "Extremely Positive"
            
            
            
def sentiment_analysis(content: str) -> None:
    """
    Performs sentiment analysis on the text and prints the sentiment score and the summary of the score

    Args:
        content (str): text/url to be analyzed
    """
          #----------------- Spinner -----------------#
    with Progress(
            SpinnerColumn(spinner_name="smiley", style="bold green"),
            TextColumn("[progress.description]{task.description}", justify="left", style="bold white"),
            transient=True,
        ) as progress:
        progress.add_task(description="Getting Sentiment...", total=None)
    #----------------- Spinner -----------------#

        # check if the content is a URL, if yes, then parse the text from it and then use the model
        if isWebURL := check_url_or_text(content):
            print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="URL detected 🌐")
                )
            text = parse_text_from_web(content)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="This is not a valid URL. Processing it as text... 📃")
                )
            text = cleanup_text(content)
            text = ' '.join(text)

     

        tokenizer = AutoTokenizer.from_pretrained(
            "nlptown/bert-base-multilingual-uncased-sentiment")
        model = AutoModelForSequenceClassification.from_pretrained(
            "nlptown/bert-base-multilingual-uncased-sentiment")
        tokens = tokenizer.encode(
            text, return_tensors='pt', truncation=True, padding=True)
        result = model(tokens)
        result.logits
        sentiment_score = int(torch.argmax(result.logits))+1
        outcome = sentiment_score_to_summary(sentiment_score)
        if outcome in ["Extremely Negative", "Somewhat Negative"]:
            emoji = "😞"
        
        elif outcome == "Generally Neutral":
            emoji = "😐"
            
        elif outcome in ["Somewhat Positive", "Extremely Positive"]:
            emoji = "😀"
        
        print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable=f"Sentiment Analysis Verdict: {sentiment_score_to_summary(sentiment_score)} {emoji}") 
                )
       


def summarize_text_util(text:str, per:int)->str:
    """
    Summarizes the text using the spacy library

    Args:
        text (str): text to be summarized
        per (int): percentage of the text to be summarized

    Returns:
        str: summarized text
    """
   
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    word_frequencies = {}
    for word in doc:
        if (
            word.text.lower() not in list(STOP_WORDS)
            and word.text.lower() not in punctuation
        ):
            if word.text in word_frequencies:
                word_frequencies[word.text] += 1
            else:
                word_frequencies[word.text] = 1

    max_frequency = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] = word_frequencies[word]/max_frequency
    sentence_tokens = list(doc.sents)
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies:
                if sent in sentence_scores:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
    select_length = int(len(sentence_tokens)*per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    return summary


def summarize_text(content: str, file: Optional[bool] = False) -> None:
    """Print the summarized text or internet article. 

    Args:
        text (str): Text that is to be summarized
    """

     #----------------- Spinner -----------------#
    with Progress(
            SpinnerColumn(spinner_name="dots12", style="bold blue"),
            TextColumn("[progress.description]{task.description}", justify="left", style="bold white"),
            transient=True,
        ) as progress:
        progress.add_task(description="Summarizing...", total=None)
    #----------------- Spinner -----------------#
    
        if isWebURL := check_url_or_text(content):
            print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="URL detected 🌐")
                )

            # this is just get the headings
            r = requests.get(content)
            soup = BeautifulSoup(r.content, "html.parser")
            headline = soup.find('h1').get_text()

            # this gets the body of the article.
            text = parse_text_from_web(content)

        # if text and not URL, then directly use the model
        if not isWebURL:
            print(Panel(title="[b reverse yellow]  Warning!  [/b reverse yellow]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="This is not a valid URL. Processing it as text... 📃")
                )
            text = cleanup_text(content)
            text = ' '.join(text)

        text_summary = summarize_text_util(text, 0.2)

        if not file: #@atharva check this
            if isWebURL:
                print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable=f"Length of the article: {len(text)} characters  \n\n Length of the summary:{len(text_summary)} characters \n\nHeadline:\n{headline} \n\n Summary:\n{text_summary}"
                ))
            else:
                print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable=f"Length of the article: {len(text)} characters  \n\n Length of the summary:{len(text_summary)} characters \n\n Summary:\n{text_summary}"
                ))

        if file:  
            # writing to a .txt file
            with open("summary.txt", "w", encoding="utf-8") as f:
                f.write(f"Length of the article: {len(text)} characters\n\n")
                f.write(f"Length of the summary:{len(text_summary)} characters\n\n")
                if isWebURL:
                    f.write(str(f"Headline:\n{headline}\n\n"))
                f.write("------------------------------------------------------------\n\n")
                f.write(f"Summary:\n{text_summary}\n\n")

            print(Panel(title="[b reverse green]  Success!  [/b reverse green]",
                        title_align="center",
                        padding=(1, 1),
                        renderable="[bold green]Summary saved[/bold green] to [bold]summary.txt[/bold]")
              )
        #TODO: writing to a .md file
       