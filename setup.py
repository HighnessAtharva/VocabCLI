from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A stylish and modern CLI to help you build your vocabulary and manage your words.'
LONG_DESCRIPTION = 'Lightweight CLI for Dictionary Lookups, Vocabulary Building, Quote Saving and enhancing Knowledge Base. Supported with Rich Markup, Graph Reporting and Flashcard Generation'


setup(
       # the name must match the folder name 'verysimplemodule'
        name="VocabularyCLI", 
        version=VERSION,
        author="Atharva Shah, Anay Deshpande",
        author_email="<HighnessAtharva@gmail.com>, <anaydesh1234@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        # add any additional packages that
        install_requires=['typer', 'rich', 'matplotlib', 'pytest', 'random_word', 'playsound'],  
        
        keywords=['python', 'vocabulary', 'cli', 'dictionary', 'flashcards', 'quotes', 'knowledgebase', 'rich', 'richmarkup', 'graph', 'reporting', 'flashcard'],
        classifiers= [
            "Development Status :: 1 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)