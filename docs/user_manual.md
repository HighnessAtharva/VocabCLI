# `VocabularyCLI`

📕 This is a dictionary and a vocabulary builder CLI. VocabularyCLI is a lightweight Command Line Interface that allows users to look up word definitions, examples, synonyms and antonyms directly via the command line. Powered with several utility based commands our CLI offers rapid and robust Knowledge Base capabilities like Flashcards, Tagging, Word Management, Graph Reporting, Bulk import and export of word lists and is a definitive software for linguaphiles. This application boasts a simple and intuitive interface that is easy to use and is a must have for anyone who wants to expand their vocabulary and improve their language skills. The app also offers advanced Text Classification and Processing via the use of Natural Language Processing. The CLI will be offered with eye-catching Panels, Tables, Animated Symbols, Emojis, Interactive Menus, Spinners, Colored fonts and other rich features that will make the user experience more enjoyable and interactive.

**Usage**:

```console
$ VocabularyCLI [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `about`: 💻 About the software
* `antonym`: ❌ Find antonyms for a word
* `bye`: 👋🏼 Exits the CLI
* `clean`: 🧹 Filter out [b red1]Explicit[/b red1] words...
* `clear`: 🧹 Clears all lists.
* `daily-quote`: 🔆 Get quote of the day.
* `daily-word`: 😍 Get word of the day.
* `define`: 📚 Lookup a word in the dictionary
* `delete`: 🚮 Deletes the word from the database
* `export`: 📂 Exports a list of all your looked up words
* `favorite`: 💙 Sets a word as favorite
* `flashcard`: 🎫 Generate flashcards for words in your...
* `graph`: 📊 Generate Graphical Charts based on your...
* `hardwords`: 😯 Extract [b deep_pink2]Difficult[/b...
* `history`: 🔁 Get a lookup history of a word
* `import`: 🔼 Imports a list words in the application
* `learn`: 🎓 Sets a word as learning
* `list`: 📝 Lists of all your looked up words
* `master`: 🧠 Sets a word as mastered
* `milestone`: 🎯 Predict the milestone of words looked up...
* `quiz`: ❓ Take a quiz on word definitions
* `quote`: ✍🏼 Add, View, Search or Delete Delete Quotes
* `random`: 🔀 Gets a random word
* `rate`: 📈 Periodic comparison of words learned
* `readability`: 💯 Get [b plum3]Readability Score[/b plum3] of...
* `refresh`: 🔄 Update the JSON response in the cache
* `revise`: 💡 Revise words from your learning list
* `rss`: 📰 Add, View or Delete [b green4]RSS[/b...
* `sentiment`: 😀😐😞 Get the Sentiment...
* `spellcheck`: 🔠 Spell check your input sentences and find...
* `streak`: 🔥 Get the streak of days you have looked up...
* `summary`: 📝 Generate a Summary[/b...
* `synonym`: 🔎 Find synonyms for a word
* `tag`: 🔖 Tags a word
* `unfavorite`: 💔 Removes the word from favorites
* `unlearn`: 😪 Removes the word from learning
* `unmaster`: 🤔 Removes the word from mastered
* `untag`: 🔪 Removes tag of a word in the dictionary

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

* `WORDS...`: ❌ Word to search antonyms for  [required]

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

🧹 Filter out [b red1]Explicit[/b red1] words in a text or a webpage. Make it SFW!

**Usage**:

```console
$ VocabularyCLI clean [OPTIONS] CONTENT
```

**Arguments**:

* `CONTENT`: 🧹 Text or URL to [b red1]clean[/b red1]  [required]

**Options**:

* `-s, --strict`: 🧹 Completely [b red1]replace[/b red1] all bad words with asterisks.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI clear`

🧹 Clears all lists.

**Usage**:

```console
$ VocabularyCLI clear [OPTIONS]
```

**Options**:

* `-l, --learning`: 🧹 Clear all words in your learning list.  [default: False]
* `-m, --mastered`: 🧹 Clear all words in your mastered list.  [default: False]
* `-f, --favorite`: 🧹 Clear all words in your favorite list.  [default: False]
* `-t, --tag TEXT`: 🧹 Clear all words with a particular tag.
* `--help`: Show this message and exit.

## `VocabularyCLI daily-quote`

🔆 Get quote of the day.

**Usage**:

```console
$ VocabularyCLI daily-quote [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI daily-word`

😍 Get word of the day.

**Usage**:

```console
$ VocabularyCLI daily-word [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI define`

📚 Lookup a word in the dictionary

**Usage**:

```console
$ VocabularyCLI define [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: 📚 Word which is to be defined.  [required]

**Options**:

* `-s, --short`: 📚 Short definition of the word.  [default: False]
* `-p, --pronounce`: 📚 Pronounce the word.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI delete`

🚮 Deletes the word from the database

**Usage**:

```console
$ VocabularyCLI delete [OPTIONS] [WORDS]...
```

**Arguments**:

* `[WORDS]...`: 🚮 Word to be deleted

**Options**:

* `-m, --mastered`: 🚮 Delete all mastered words.  [default: False]
* `-l, --learning`: 🚮 Delete all learning words.  [default: False]
* `-f, --favorite`: 🚮 Delete all favorite words.  [default: False]
* `-t, --tag TEXT`: 🚮 Delete all words with a particular tag.
* `--help`: Show this message and exit.

## `VocabularyCLI export`

📂 Exports a list of all your looked up words

**Usage**:

```console
$ VocabularyCLI export [OPTIONS]
```

**Options**:

* `-P, --pdf`: 📂 Export a list of your looked up words in  PDF format.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI favorite`

💙 Sets a word as favorite

**Usage**:

```console
$ VocabularyCLI favorite [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: 💙 Word to add to favorites.  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI flashcard`

🎫 Generate flashcards for words in your learning list

**Usage**:

```console
$ VocabularyCLI flashcard [OPTIONS]
```

**Options**:

* `-a, --all`: 🎫 Generate for all words.  [default: False]
* `-l, --learning`: 🎫 Generate for words set as learning.  [default: False]
* `-m, --mastered`: 🎫 Generate for words set as mastered.  [default: False]
* `-f, --favorite`: 🎫 Generate for words set as favorite.  [default: False]
* `-t, --tag TEXT`: 🎫 Generate for words with a specific tag.
* `--help`: Show this message and exit.

## `VocabularyCLI graph`

📊 Generate Graphical Charts based on your vocabulary

**Usage**:

```console
$ VocabularyCLI graph [OPTIONS]
```

**Options**:

* `-twb, --topwordsbar INTEGER RANGE`: 📊 Bar Graph of Top N Most Looked Up Words
* `-ttb, --toptagsbar INTEGER RANGE`: 📊 Bar Graph of Top N Tags with the most words.
* `-twp, --topwordspie`: 📊 Pie Chart of Top 10 Most Looked Up Words  [default: False]
* `-ttp, --toptagspie`: 📊 Pie Chart of Top 10 Tags with the most words.  [default: False]
* `-lw, --lookupweek`: 📊 Bar Graph of the word count distribution for days in the past [b u]week[/b u].  [default: False]
* `-lm, --lookupmonth`: 📊 Bar Graph of the word count distribution for days in the past [b u]month[/b u].  [default: False]
* `-lvm, --learnvsmaster`: 📊 Stacked Graph the number of words in your learning list vs. your mastered list.  [default: False]
* `-wc, --wordcategories`: 📊 Bar Graph of the number of words in a category domain.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI hardwords`

😯 Extract [b deep_pink2]Difficult[/b deep_pink2] Words from a text or a webpage.

**Usage**:

```console
$ VocabularyCLI hardwords [OPTIONS] CONTENT
```

**Arguments**:

* `CONTENT`: 😯 Text or URL to extract [b deep_pink2]difficult words[/b deep_pink2] from  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI history`

🔁 Get a lookup history of a word

**Usage**:

```console
$ VocabularyCLI history [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: 🔁 Word to get lookup history for  [required]

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

🎓 Sets a word as learning

**Usage**:

```console
$ VocabularyCLI learn [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: ✍🏼 Word to add to learning.  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI list`

📝 Lists  of all your looked up words

**Usage**:

```console
$ VocabularyCLI list [OPTIONS]
```

**Options**:

* `-f, --favorite`: 📝 Lists only words set as [r bold gold1]favorite[/r bold gold1].  [default: False]
* `-l, --learning`: 📝 Lists only words set as [r bold green]learning[/r bold green].  [default: False]
* `-m, --mastered`: 📝 Lists only words set as [r bold blue]mastered[/r bold blue].
* `-t, --tag TEXT`: 📝 Lists only words with a particular tag.
* `-d, --days INTEGER`: 📝 Lists only words looked up in the last N days.
* `-D, --date`: 📝 Lists only words looked up on a particular date.  [default: False]
* `-L, --last INTEGER`: 📝 Lists only the last N words looked up.
* `-M, --most INTEGER`: 📝 Lists only the most looked up words.
* `-T, --tagnames`: 📝 Lists only the tags used by the user.  [default: False]
* `-c, --collection TEXT`: 📝 Lists only the words in a particular collection
* `-C, --collections`: 📝 Lists only the collections available.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI master`

🧠 Sets a word as mastered

**Usage**:

```console
$ VocabularyCLI master [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: 🧠 Word to add to mastered.  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI milestone`

🎯 Predict the milestone of words looked up via the app.

**Usage**:

```console
$ VocabularyCLI milestone [OPTIONS] MILESTONE_NUMBER
```

**Arguments**:

* `MILESTONE_NUMBER`: 🎯 Number of words that marks a milestone.  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI quiz`

❓ Take a quiz on word definitions

**Usage**:

```console
$ VocabularyCLI quiz [OPTIONS]
```

**Options**:

* `-n, --number INTEGER RANGE`: ❓ Limit the number of words to quiz on.
* `-t, --tag TEXT`: ❓ Take a quiz on words in a particular tag
* `-l, --learning`: ❓ Take a quiz on words in your learning list  [default: False]
* `-m, --mastered`: ❓ Take a quiz on words in your mastered list  [default: False]
* `-f, --favorite`: ❓ Take a quiz on words in your favorite list  [default: False]
* `-c, --collection TEXT`: ❓ Take a quiz on words in a particular collection
* `-h, --history`: ❓ Show quiz history and statistics  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI quote`

✍🏼 Add, View, Search or Delete Delete Quotes

**Usage**:

```console
$ VocabularyCLI quote [OPTIONS]
```

**Options**:

* `-r, --random`: ✍🏼 Show a random quote from the saved list.  [default: False]
* `-l, --list`: ✍🏼 Display all saved quotes.  [default: False]
* `-d, --delete`: ✍🏼 Delete a quote from the saved list.  [default: False]
* `-a, --add`: ✍🏼 Add a new quote.  [default: False]
* `-S, --search TEXT`: ✍🏼 Search for a quote.
* `-D, --delete-all`: ✍🏼 Delete all quotes.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI random`

🔀 Gets a random word

**Usage**:

```console
$ VocabularyCLI random [OPTIONS]
```

**Options**:

* `-l, --learning`: 🔀 Get a random learning word.  [default: False]
* `-m, --mastered`: 🔀 Get a random mastered word.  [default: False]
* `-f, --favorite`: 🔀 Get a random favorite word.  [default: False]
* `-t, --tag TEXT`: 🔀 Get a random word from a particular tag
* `-c, --collection TEXT`: 🔀 Get a random word from a particular collection
* `--help`: Show this message and exit.

## `VocabularyCLI rate`

📈 Periodic comparison of words learned

**Usage**:

```console
$ VocabularyCLI rate [OPTIONS]
```

**Options**:

* `-t, --today`: 📊 Get learning rate today  [default: False]
* `-w, --week`: 📊 Get learning rate this week  [default: False]
* `-m, --month`: 📊 Get learning rate this month  [default: False]
* `-y, --year`: 📊 Get learning rate this year  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI readability`

💯 Get [b plum3]Readability Score[/b plum3] of a text or a webpage.

**Usage**:

```console
$ VocabularyCLI readability [OPTIONS] CONTENT
```

**Arguments**:

* `CONTENT`: 💯 Text or URL to get readability score from  [required]

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

* `-n, --number INTEGER`: 💡 Number of words to revise in random order.
* `-t, --tag TEXT`: 💡 Revise words in a particular tag.
* `-l, --learning`: 💡 Revise words in your learning list.  [default: False]
* `-m, --mastered`: 💡 Revise words in your mastered list.  [default: False]
* `-f, --favorite`: 💡 Revise words in your favorite list.  [default: False]
* `-c, --collection TEXT`: 💡 Revise words in a particular collection.
* `--help`: Show this message and exit.

## `VocabularyCLI rss`

📰 Add, View or Delete RSS feeds

**Usage**:

```console
$ VocabularyCLI rss [OPTIONS]
```

**Options**:

* `-a, --add TEXT`: 📰 Add a new RSS feed.
* `-l, --list`: 📰 View all RSS feeds.  [default: False]
* `-d, --delete`: 📰 Delete an RSS feed.  [default: False]
* `-r, --read TEXT`: 📰 Read an RSS feed.
* `--help`: Show this message and exit.

## `VocabularyCLI sentiment`

😀😐😞 Get the Sentiment Analysis of a text or a webpage.

**Usage**:

```console
$ VocabularyCLI sentiment [OPTIONS] CONTENT
```

**Arguments**:

* `CONTENT`: 😀😐😞 Text or URL to get sentiment analysis from  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI spellcheck`

🔠 Spell check your input sentences and find the misspelled words.

**Usage**:

```console
$ VocabularyCLI spellcheck [OPTIONS] TEXT
```

**Arguments**:

* `TEXT`: 🔠 Text to spell check.  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI streak`

🔥 Get the streak of days you have looked up words.

**Usage**:

```console
$ VocabularyCLI streak [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI summary`

📝 Generate a Summary of a text or a webpage.

**Usage**:

```console
$ VocabularyCLI summary [OPTIONS] CONTENT
```

**Arguments**:

* `CONTENT`: 📝 Text or URL to summarize  [required]

**Options**:

* `-f, --file`: 📝 [b green]Save[/b green] the summary to a text file.  [default: False]
* `--help`: Show this message and exit.

## `VocabularyCLI synonym`

🔎 Find synonyms for a word

**Usage**:

```console
$ VocabularyCLI synonym [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: 🔎 Word to search synonyms for  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI tag`

🔖 Tags a word

**Usage**:

```console
$ VocabularyCLI tag [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: 🔖 Words to be tagged  [required]

**Options**:

* `-n, --name TEXT`: 🔖 Tag to add to the words  [required]
* `--help`: Show this message and exit.

## `VocabularyCLI unfavorite`

💔 Removes the word from favorites

**Usage**:

```console
$ VocabularyCLI unfavorite [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: 💔 Word to remove from favorites  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI unlearn`

😪 Removes the word from learning

**Usage**:

```console
$ VocabularyCLI unlearn [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: 😪 Word to remove from learning.  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI unmaster`

🤔 Removes the word from mastered

**Usage**:

```console
$ VocabularyCLI unmaster [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: 🤔Word to remove from mastered  [required]

**Options**:

* `--help`: Show this message and exit.

## `VocabularyCLI untag`

🔪 Removes tag of a word in the dictionary

**Usage**:

```console
$ VocabularyCLI untag [OPTIONS] WORDS...
```

**Arguments**:

* `WORDS...`: ✂ Word to remove tag from  [required]

**Options**:

* `--help`: Show this message and exit.
