from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'A stylish and modern CLI to look up words, save quotes and build vocabulary and perform Natural Language Processing with ease.'


def readme():
    with open('README.md', encoding='utf-8') as f:
        README = f.read()
    return README


setup(
    # the name must match the folder name 'verysimplemodule'
    name="VocabCLI",
    version=VERSION,
    author="Atharva Shah, Anay Deshpande",
    author_email="<HighnessAtharva@gmail.com>, <anaydesh1234@gmail.com>",
    description=DESCRIPTION,
    long_description=readme(),
    long_description_content_type="text/markdown",
    license='MIT',
    # these are packages inside vocabCLI folder (i.e packages made by us)
    packages=find_packages(include=['vocabCLI', 'vocabCLI.*']),
    include_package_data=True,
    # these are external packages needed (third party dependencies to be pulled from requirements.txt)
    install_requires=[
        "attrs",
        "autopep8",
        "bs4",
        "certifi",
        "charset-normalizer",
        "click",
        "colorama",
        "commonmark",
        "configparser",
        "dateparser",
        "db",
        "db-sqlite3",
        "feedparser",
        "fpdf",
        "homophones",
        "huggingface-hub",
        "lxml",
        "idna",
        "iniconfig",
        "kiwisolver",
        "matplotlib",
        "mkdocs",
        "nltk",
        "numpy",
        "packaging",
        "pandas",
        "Pillow",
        "playsound==1.2.2",
        "pluggy",
        "py",
        "Pygments",
        "pyparsing",
        "pyspellchecker",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "Random-Word",
        "requests",
        "rich",
        "scikit-learn",
        "seaborn",
        "shellingham",
        "spacy",
        "spacy-alignments",
        "spacy-legacy",
        "spacy-loggers",
        "spacytextblob",
        "six",
        "textblob",
        "textstat",
        "tomli",
        "tk",
        "torch",
        "torchaudio",
        "torchvision",
        "typer",
        "typer-cli",
        "urllib3",
        "black",
    ],

    keywords=['python', 'vocabulary', 'cli', 'dictionary', 'flashcards', 'quotes',
              'knowledgebase', 'rich', 'richmarkup', 'graph', 'reporting', 'flashcard'],
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'vocab = vocabCLI.__main__:app',
            'vocabcli = vocabCLI.__main__:app'
        ],
    },
)
