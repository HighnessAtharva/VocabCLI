# VocabularyBuilder CLI

## Project Description

> VocabularyCLI is a lightweight Command Line Interface that allows users to look up word definitions, examples, synonyms and antonyms directly via the command line. Powered with several utility based commands our CLI offers rapid and robust Knowledge Base capabilities like Flashcards, Tagging, Word Management, Graph Reporting, Bulk import and export of word lists and is a definitive software for linguaphiles.
>
> This application boasts a simple and intuitive interface that is easy to use and is a must have for anyone who wants to expand their vocabulary and improve their language skills. The app also offers advanced Text Classification and Processing via the use of Natural Language Processing and Machine Learning algorithms which will be discussed in detail in the "Scope and Features" section.
>
> The CLI will be offered with eye-catching Panels, Tables, Animated Symbols, Emojis, Interactive Menus, Spinners, Colored fonts and other rich features that will make the user experience more enjoyable and interactive. The CLI will also be offered with a comprehensive User Manual and a detailed Documentation that will help users get started with the CLI and use it to its full potential.
>
<hr>

## Technology and Libraries Involved

- **Primary Development Language**: Python 3.10
- **Database Management System**: SQLite3
- **API**: DictionaryAPI <https://api.dictionaryapi.dev/api/v2/entries/en/hello>
- **Deployment**: PyPi (Python Package Index)
- **Libraries**: Rich, Typer, Matplotlib, Seaborn, NLTK, SpaCy, Pandas, Numpy, Requests, Beautiful Soup, PyDictionary
- **Testing**: PyTest (Unit Testing), PyTest-Cov (Code Coverage), PyTest-Benchmark (Benchmarking)
- **Documentation**: Sphinx, ReadTheDocs

## Running the Project 🕹

**While setting up the project for the first time** :arrow_right:

- Make a Virtual environment: `python3 -m venv my_env`
- Activate the virtual environment: `my_env\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- To freeze the requirements: `pip freeze > requirements.txt`

**While developing** :arrow_right:

- Move to source folder: `cd src/VocabularyBuilder`
- Run the main project file: `python VocabularyBuilder.py`

**To Run Test Cases** :arrow_right:

- Write test cases in /tests folder
- Then go to src/VocbularyBuilder
- RUN `python -m pytest ../tests` to run all tests
- RUN `python -m pytest -k "ClassName" ../tests` to run a specific class or function test

<hr>

## Generating Documentation 📚

```powershell
cd docs
make html
```


## Generating PyTest Coverage Report 📊

```powershell
PythonCLI\app> coverage run -m pytest ..\tests
PythonCLI\app> coverage html
```
<hr>

## Features 🎯

- Look up word definitions, examples, homonyms, synonyms and antonyms
- Generate flashcards for words
- Tag words, set words as favorites, set words as learning, set words as mastered
- Generate Graph Reports
- Import and Export word lists in PDF and CSV formats
- Show word lookup history and word lookup statistics
- Perform Text Classification and Processing and Summarize Web Articles
- Delete words from the database and clear attributes associated with the words
- Revise words and ready-made word collections
- Quiz Mode
- TTS (Text to Speech) Mode and Accessibility Mode
- Paraphrase Text and Generate Word Clouds
- Detect Plagiarism and Generate Similarity Scores
- Determine Readability Index and Filter out offensive words
- Generate Word Frequency Distributions
- Save User Quotes and Provide Quotes of the Day
- Determine Word Sentiment and Generate Sentiment Analysis Reports
- More to follow...


![snap4](C:\Users\AtharvaShah\Downloads\snap4.png)
![snap3](C:\Users\AtharvaShah\Downloads\snap3.png)
![snap2](C:\Users\AtharvaShah\Downloads\snap2.png)
![snap1](C:\Users\AtharvaShah\Downloads\snap1.png)
![snap5](C:\Users\AtharvaShah\Downloads\snap5.png)
