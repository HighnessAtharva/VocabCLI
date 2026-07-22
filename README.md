<div align="center">

# 📕 VocabCLI

**The AI-powered vocabulary builder for linguaphiles — right in your terminal.**

[![CI](https://github.com/HighnessAtharva/VocabCLI/actions/workflows/ci.yml/badge.svg)](https://github.com/HighnessAtharva/VocabCLI/actions)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](https://pypi.org/project/vocabcli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)
[![PyPI](https://img.shields.io/pypi/v/vocabcli)](https://pypi.org/project/vocabcli/)

</div>

---

## ⚡ Install

```bash
pip install vocabcli             # core features
pip install "vocabcli[ai]"       # + OpenAI-powered tools
pip install "vocabcli[nlp]"      # + spaCy / transformers (heavy, opt-in)
```

> **Recommended:** `pipx install "vocabcli[ai]"` for an isolated, globally-available install.

---

## 🚀 30-Second Quickstart

```bash
# First-run setup (API key, provider preferences)
vocab setup

# Look up a word
vocab define serendipity

# AI deep-dive with etymology, register, and memory tip
vocab ai explain serendipity

# Generate a mnemonic to remember it
vocab ai mnemonic serendipity

# Add to your learning list & start spaced-repetition review
vocab learn serendipity
vocab review

# Check your streak
vocab streak
```

---

## ✨ Feature Grid

| Category | Features |
|---|---|
| 📚 **Dictionary** | Definitions, phonetics, audio pronunciation, commonly confused words |
| 🔤 **Thesaurus** | Synonyms & antonyms via API + NLTK WordNet fallback |
| 🧠 **Spaced Repetition** | SM-2 algorithm (`vocab review`) — the Anki algorithm built-in |
| 🤖 **AI Explain** | Etymology, register, usage tips, memory hook — streamed live |
| 🧠 **AI Mnemonic** | Vivid story hooks cached locally for instant re-display |
| 📖 **AI Story** | Short narrative using all your learning-list words |
| 💬 **AI Chat** | Interactive vocabulary tutor with conversation context |
| ❓ **AI Quiz** | Advanced question types: analogies, fill-in-the-blank, context usage |
| 🎫 **Flashcards** | Beautiful PIL-generated image cards for learning/mastered/favorite lists |
| 📊 **Graphs** | 8 visualisations: word distribution, tags, categories, weekly/monthly trends |
| 📥 **Import/Export** | Bulk CSV import, PDF export, quiz history export |
| 📰 **RSS Reader** | Subscribe to feeds; highlighted vocabulary words appear inline |
| 🔤 **NLP Tools** | Sentiment analysis, readability index, text summarization, bad-word censor |
| 🔥 **Streaks** | Daily lookup streak tracking |
| 💡 **AI Suggest** | Personalised next-10-words recommendation based on your history |

---

## 🤖 AI Features Spotlight

### `vocab ai explain <word>`
Streams an educator-quality explanation covering etymology, core meaning, register (formal/informal/archaic), when to use it, when **not** to, and a memory tip.

### `vocab ai mnemonic <word>`
```
Think of EPHEMERAL as an EP record — it barely lasts long enough to play one side.
```

### `vocab ai story`
Takes every word in your `--learning` list and weaves them into a 150–200 word narrative.  Reading words in context dramatically improves retention.

### `vocab ai chat`
An interactive vocabulary tutor you can ask anything:
> *"What's the difference between ephemeral and transient?"*

### Local / Offline AI with Ollama

```toml
# ~/.vocabcli/config.toml
[ai]
provider = "ollama"
model    = "llama3.2"
```

All AI commands then route to your local Llama 3 / Mistral instance — no API key, no cloud, complete privacy.

---

## 🗄 Database & Configuration

VocabCLI stores everything in `~/.vocabcli/`:

```
~/.vocabcli/
├── VocabularyBuilder.db   # SQLite — words, cache, quiz history, ai_cache, streaks
└── config.toml            # User preferences
```

Manage config from the command line:

```bash
vocab config --show
vocab config --set ai.provider=ollama
vocab config --set ai.model=llama3.2
```

---

## 🔁 Spaced Repetition (SM-2)

```bash
vocab learn ephemeral serendipity eloquent

# The next morning, review only words due today:
vocab review

# Rate your recall: 1=forgot  3=hard  5=easy
# VocabCLI automatically schedules the next review date
```

The [SM-2 algorithm](https://www.supermemo.com/en/blog/application-of-a-computer-to-improve-the-results-obtained-in-working-with-the-supermemo-method) — the same one used by Anki — adjusts review intervals based on your ratings.

---

## 🎯 Complete Command Reference

```
vocab define <word>          Look up a word
vocab synonym <word>         Find synonyms
vocab antonym <word>         Find antonyms
vocab learn <word>           Add to learning list
vocab master <word>          Mark as mastered
vocab revise <word>          Revise a word
vocab review                 Spaced-repetition review (words due today)
vocab quiz                   Classic 4-choice definition quiz
vocab flashcard              Generate flashcard images

vocab streak                 View daily lookup streak
vocab today                  Word of the day
vocab daily_quote            Quote of the day

vocab ai explain <word>      Deep AI word explanation
vocab ai mnemonic <word>     Generate/show mnemonic
vocab ai story               Story using learning list
vocab ai sentence <word>     3 example sentences
vocab ai suggest             Personalised recommendations
vocab ai quiz                Advanced AI quiz
vocab ai chat                Interactive tutor
vocab ai paraphrase <text>   AI paraphrase

vocab setup                  First-run setup wizard
vocab config                 View/set configuration
vocab refresh                Refresh API cache
vocab about                  About VocabCLI
```

---

## 🛠 Development Setup

```bash
git clone https://github.com/HighnessAtharva/VocabCLI.git
cd VocabCLI
pip install -e ".[dev,ai]"

# Run tests from repo root
pytest
```

---

## 📚 Documentation

Full documentation at **[vocabcli.github.io](https://vocabcli.github.io)** *(built with MkDocs Material)*

---

## 🤝 Contributors

Built with ❤️ by **Atharva Shah** and **Anay Deshpande**.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/AtharvaShah)

---

## 📄 License

[MIT License](LICENSE.md)

<!-- social-footer -->
---

<div align="center">

**Atharva Shah** — Python & AI Engineer · Developer Advocate · Technical Writer

[![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=About.me&logoColor=white)](https://atharvashah.com)
[![Blog](https://img.shields.io/badge/Blog-FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://blog.atharvashah.com)
[![Twitter](https://img.shields.io/badge/Twitter-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/cultist_dev)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/atharva-shah-tech/)

</div>
