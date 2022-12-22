import pandas as pd
import regex as re
import requests
import spacy
import textstat
from bs4 import BeautifulSoup
from spacytextblob.spacytextblob import SpacyTextBlob
import trafilatura
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import nltk
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
from string import punctuation
from heapq import nlargest
import rich 
from rich.console import Console
from rich.table import Table


def check_url_or_text(value:str)->bool:
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

def clean_up_web_page(text:str)->str:
    """Clean up the text by removing certain ad words

    Args:
        text (str): text to be cleaned up

    Returns:
        str: cleaned up text
    """

    remove_words=['click', 'watch', 'advertisement', 'join', 'subscribe', 'register', 'login']
    # delete the words from the remove_Words list from the text string
    for word in text:
        if word in remove_words:
            text.remove(word)
    return text
         

def parse_text_from_web(webURL):
    """Extracts the text from the main content of the web page. Removes the ads, comments, navigation bar, footer, html tags, etc

    Args:
        webURL (str): URL of the web page

    Returns:
        str: clean text from the web page
    """

    downloaded = trafilatura.fetch_url(webURL)
    return trafilatura.extract(downloaded)


def cleanup_text(text:str)->str:
    """Clean up the text by removing special characters, numbers, whitespaces, etc for further processing and to improve the accuracy of the model.

    Args:
        text (str): text to be cleaned up

    Returns:
        str: cleaned up text
    """

    text = text.replace("\xc2\xa0", "") # Deal with some weird tokens
    text = re.sub(r'\d+', '', text) # remove numbers
    text = re.sub(r'\s+', ' ', text)  # remove whitespaces
    text = re.sub(r'[^a-zA-Z0-9\s.]', '', text)  # remove special characters except full stop and apostrophe
    text = text.lower() # convert text to lowercase
    text=  text.strip() # remove leading and trailing whitespaces
    text = text.encode('ascii', 'ignore').decode('ascii') # remove non-ascii characters
    text=text.split()
    return text


    

# TODO - allow to pass an internet article url here and show percentage of offensive words in the article
def censor_bad_words_strict(text:str)->None:
    """Removes the bad words from the text and replaces them with asterisks completely and prints the censor text

    Args:
        text (str): text that needs to be censored
    """

    with open('_bad_words.txt', mode='r') as f:
        bad_words = f.read().splitlines()
    text=cleanup_text(text)
    new_text=''
    for word in text:
        if word in bad_words:
            word=word.replace(word, '*' * len(word))
        new_text += f'{word} '
    print(new_text)


# TODO - allow to pass an internet article url here and show percentage of offensive words in the article
def censor_bad_words_not_strict(text:str)->None:
    """Removes the bad words from the text and replaces them with asterisks partially and prints the censor text

    Args:
        text (str): text that needs to be censored
    """

    with open('_bad_words.txt', mode='r') as f:
        bad_words = f.read().splitlines()
    
    text=cleanup_text(text)
    new_text=''
    
    for word in text:
        if word in bad_words:
            if len(word) <= 3:
                word=word.replace(word, '*' * len(word))
            elif len(word) <= 5:
                word=word.replace(word[1:], '****')
            else:
                word=word.replace(word[2:], '*'*len(word)-1)
        new_text+= f'{word} '
    print(new_text)



def readability_index(text:str)->None:
    """Prints the readability index of the text and the summary of the index 

    Args:
        text (str): text to be analyzed
    """

    print(f"Lexicon Count {textstat.lexicon_count(text, removepunct=True)}")
    print(f"Character Count {textstat.char_count(text)}")
    print(f"Sentences Count {textstat.sentence_count(text)}")
    print(f"Words Per Sentence {textstat.avg_sentence_length(text)}")
    
    readability_index=textstat.flesch_reading_ease(text)
    
    if readability_index > 90:
        index_desc="Very Easy"
    elif readability_index > 80:
        index_desc="Easy"
    elif readability_index > 70:
        index_desc="Fairly Easy"
    elif readability_index > 60:
        index_desc="Standard"
    elif readability_index > 50:
        index_desc="Fairly Difficult"
    elif readability_index > 30:
        index_desc="Difficult"
    else:
        index_desc="Very Confusing"
    
    print(f"Readability Index {textstat.flesch_reading_ease(text)}\nSummary: The text is {index_desc} to read")
    



# TODO - allow to pass an internet article url here and show percentage of difficult words in the article 
def extract_difficult_words(text:str) -> None:
    """Extracts the difficult words from the text and prints them, uses the _most_common_words.txt file to determine the difficult words

    Args:
        text (str): text/url to be analyzed
    """

    # check if the content is a URL, if yes, then parse the text from it and then use the model
    if isWebURL:=check_url_or_text(text):
        print("URL detected")
        text=parse_text_from_web(text)
        text=clean_up_web_page(text)    

    # if text and not URL, then directly use the model
    if not isWebURL:
        print("This is not a valid URL. Processing it as text...")
        text=cleanup_text(text)
        text=' '.join(text)


    with open(file='_most_common_words.txt', mode='r') as f:
        simple_words = f.read().splitlines()
    text=cleanup_text(text)
    article_word_count=len(text)
    
    # remove full stop from the words
    text=[word for word in text if '.' not in word]
    difficult_words = [word for word in text if word not in simple_words]
    filter_words=['didnt', 'couldnt', 'wouldnt', 'shouldnt', 'isnt', 'wasnt', 'arent', 'werent', 'dont', 'doesnt', 'didnt', 'hasnt', 'hadnt']
    difficult_words=[word for word in difficult_words if word not in filter_words]
    # filter out duplicate words
    difficult_words=list(set(difficult_words))

    # remove plurals of the same word
    for word in difficult_words:
        if word[-1] == 's' and word[:-1] in difficult_words:
            difficult_words.remove(word)
    
    # remove plurals of which singular is in the simple words list
    for word in difficult_words:
        if word[-1] == 's' and word[:-1] in simple_words:
            difficult_words.remove(word)
            
    difficult_words.sort()
    print(f"Content Length: {article_word_count} words")        
    print(f"Extracted {len(difficult_words)} difficult words")
    for word in difficult_words:
        print(word)        


extract_difficult_words("https://www.wikiwand.com/en/Wolfgang_Amadeus_Mozart")


def sentiment_analysis(content):
    """
    Performs sentiment analysis on the text and prints the sentiment score and the summary of the score

    Args:
        content (str): text/url to be analyzed
    """

    # check if the content is a URL, if yes, then parse the text from it and then use the model
    if isWebURL:=check_url_or_text(content):
        print("URL detected")
        text=parse_text_from_web(content)
        text=clean_up_web_page(text)    
        
    # if text and not URL, then directly use the model
    if not isWebURL:
        print("This is not a valid URL. Processing it as text...")
        text=cleanup_text(content)
        text=' '.join(text)
    
    def remove_long_sentences(text):
        """
        Removes sentences with more than 512 characters from the text

        Args:
            text (str): text to be cleaned

        Returns:
            str: cleaned text
        """

        # remove sentences with more than 512 characters
        sentences = text.split('.')
        new_text = ''
        for sentence in sentences:
            if len(sentence) <= 500:
                new_text += sentence + '.'
        return new_text
    
    def sentiment_score_to_summary(sentiment_score):
        """
        Converts the sentiment score to a summary

        Args:
            sentiment_score (int): sentiment score

        Returns:
            str: summary of the sentiment score
        """

        if sentiment_score==1:
            return "Extremely Negative"
        elif sentiment_score==2:
            return "Somewhat Negative"
        elif sentiment_score==3:
            return "Generally Neutral"
        elif sentiment_score==4:
            return "Somewhat Positive"
        elif sentiment_score==5:
            return "Extremely Positive"
    
    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    tokens = tokenizer.encode(text, return_tensors='pt', truncation=True, padding=True)
    result = model(tokens)
    result.logits 
    sentiment_score=int(torch.argmax(result.logits))+1
    outcome=sentiment_score_to_summary(sentiment_score)
    print(f"Sentiment Analysis Verdict: {sentiment_score_to_summary(sentiment_score)}")
    


def summarize_text_util(text, per):
    """
    Summarizes the text using the spacy library

    Args:
        text (str): text to be summarized
        per (int): percentage of the text to be summarized

    Returns:
        str: summarized text
    """

    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if (
            word.text.lower() not in list(STOP_WORDS)
            and word.text.lower() not in punctuation
        ):
            if word.text in word_frequencies:
                word_frequencies[word.text] += 1
            else:
                word_frequencies[word.text] = 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens = list(doc.sents)
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies:
                if sent in sentence_scores:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary

def summarize_text(content:str)->None:
    """
    Print the summariezed text or internet article. 

    Args:
        text (str): Text that is to be summarized
    """
    
    if isWebURL:=check_url_or_text(content):
        print("URL detected")
        
        # this is just get the headings
        r = requests.get(content)
        soup = BeautifulSoup(r.content, "html.parser")
        headline = soup.find('h1').get_text()
        
        
        # this gets the body of the article.
        text=parse_text_from_web(content)
        text=clean_up_web_page(text)
        
        
    # if text and not URL, then directly use the model
    if not isWebURL:
        print("This is not a valid URL. Processing it as text...")
        text=cleanup_text(content)
        text=' '.join(text)
        
    # print(text)
    text_summary = summarize_text_util(text, 0.4)  
    
    
    print(f"Length of the article: {len(text)} characters", end="\n\n")
    print(f"Length of the summary:{len(text_summary)} characters", end="\n\n")
    
    if isWebURL:
        print(f"Headline:\n{headline}", end="\n\n")
    
    print(f"Summary:\n{text_summary}", end="\n\n")
        
        