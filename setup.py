from setuptools import setup, find_packages

with open ("README.md", "r", encoding='utf-8') as fh:
     LONG_DESCRIPTION = fh.read()
     
setup(
    name="vocabCLI",
    version='0.0.15',
    author="Atharva Shah, Anay Deshpande",
    author_email="<HighnessAtharva@gmail.com>, <anaydesh1234@gmail.com>",
    description='A stylish and modern CLI to help you build your vocabulary and manage your words.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
 
    packages=find_packages("modules", exclude="tests"),
 
    # add any additional packages that
    install_requires=["bs4", "click", "configparser", "dateparser", "feedparser", "fpdf", "lxml", "matplotlib", "nltk", "numpy", "pandas", "Pillow", "playsound==1.2.2", "pyspellchecker", "requests", "rich", "seaborn", "spacy", "spacy-loggers", "spacytextblob", "textblob", "textstat", "tk", "torch", "torchaudio", "torchvision", "typer",  "typer[all]"],

    keywords=['python', 'vocabulary', 'cli', 'dictionary', 'flashcards', 'quotes',
              'knowledgebase', 'rich', 'richmarkup', 'graph', 'reporting', 'flashcard'],
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        "console_scripts": [
            "vocab = vocabCLI.__main__:app"
        ]
    },
)