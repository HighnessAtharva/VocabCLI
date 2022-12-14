# `vocabCLI`

:book: This is a dictionary and a vocabCLI CLI.

**Usage**:

```console
$ vocabCLI [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `about`: 💻 About the software
* `antonym`: ❌ Find antonyms for a...
* `bye`: 👋🏼 Exits the CLI
* `clear`: 🧹 Clears all lists
* `define`: 📚 Lookup a word in the...
* `delete`: 🚮 Deletes the word from the database
* `export`: 📂 Exports a list of...
* `favorite`: 💙 Sets a word as...
* `flashcard`: 📇 Create flashcards for words in your...
* `graph`: 📚 Generate Graphical Charts based on your...
* `history`: 🔁 Get a lookup history of a word
* `import`: 🔼 Imports a list words...
* `learn`: ✍🏼 Sets a word as...
* `list`: 📝 Lists  of all your...
* `master`: 🧠 Sets a word as...
* `quiz`: ❓ Take a quiz on words in your learning list
* `random`: 🔀 Gets a random word
* `rate`: 📊 Learning Rate gives...
* `refresh`: 🔄 Update the JSON response in the cache
* `revise`: 💡 Revise words from your learning list
* `synonym`: 🔎 Find synonyms for a...
* `tag`: 🔖 Tags a word
* `unfavorite`: 💔 Removes the word from...
* `unlearn`: 😪 Removes the word from...
* `unmaster`: 🤔 Removes the word from...
* `untag`: ✂  Removes tag of a word...

## `vocabCLI about`

💻 About the software

**Usage**:

```console
$ vocabCLI about [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI antonym`

❌ Find antonyms for a word

**Usage**:

```console
$ vocabCLI antonym [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to search antonyms for  [required]

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI bye`

👋🏼 Exits the CLI

**Usage**:

```console
$ vocabCLI bye [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI clear`

🧹 Clears all lists

**Usage**:

```console
$ vocabCLI clear [OPTIONS]
```

**Options**:

* `-l, --learning`: Clear all words in your learning list  [default: False]
* `-m, --mastered`: Clear all words in your mastered list  [default: False]
* `-f, --favorite`: Clear all words in your favorite list  [default: False]
* `-t, --tag TEXT`: Clear all words with a particular tag
* `--help`: Show this message and exit.

## `vocabCLI define`

📚 Lookup a word in the dictionary

**Usage**:

```console
$ vocabCLI define [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to search  [required]

**Options**:

* `-s, --short`: Lightweight definitions.  [default: False]
* `-p, --pronounce`: Pronounce the word.  [default: False]
* `--help`: Show this message and exit.

## `vocabCLI delete`

🚮 Deletes the word from the database

**Usage**:

```console
$ vocabCLI delete [OPTIONS] [WORDS]...
```

**Arguments**:

* `[WORDS]...`: Word to be deleted

**Options**:

* `-m, --mastered`: Deletes all mastered words  [default: False]
* `-l, --learning`: Deletes all learning words  [default: False]
* `-f, --favorite`: Deletes all favorite words  [default: False]
* `-t, --tag TEXT`: Tag of words to be deleted
* `--help`: Show this message and exit.

## `vocabCLI export`

📂 Exports a list of all your looked up words

**Usage**:

```console
$ vocabCLI export [OPTIONS]
```

**Options**:

* `-P, --pdf`: Export a list of your looked up words in PDF format.  [default: False]
* `--help`: Show this message and exit.

## `vocabCLI favorite`

💙 Sets a word as favorite

**Usage**:

```console
$ vocabCLI favorite [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to add to favorites.  [required]

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI flashcard`

📇 Create flashcards for words in your learning list

**Usage**:

```console
$ vocabCLI flashcard [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI graph`

📚 Generate Graphical Charts based on your vocabulary

**Usage**:

```console
$ vocabCLI graph [OPTIONS]
```

**Options**:

* `-twb, --topwordsbar INTEGER RANGE`: Bar Graph of Top N Most Looked Up Words
* `-ttb, --toptagsbar INTEGER RANGE`: Bar Graph of Top N Tags with the most words.
* `-twp, --topwordspie INTEGER RANGE`: Pie Chart of Top N Most Looked Up Words
* `-ttp, --toptagspie INTEGER RANGE`: Pie Chart of Top N Tags with the most words.
* `-lw, --lookupweek`: Bar Graph of the word count distribution for days in the past week.  [default: False]
* `-lm, --lookupmonth`: Bar Graph of the word count distribution for days in the past month.  [default: False]
* `-ly, --lookupyear`: Bar Graph of the word count distribution for days in the past year.  [default: False]
* `-lvm, --learnvsmaster`: Stacked Graph the number of words in your learning list vs. your mastered list.  [default: False]
* `-s, --slider`: Shows all graphs one by one in a slider.  [default: False]
* `--help`: Show this message and exit.

## `vocabCLI history`

🔁 Get a lookup history of a word

**Usage**:

```console
$ vocabCLI history [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to get lookup history for  [required]

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI import`

🔼 Imports a list words in the application

**Usage**:

```console
$ vocabCLI import [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI learn`

✍🏼 Sets a word as learning

**Usage**:

```console
$ vocabCLI learn [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to add to learning.  [required]

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI list`

📝 Lists  of all your looked up words

**Usage**:

```console
$ vocabCLI list [OPTIONS]
```

**Options**:

* `-f, --favorite`: Get a list of your favorite words.  [default: False]
* `-l, --learning`: Get a list of words in your learning list.  [default: False]
* `-m, --mastered`: Get a list of words in your mastered list.
* `-t, --tag TEXT`: Get a list of words with a particular tag.
* `-d, --days INTEGER`: Get a list of words from last n number of days.
* `-D, --date`: Get a list of words from a particular date.  [default: False]
* `-L, --last INTEGER`: Get a list of last searched words.
* `-M, --most INTEGER`: Get a list of most searched words.
* `-T, --tagnames`: Get a list of all the tags.  [default: False]
* `--help`: Show this message and exit.

## `vocabCLI master`

🧠 Sets a word as mastered

**Usage**:

```console
$ vocabCLI master [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to add to mastered.  [required]

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI quiz`

❓ Take a quiz on words in your learning list

**Usage**:

```console
$ vocabCLI quiz [OPTIONS]
```

**Options**:

* `-n, --number INTEGER RANGE`: Number of words to quiz on. If not specified, all words will be included in the quiz in alphabetical order.
* `-t, --tag TEXT`: Tag of words to quiz on.
* `-l, --learning`: Take a quiz on words in your learning list  [default: False]
* `-m, --mastered`: Take a quiz on words in your mastered list  [default: False]
* `-f, --favorite`: Take a quiz on words in your favorite list  [default: False]
* `-c, --collection TEXT`: Take a quiz on words in a particular collection
* `--help`: Show this message and exit.

## `vocabCLI random`

🔀 Gets a random word

**Usage**:

```console
$ vocabCLI random [OPTIONS]
```

**Options**:

* `-l, --learning`: Get a random learning word  [default: False]
* `-m, --mastered`: Get a random mastered word  [default: False]
* `-f, --favorite`: Get a random favorite word  [default: False]
* `-t, --tag TEXT`: Get a random word from a particular tag
* `--help`: Show this message and exit.

## `vocabCLI rate`

📊 Learning Rate gives the number of words you have learned in a particular time period with a comparison of a previous time period

**Usage**:

```console
$ vocabCLI rate [OPTIONS]
```

**Options**:

* `-t, --today`: Get learning rate today  [default: False]
* `-w, --week`: Get learning rate this week  [default: False]
* `-m, --month`: Get learning rate this month  [default: False]
* `-y, --year`: Get learning rate this year  [default: False]
* `--help`: Show this message and exit.

## `vocabCLI refresh`

🔄 Update the JSON response in the cache

**Usage**:

```console
$ vocabCLI refresh [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI revise`

💡 Revise words from your learning list

**Usage**:

```console
$ vocabCLI revise [OPTIONS]
```

**Options**:

* `-n, --number INTEGER`: Number of words to revise in random order.
* `-t, --tag TEXT`: Revise words in a particular tag.
* `-l, --learning`: Revise words in your learning list  [default: False]
* `-m, --mastered`: Revise words in your mastered list  [default: False]
* `-f, --favorite`: Revise words in your favorite list  [default: False]
* `-c, --collection TEXT`: Revise words in a particular collection
* `--help`: Show this message and exit.

## `vocabCLI synonym`

🔎 Find synonyms for a word

**Usage**:

```console
$ vocabCLI synonym [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to search synonyms for  [required]

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI tag`

🔖 Tags a word

**Usage**:

```console
$ vocabCLI tag [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Words to tagged  [required]

**Options**:

* `-n, --name TEXT`: Tag to add to the words  [required]
* `--help`: Show this message and exit.

## `vocabCLI unfavorite`

💔 Removes the word from favorites

**Usage**:

```console
$ vocabCLI unfavorite [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to remove from favorites  [required]

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI unlearn`

😪 Removes the word from learning

**Usage**:

```console
$ vocabCLI unlearn [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to remove from learning  [required]

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI unmaster`

🤔 Removes the word from mastered

**Usage**:

```console
$ vocabCLI unmaster [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to remove from mastered  [required]

**Options**:

* `--help`: Show this message and exit.

## `vocabCLI untag`

✂  Removes tag of a word in the dictionary

**Usage**:

```console
$ vocabCLI untag [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to remove tag from  [required]

**Options**:

* `--help`: Show this message and exit.