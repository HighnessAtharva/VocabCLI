# VocabularyBuilder CLI

<hr>

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
- RUN `python -m pytest ../tests` in terminal
<hr>


## Features 🎯

- Allow users to lookup word definitions
- Generate flashcards for revision
- Allow tagging of words (i.e. for categorization) such as "learning" or "mastered" or "SAT 1000 word list"
- Recommend potential words for vocabulary building based on lookup history
- Maintain lookup history and report it daily/weekly/monthly
- Generate learning graphs (matplotlib/seaborn)
- Allow saving of quotes (possibly reading from clipboard/browser)

