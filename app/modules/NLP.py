import pandas as pd
import regex as re
import requests
import spacy
import textstat
from bs4 import BeautifulSoup
from spacytextblob.spacytextblob import SpacyTextBlob
import trafilatura



def cleanup_text(text):
    """_summary_

    Args:
        text (_type_): _description_

    Returns:
        _type_: _description_
    """

    text = text.replace("\xc2\xa0", "") # Deal with some weird tokens
    text = re.sub(r'\d+', '', text) # remove numbers
    text = re.sub(r'\s+', ' ', text)  # remove whitespaces
    text = re.sub(r'[^\w\s]', '', text) # remove special characters
    text = text.lower() # convert text to lowercase
    text=  text.strip() # remove leading and trailing whitespaces
    text = text.encode('ascii', 'ignore').decode('ascii') # remove non-ascii characters
    text=text.split()
    return text

def clean_up_web_page(text):
    remove_words=['click', 'watch', 'advertisement', 'join', 'subscribe', 'register', 'login']
    # delete the words from the remove_Words list from the text string
    for word in text:
        if word in remove_words:
            text.remove(word)
    return text
         
    

# TODO - allow to pass an internet article url here and show percentage of offensive words in the article
def censor_bad_words_strict(text):
    """_summary_

    Args:
        text (_type_): _description_
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
def censor_bad_words_not_strict(text):
    """_summary_

    Args:
        text (_type_): _description_

    Returns:
        _type_: _description_
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



def readability_index(text):
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
def extract_difficult_words(text):
    """_summary_

    Args:
        text (_type_): _description_
    """
    with open(file='_most_common_words.txt', mode='r') as f:
        simple_words = f.read().splitlines()
    text=cleanup_text(text)

    difficult_words = [word for word in text if word not in simple_words]
    print(difficult_words)        

def check_url_or_text(value)->bool:
    try:
        response = requests.get(value)
    except requests.exceptions.MissingSchema:
        return False
    except requests.exceptions.InvalidSchema:
        return False
    return True


def parse_text_from_web(webURL):
    downloaded = trafilatura.fetch_url(webURL)
    return trafilatura.extract(downloaded)


def sentiment_analysis(content):
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
    
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')

    # print(text)
    doc = nlp(text)
    sentiment = round(doc._.blob.polarity,2)
    sent_label = "Positive" if sentiment > 0 else "Negative"
    url_sent_label = [sent_label]
    url_sent_score = [sentiment]
    positive_words = []
    negative_words = []

    for x in doc._.blob.sentiment_assessments.assessments:
        if x[1] > 0:
            positive_words.append(x[0][0])
        elif x[1] < 0:
            negative_words.append(x[0][0])

    total_pos = [', '.join(set(positive_words))]
    total_neg = [', '.join(set(negative_words))]
    print(f"Sentiment Score: {url_sent_score}")
    print(f"Outcome: {url_sent_label}")
    print(f"+ve Words: {total_pos}")
    print(f"-Ve Words: {total_neg}")


# essay="""
# Todd awoke to singing. The singing was light and airy. It reminded him of a sunrise. Well that’s appropriate, thought Todd, it’s so early the sun is probably just rising. As his mind grew more awake, Todd realized that he didn’t know where the music was coming from. He checked his radio, as well as his phone. Nothing.He stretched and looked around his room. Nothing in here would be singing, he thought. Todd got out of bed and walked toward his window, thinking that maybe one of his neighbors was playing music.
# """