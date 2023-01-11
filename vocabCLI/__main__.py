from .vocabCLI import app

# Run it with `python3 -m vocabCLI`
if __name__ == "__main__":
    
    # check if Vocabulary.db exists, if not create it
    if not os.path.exists("VocabularyBuilder.db"):
        from vocabCLI.modules.Database import initializeDB
        from vocabCLI.modules.WordCollections import delete_collection_from_DB, clean_collection_csv_data, insert_collection_to_DB
        
        # initialize the database with the tables if not already existing
        initializeDB()
        # uncomment this to easily delete all words from collections table during testing
        # delete_collection_from_DB()
        clean_collection_csv_data()
        # add all the collection words to the database if not already existing
        insert_collection_to_DB()

    app()