# VocabCLI TODO

## Priority

### ANAY

- [x]  Adding Panels Emojies and Rich Styling everywhere.
- [x]  Update Docstrings based on new functions and arguments. Also mention data type and return type in all the functions.
- [ ]  Generate Requirements.txt after reinstalling linux
- [x]  Add more words to domains.csv with the right topic name.
- [x]  Get Linux Installed and try out asciinema
- [ ]  Github Pages Improvement
- [ ]  Start with application promo on Reddit, Discord and other platforms to get early adopters and feedback.
- [ ]  FlashCard Generation Code (for Export, and Slide Show)

### ATHARVA


- [x]  Add Heading to Panels @Anay
- [ ]  Generate Coverage Report, Add All Missing Tests for Existing Commands
- [ ]  FlashCard Generation - Download or View Options (Enable Carousel for viewing) (Desing a Template First @AtharvaShah)
- [x]  Get Linux Installed @anay and try out asciinema
- [ ]  Github Pages Improvement @anay
- [ ]  Maintain Quiz History (need a separate table-> Quiz Type | Count | Duration | Points | )
- [ ]  Add Progress Bar to Refresh Cache (takes a while)
- [ ]  Generate Coverage Report, Add All Missing Tests for Existing Commands
- [ ]  Complete rest of the graph commands
- [x]  Flashcard Generation Design Template
- [x]  5 Graph Carousel
- [x]  Basic NLP (Sentiment Analysis, Word Processing, etc)
- [x]  Exception Refactoring
- [x]  Quiz and Revise Command
- [x]  Test Cases Refactoring

## College Related Submission/Work

### ANAY

- [x] 100 page notebook, use it for rough work to show proof of work.
- [ ] Handwriting and diagrams need not be fancy but should be readable. Use it to jot down ideas.
- [ ] First few pages should be in the following order:-
      -  Project Title and Members
      -  Organization summary  
      -  Project Scope

### ATHARVA + ANAY

- [ ] Diagrams (Rough Sketch)
      -  Context Level Diagram
      -  Data Flow Diagram (First Level)
      -  Use Case Diagram
      -  Activity Diagram
      -  Sequence Diagram
  As per Ma'am instruction, rough sketch is expected. You can cross out and redraw diagrams as many times as you want. Brainstorming and jotting down ideas and maintaining a log of progress is the main purpose of this notebook. The actual digital diagrams will serve as the final version so don't worry too much about drawing diagrams correctly in the notebook.

## Low Priority (Do This Before 25th Dec)

### ANAY

- [ ] Prepare a dummy database with lots of words (5000 words -> 500 fav, 500 learning, 500 mastered and 2000 words should have 200 tags) and test the performance of the application on a large scale.  (Use <https://www.mockaroo.com/> or <https://generatedata.com/> or <https://www.onlinedatagenerator.com/>)
- [ ] Data Gathering - Collect 25 total paragraphs (5 x 5 different topics (like sports, politics, etc)) of 200 words each and save it in NLP.py in modules folder. This will be the test data for sentinment analysis, word processing and other NLP related tasks.

---

## To Handle Later

[ ] Help command alignment
[ ] Debug command prompt resizing issue
[ ] Do error handling everywhere where user is typing incorrect input (example:wrong tag/ date/ days, etc)
[ ] Test cases for all the functions I have commented as: no tests for this function as it is not called anywhere in the command directly
[ ] Generate Markdown Articles based on the RSS feed added by the user. Support for multiple RSS feeds. Try with Pitchfork, Tor Publishing, The Guardian, Entertainment Weekly, IGN, etc.

---

## Domains to Target

Get 1000 words from each domain and add them to a CSV. Will be read into a DF later.
From domain.csv remove all the rows which contain a space and hyphen in the word column. (This is because the words are not valid for the API)

- Arts ✅ (can refine)
- Music ✅
- Entetainment  ✅
- Astronomy ✅
- Sports   ✅
- Politics  ✅
- History    ✅
- Geography ✅
- Medical   ✅
- Legal and Law ✅
- Literature    ✅
- Culture     ✅
- Technology   ✅
- Business    ✅
- Chemistry   ✅
- Biology     ✅
- Mathematics   ✅

## Things to Do After Finishing the Project

[ ] Publishing to PyPI
[ ] Generate Requirements.txt
[ ] Generate the documentation, check formatting, correctness and theme and link it to website and PyPI
[ ] Generate the release notes
[ ] Generate an executable file and upload it to the release page on GitHub
[ ] Generate command list and attach it to readme and website
[ ] Add proper content and styling to VocabCLI.github.io
[ ] Record demo screenscasts using asciinema and publish them on the website
[ ] Draw UML Diagrams and get them approved:

  1. Context Level Diagram
  2. Data Flow Diagram (First Level)
  3. Class Diagram
  4. Use Case Diagram
  5. Activity Diagram
  6. Sequence Diagram)
[ ] Split the test files into multiple files based on Classes or Modules
[ ] Final Project Report for College Submission

## Notes

### Datetimes

Date Time Format -  %Y-%m-%d %H:%M:%S

### Color Formats

for errors: red
for mastered words: green
for favorite words: gold1
for learning words: blue

### Regex to Replace the Style in Markdown Typer Doc [bold blue]asdasd[/(bold blue)] -> Remove the Styles

\[(bold.*?)\]
\[/(bold.*?)\]
