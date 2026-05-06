# Changelog

All notable changes to VocabCLI are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [2.0.0] – 2026-05-06  *(VocabCLI 2026 Reinvention)*

### Added

#### AI Features (new `vocab ai` command group)
- `vocab ai explain <word>` – deep etymological + usage explanation, streamed live
- `vocab ai mnemonic <word>` – vivid mnemonic story hook, cached to SQLite
- `vocab ai story` – short narrative using all words in your learning list
- `vocab ai sentence <word>` – 3 contextually diverse example sentences (formal/casual/literary)
- `vocab ai suggest` – personalised next-10-words recommendation based on lookup history
- `vocab ai quiz` – AI-generated quiz with advanced question types (analogies, fill-in-the-blank)
- `vocab ai chat` – interactive conversational vocabulary tutor with streaming output
- `vocab ai paraphrase <text>` – lightweight AI paraphrase (replaces heavy transformer approach)
- `--provider openai|ollama` flag on all `ai` sub-commands for local/offline LLM support
- `ai_cache` SQLite table – caches all AI responses to avoid repeated API calls

#### Infrastructure
- `pyproject.toml` – proper PEP 517 packaging, optional extras `[ai]`, `[nlp]`, `[dev]`
- `MANIFEST.in` – bundles CSV/font/asset files in the distributed wheel
- `vocab = "vocabCLI.vocabCLI:app"` entry point so `vocab` works after `pip install vocabcli`
- Database now lives in `~/.vocabcli/VocabularyBuilder.db` (user-scoped, persists across CWD changes)
- `VOCABCLI_DB_PATH` env var to override database path (used by tests)
- `~/.vocabcli/config.toml` configuration file
- `vocabCLI/modules/Config.py` – config reader/writer with `tomllib`
- `vocabCLI/modules/AI.py` – central AI abstraction layer
- `asyncio` + `httpx` parallel cache refresh (replaces sequential `requests` loop)
- SM-2 spaced-repetition columns added to `words` table: `ease_factor`, `interval_days`, `next_review_date`, `review_count`
- `streaks` SQLite table for daily lookup tracking

#### New Commands
- `vocab setup` – interactive first-run setup wizard (API key, provider, preferences)
- `vocab review` – SM-2 spaced-repetition review session with recall rating
- `vocab config [--show] [--set section.key=value]` – view/update config
- `vocab today` – alias for `daily_word` that always works (no Wordnik key required)

#### Testing
- `tests/test_ai.py` – full test suite for AI module with mocked OpenAI client
- `tests/test_config.py` – config module + database path tests
- Updated `conftest.py` – tests now run from repo root with `pytest`; use temp DB via `VOCABCLI_DB_PATH`
- `.github/workflows/ci.yml` – CI on Python 3.11/3.12/3.13 × Linux/macOS/Windows with PyPI publishing

#### Documentation
- `mkdocs.yml` – MkDocs Material documentation site configuration
- `CHANGELOG.md` – this file

### Changed

- **OpenAI API**: updated from deprecated `openai==0.26.1` to `openai>=1.50` (new client pattern)
- **Audio playback**: replaced abandoned `playsound==1.2.2` with `pygame.mixer` (works on all platforms)
- **PDF generation**: replaced deprecated `fpdf==1.7.2` with `fpdf2>=2.8`
- **Requirements**: all dependencies updated to 2026-era versions; `torch`/`transformers`/`spacy` moved to optional `[nlp]` extra
- **Data file paths**: replaced CWD-relative `"modules/foo.csv"` with `Path(__file__).parent / "foo.csv"` throughout
- **Asset paths**: Flashcard font/image assets now resolved relative to `__file__` instead of CWD
- **DB path**: moved from `./VocabularyBuilder.db` (CWD) to `~/.vocabcli/VocabularyBuilder.db`
- **`get_word_of_the_day`**: falls back to curated word list when `WORDNIK_API_KEY` is absent
- **`insert_word_to_db`**: removed gratuitous `time.sleep(1)` bottleneck
- **`refresh_cache`**: rewritten with `asyncio` + `httpx` for parallel fetching
- **Module imports**: converted bare `from Database import …` to relative `from .Database import …`
- **Shell completion**: enabled (`add_completion=True`) so `vocab --install-completion` works
- **`vocabCLI/__init__.py`**: bumped version to `2.0.0`

### Removed

- `playsound` dependency
- `fpdf` (old, deprecated library)
- `spellchecker==0.4` duplicate (only `pyspellchecker` is now used)
- Stale `openai.api_key = os.getenv("OPENAI")` pattern
- `time.sleep(1)` in `insert_word_to_db`
- `sys.path` hacks in test files (replaced with `pythonpath = ["vocabCLI"]` in `pyproject.toml`)

### Fixed

- `say_aloud` crashes on Linux/macOS due to `playsound` being abandoned
- Hard-coded relative paths breaking when `vocab` is run from any directory other than `vocabCLI/`
- `openai.Completion.create` call in `NLP.py` (old API removed in openai 1.0)
- Test database leaking into the user's home directory
- Module imports failing when the package is installed via `pip`

---

## [1.0.0] – 2023-01-01  *(Original Release)*

Initial public release of VocabCLI.

### Features
- Dictionary lookups via [Free Dictionary API](https://dictionaryapi.dev/)
- Thesaurus (synonyms/antonyms) via NLTK WordNet
- Word management: learning / mastered / favorite lists
- Tag system
- Flashcard generation (PIL)
- Quiz mode (4-choice definition quiz)
- Graph reporting (Matplotlib/Seaborn)
- Bulk import/export (CSV, PDF)
- NLP tools: sentiment analysis, readability, summarization, hard-word extraction
- RSS feed reader
- Quote saving
- Spell checker
- Word of the Day (Wordnik API)
- Rich terminal UI

[2.0.0]: https://github.com/HighnessAtharva/VocabCLI/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/HighnessAtharva/VocabCLI/releases/tag/v1.0.0
