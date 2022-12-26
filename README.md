
## About VocabCLI 📚

![image](https://user-images.githubusercontent.com/68660002/207532026-a82ce199-51b8-4d11-8efd-01e37ec5564f.png)

VocabularyCLI is a lightweight Command Line Interface that allows users to look up word definitions, examples, synonyms and antonyms directly via the command line. Powered with several utility based commands our CLI offers rapid and robust Knowledge Base capabilities like Flashcards, Tagging, Word Management, Graph Reporting, Bulk import and export of word lists and is a definitive software for linguaphiles.

This application boasts a simple and intuitive interface that is easy to use and is a must have for anyone who wants to expand their vocabulary and improve their language skills. The app also offers advanced Text Classification and Processing via the use of Natural Language Processing and Machine Learning algorithms which will be discussed in detail in the "Scope and Features" section.

The CLI will be offered with eye-catching Panels, Tables, Animated Symbols, Emojis, Interactive Menus, Spinners, Colored fonts and other rich features that will make the user experience more enjoyable and interactive. The CLI will also be offered with a comprehensive User Manual and a detailed Documentation that will help users get started with the CLI and use it to its full potential.

---

## Installation 📥

Official package release coming soon. Stay tuned! 🚧
<!-- ```powershell

# Install the package from PyPi
pip3 install vocabcli

# Upgrade the package
pip3 install --upgrade vocabcli

# Uninstallation
pip3 uninstall vocabcli
``` -->

---

## [Demo and Examples](https://vocabcli.github.io/demo) 💡

---

## Developed Using 🛠

- **Primary Development Language**: Python 3.10
- **Database Management System**: SQLite3
- **API**: DictionaryAPI (<https://api.dictionaryapi.dev/api/v2/entries/en/hello>)
- **Deployment**: PyPi (Python Package Index)
- **Libraries**: Rich, Typer, Matplotlib, Seaborn, NLTK, SpaCy, Pandas, Numpy, Requests, Beautiful Soup, PyDictionary
- **Testing**: PyTest (Unit Testing), PyTest-Cov (Code Coverage), PyTest-Benchmark (Benchmarking)
- **Documentation**: Sphinx, ReadTheDocs

---

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

---

## Screenshots 📸

![snap1](https://user-images.githubusercontent.com/68660002/205949431-a10bfb73-05a3-484c-9821-061ee3eddfa0.png)
---

![snap2](https://user-images.githubusercontent.com/68660002/205949434-d3f3c567-a5ed-4c9c-a3a3-17aaefc22c50.png)
---

![snap3](https://user-images.githubusercontent.com/68660002/205949437-23b90fd1-6023-4eb3-ba3f-dff735bb00ee.png)
---

![snap4](https://user-images.githubusercontent.com/68660002/205949444-25b5ab53-f000-42dd-aac5-99c8013c8d76.png)
---

![snap5](https://user-images.githubusercontent.com/68660002/207532081-e088f7d5-f7ef-44fc-9152-c5b72283cb55.png)
---

---

## Getting Started 🚀

### For Development 👇🏻

```powershell
# Make a Virtual environment
python3 -m venv my_env

# Activate the virtual environment
my_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Freeze the requirements
pip freeze > requirements.txt
```

### Running the Application 👇🏻

```powershell
# Move to source folder
cd app

# Run the main project file
python -m VocabularyCLI --help
```

### Run Tests 👇🏻

```powershell
# Move to source folder
cd app

# Run all tests
python -m pytest ../tests

# Run specific tests
python -m pytest -k "ClassName" ../tests 
```

---

### Generating Documentation 📚

```powershell
# run the following command in the root directory to update the docs
sphinx-apidoc -o docs

# move to docs folder
cd docs

# Edit the conf.py file to index modules

# generate html docs
make html
```

### Generating PyTest Coverage Report 📊

```powershell
# Move to source folder
cd app

# Run the coverage command
coverage run -m pytest ..\tests

# Generate the coverage report
coverage html

# Open the index.html file in the htmlcov folder to view the report
```

### Generating User Manual 📖

```powershell
# NOTE: Always use the Linux Subsystem for Windows to generate the user manual. 

# Ensure tpyer-cli is installed
pip3 install typer-cli

# Move to source folder
cd app

# Generate the user manual in command line 
typer VocabularyCLI.py utils docs

# To generate the docs the rich help text must be commented out in the main file (VocabularyCLI.py) and the modules.* imports must also be commented out. Use the Regex in Notes.md to comment out the rich help text.

# Write the user manual to a file
typer VocabularyCLI.py utils docs --name "VocabularyCLI" --output "../docs/user_manual.md"
```

---

## Contributors ✨

Thanks goes to these wonderful people: <br>
![](https://contrib.rocks/image?repo=VocabCLI/VocabCLI)

---

## License 📜

This project follows the [MIT License](https://github.com/VocabCLI/VocabCLI/blob/main/LICENSE.md)
Copyright (c) 2021 Atharva Shah, Anay Deshpande
