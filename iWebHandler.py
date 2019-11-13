import dataset
from Entry import *
from Word import *
from DataProcessing import *
import re

class iWebHandler:
    db = "NA"
    db_url = "NA"

    def __init__(self, db_url):
        # sets the db_url to
        # the given sqlite url
        if type(db_url) != str:
            raise TypeError("db_url should be of type str and in sqlite url format")
        elif re.match("sqlite:\/\/\/.+\.db", db_url) == None:
            raise TypeError("db_url should be of type str and in sqlite url format")
        else:
            self.db_url = db_url

    def get_first_lemma_of(self, to_find):
        # Returns the first instance of a word
        # in the iWeb corpus where
        # the lemma is that word.
        #
        # Thus, searching for "potatoes" will not
        # return a value because the lemma of
        # "potatoes" is "potato"
        if type(to_find) is str:
            db = dataset.connect(self.db_url)
            
            results = db.query("SELECT * FROM entries WHERE lemma LIKE '" + to_find + "' LIMIT 1")
                
            for result in results:
                return Entry(int(result["word_id"]), result["word"], result["lemma"], result["pos"])

            return None
        else:
            raise TypeError("to_find should be of type str")

    def get_first_word_of(self, to_find):
        # Returns the first instance of a word
        # in the iWeb corpus where
        # the word is that word.

        if type(to_find) is str:
            db = dataset.connect(self.db_url)
            
            results = db.query("SELECT * FROM entries WHERE word LIKE '" + to_find + "' LIMIT 1")
                
            for result in results:
                return Entry(int(result["word_id"]), result["word"], result["lemma"], result["pos"])


            return None
        else:
            raise TypeError("to_find should be of type str")

    def get_first_entry_of(self, to_find):
        # Returns the first instance of a word
        # in the iWeb corpus, given either the lemma or word

        if type(to_find) is str:
            lemma = self.get_first_lemma_of(to_find)
            word = self.get_first_word_of(to_find)

            if lemma.word_id < word.word_id:
                return lemma
            elif word.word_id < lemma.word_id:
                return word
            else:
                return None
        else:
            raise TypeError("to_find should be of type str")
