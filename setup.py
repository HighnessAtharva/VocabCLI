from setuptools import setup, find_packages
import vocabCLI

     
setup(
    name="vocabCLI",
    version='0.0.16',
    author="Atharva Shah, Anay Deshpande",
    author_email="<HighnessAtharva@gmail.com>, <anaydesh1234@gmail.com>",
    description='A stylish and modern CLI to help you build your vocabulary and manage your words.',
    long_description=open('README.md', encoding='utf-8').read(),
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
         "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "vocab = vocabCLI.vocabCLI:app",
            "vocabCLI = vocabCLI.vocabCLI:app"
        ]
    },
)