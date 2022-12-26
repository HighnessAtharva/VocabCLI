# `VocabularyCLI`

📂 This is a dictionary and a vocabulary builder CLI.

**Usage**:

```console
$ VocabularyCLI [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `Search or Delete Delete Quotes`
* `View or Delete RSS feeds`
* `about`: 💻 About the software
* `antonym`: ❌ Find antonyms for a...
* `bye`: 👋🏼 Exits the CLI
* `clean`: Filter out explicit words in a text or a...
* `clear`: 🧹 Clears all lists
* `define`: 📚 Lookup a word in the...
* `delete`: 🚮 Deletes the word from the database
* `export`: 📂 Exports a list of...
* `favorite`: 💙 Sets a word as...
* `flashcard`: 📇 Create flashcards for words in your...
* `graph`: 📚 Generate Graphical Charts based on your...
* `hardwords`: 📝 Extract Difficult Words from a text or a...
* `history`: 🔁 Get a lookup history of a word
* `import`: 🔼 Imports a list words...
* `learn`: ✍🏼 Sets a word as...
* `list`: 📝 Lists  of all your...
* `master`: 🧠 Sets a word as...
* `quiz`: ❓ Take a quiz on words in your learning list
* `random`: 🔀 Gets a random word
* `rate`: 📊 Learning Rate gives...
* `readability`: 📝 Get readability score of a text or a...
* `refresh`: 🔄 Update the JSON response in the cache
* `revise`: 💡 Revise words from your learning list
* `sentiment`: 📝 Get the Sentiment Analysis of a text or a...
* `summary`: 📝 Generate a summary of a text or a webpage.
* `synonym`: 🔎 Find synonyms for a...
* `tag`: 🔖 Tags a word
* `unfavorite`: 💔 Removes the word from...
* `unlearn`: 😪 Removes the word from...
* `unmaster`: 🤔 Removes the word from...
* `untag`: ✂  Removes tag of a word...

## `VocabularyCLI Search or Delete Delete Quotes`

**Usage**:

```console
$ VocabularyCLI Search or Delete Delete Quotes [OPTIONS]
```

**Options**:

* `-s, --show`: Show a random quote from the saved list.  [default: False]
* `-l, --list`: Display all saved quotes.  [default: False]
* `-d, --delete`: Delete a quote from the saved list.  [default: False]
* `-a, --add`: Add a new quote.  [default: False]
* `-S, --search TEXT`: Search for a quote.
* `--help`: Show this message and exit.

## `VocabularyCLI View or Delete RSS feeds`

**Usage**:

```console
$ VocabularyCLI View or Delete RSS feeds [OPTIONS]
```

**Options**:

* `-a, --add TEXT`: Add a new RSS feed.
* `-v, --view`: View all RSS feeds.  [default: False]
* `-d, --delete`: Delete an RSS feed.  [default: False]
* `-r, --read TEXT`: Read an RSS feed.
* `--help`: Show this message and exit.

## `VocabularyCLI about`

💻 About the software

**Usage**:

```console
$ VocabularyCLI about [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI antonym`

❌ Find antonyms for a word

**Usage**:

```console
$ VocabularyCLI antonym [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to search antonyms for  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI bye`

👋🏼 Exits the CLI

**Usage**:

```console
$ VocabularyCLI bye [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI clean`

Filter out explicit words in a text or a webpage. Make it SFW!

**Usage**:

```console
$ VocabularyCLI clean [OPTIONS]
```

**Options**:

* `-s, --strict`: Completely replace all bad words with asterisks.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI clear`

🧹 Clears all lists

**Usage**:

```console
$ VocabularyCLI clear [OPTIONS]
```

**Options**:

* `-l, --learning`: Clear all words in your learning list  [default: False]
* `-m, --mastered`: Clear all words in your mastered list  [default: False]
* `-f, --favorite`: Clear all words in your favorite list  [default: False]
* `-t, --tag TEXT`: Clear all words with a particular tag
* `--help`: Show this message and exit.

## `VocabularyCLI define`

📚 Lookup a word in the dictionary

**Usage**:

```console
$ VocabularyCLI define [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to search  [required]

**Options**:

* `-s, --short`: Lightweight definitions.  [default: False]
* `-p, --pronounce`: Pronounce the word.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI delete`

🚮 Deletes the word from the database

**Usage**:

```console
$ VocabularyCLI delete [OPTIONS] [WORDS]...
```

**Arguments**:

* `[WORDS]...`: Word to be deleted

**Options**:

* `-m, --mastered`: Deletes all mastered words  [default: False]
* `-l, --learning`: Deletes all learning words  [default: False]
* `-f, --favorite`: Deletes all favorite words  [default: False]
* `-t, --tag TEXT`: Tag of words to be deleted
* `--help`: Show this message and exit.

## `VocabularyCLI export`

📂 Exports a list of all your looked up words

**Usage**:

```console
$ VocabularyCLI export [OPTIONS]
```

**Options**:

* `-P, --pdf`: Export a list of your looked up words in PDF format.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI favorite`

💙 Sets a word as favorite

**Usage**:

```console
$ VocabularyCLI favorite [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to add to favorites.  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI flashcard`

📇 Create flashcards for words in your learning list

**Usage**:

```console
$ VocabularyCLI flashcard [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI graph`

📚 Generate Graphical Charts based on your vocabulary

**Usage**:

```console
$ VocabularyCLI graph [OPTIONS]
```

**Options**:

* `-twb, --topwordsbar INTEGER RANGE`: Bar Graph of Top N Most Looked Up Words
* `-ttb, --toptagsbar INTEGER RANGE`: Bar Graph of Top N Tags with the most words.
* `-twp, --topwordspie`: Pie Chart of Top 10 Most Looked Up Words  [default: False]
* `-ttp, --toptagspie`: Pie Chart of Top 10 Tags with the most words.  [default: False]
* `-lw, --lookupweek`: Bar Graph of the word count distribution for days in the past week.  [default: False]
* `-lm, --lookupmonth`: Bar Graph of the word count distribution for days in the past month.  [default: False]
* `-ly, --lookupyear`: Bar Graph of the word count distribution for days in the past year.  [default: False]
* `-lvm, --learnvsmaster`: Stacked Graph the number of words in your learning list vs. your mastered list.  [default: False]
* `-wc, --wordcategories`: Bar Graph of the number of words in a category domain.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI hardwords`

📝 Extract Difficult Words from a text or a webpage.

**Usage**:

```console
$ VocabularyCLI hardwords [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI history`

🔁 Get a lookup history of a word

**Usage**:

```console
$ VocabularyCLI history [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to get lookup history for  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI import`

🔼 Imports a list words in the application

**Usage**:

```console
$ VocabularyCLI import [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI learn`

✍🏼 Sets a word as learning

**Usage**:

```console
$ VocabularyCLI learn [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to add to learning.  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI list`

📝 Lists  of all your looked up words

**Usage**:

```console
$ VocabularyCLI list [OPTIONS]
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
* `-c, --collection TEXT`: Get a list of words from a collection.
* `-C, --collections`: Get a list of all the collections.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI master`

🧠 Sets a word as mastered

**Usage**:

```console
$ VocabularyCLI master [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to add to mastered.  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI quiz`

❓ Take a quiz on words in your learning list

**Usage**:

```console
$ VocabularyCLI quiz [OPTIONS]
```

**Options**:

* `-n, --number INTEGER RANGE`: Limit the number of words to quiz on.
* `-t, --tag TEXT`: Tag of words to quiz on.
* `-l, --learning`: Take a quiz on words in your learning list  [default: False]
* `-m, --mastered`: Take a quiz on words in your mastered list  [default: False]
* `-f, --favorite`: Take a quiz on words in your favorite list  [default: False]
* `-c, --collection TEXT`: Take a quiz on words in a particular collection
* `-h, --history`: Show quiz history and stats  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI random`

🔀 Gets a random word

**Usage**:

```console
$ VocabularyCLI random [OPTIONS]
```

**Options**:

* `-l, --learning`: Get a random learning word  [default: False]
* `-m, --mastered`: Get a random mastered word  [default: False]
* `-f, --favorite`: Get a random favorite word  [default: False]
* `-t, --tag TEXT`: Get a random word from a particular tag
* `-c, --collection TEXT`: Get a random word from a particular collection
* `--help`: Show this message and exit.

## `VocabularyCLI rate`

📊 Learning Rate gives the number of words you have learned in a particular time period with a comparison of a previous time period

**Usage**:

```console
$ VocabularyCLI rate [OPTIONS]
```

**Options**:

* `-t, --today`: Get learning rate today  [default: False]
* `-w, --week`: Get learning rate this week  [default: False]
* `-m, --month`: Get learning rate this month  [default: False]
* `-y, --year`: Get learning rate this year  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI readability`

📝 Get readability score of a text or a webpage.

**Usage**:

```console
$ VocabularyCLI readability [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI refresh`

🔄 Update the JSON response in the cache

**Usage**:

```console
$ VocabularyCLI refresh [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI revise`

💡 Revise words from your learning list

**Usage**:

```console
$ VocabularyCLI revise [OPTIONS]
```

**Options**:

* `-n, --number INTEGER`: Number of words to revise in random order.
* `-t, --tag TEXT`: Revise words in a particular tag.
* `-l, --learning`: Revise words in your learning list  [default: False]
* `-m, --mastered`: Revise words in your mastered list  [default: False]
* `-f, --favorite`: Revise words in your favorite list  [default: False]
* `-c, --collection TEXT`: Revise words in a particular collection
* `--help`: Show this message and exit.

## `VocabularyCLI sentiment`

📝 Get the Sentiment Analysis of a text or a webpage.

**Usage**:

```console
$ VocabularyCLI sentiment [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI summary`

📝 Generate a summary of a text or a webpage.

**Usage**:

```console
$ VocabularyCLI summary [OPTIONS]
```

**Options**:

* `-f, --file`: Save the summary to a text file.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI synonym`

🔎 Find synonyms for a word

**Usage**:

```console
$ VocabularyCLI synonym [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to search synonyms for  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI tag`

🔖 Tags a word

**Usage**:

```console
$ VocabularyCLI tag [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Words to tagged  [required]

**Options**:

* `-n, --name TEXT`: Tag to add to the words  [required]
* `--help`: Show this message and exit.

## `VocabularyCLI unfavorite`

💔 Removes the word from favorites

**Usage**:

```console
$ VocabularyCLI unfavorite [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to remove from favorites  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI unlearn`

😪 Removes the word from learning

**Usage**:

```console
$ VocabularyCLI unlearn [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to remove from learning  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI unmaster`

🤔 Removes the word from mastered

**Usage**:

```console
$ VocabularyCLI unmaster [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to remove from mastered  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI untag`

✂  Removes tag of a word in the dictionary

**Usage**:

```console
$ VocabularyCLI untag [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: Word to remove tag from  [required]

**Options**:

* `--help`: Show this message and exit.
