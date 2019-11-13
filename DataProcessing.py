from Word import *
import dataset
import re
from Entry import *

class ComplexWord:
    language_of_word = "NA"
    word = "NA"
    relation = "NA"
    language_of_related = "NA"
    related_word = "NA"

    colon = re.compile(r"\s*:\s*")

    def __init__(self, obj):
        if type(obj) != Word:
            raise TypeError("obj should be of type Word")
        else:
            # Split word by regex and store in separate data
            splitWord = self.colon.split(obj.word)
            self.language_of_word = splitWord[0]
            self.word = splitWord[1]

            # Split relation by regex and store
            self.relation = self.colon.split(obj.relation)[1]

            # Split related word by regex and store in separate data
            splitRelatedWord = self.colon.split(obj.related)
            self.language_of_related = splitRelatedWord[0]
            self.related_word = splitRelatedWord[1]

    def __eq__(self, other):
        if type(other) == Word:
            new_word = ComplexWord(other)
            if new_word.__eq__(self):
                return True
            else:
                return False
        elif type(other) == ComplexWord:
            if self.language_of_word == other.language_of_word:
                if self.word == other.word:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __str__(self):
        string = self.language_of_word + ","
        string += self.word + ","
        string += self.relation + ","
        string += self.language_of_related + ","
        string += self.related_word
        return string

    def is_prefix(self):
        if re.match("^[^-]+\-$", self.word):
            return True
        else:
            return False

    def is_suffix(self):
        if re.match("^\-[^-]+$", self.word):
            return True
        else:
            return False

    def is_infix(self):
        if re.match("^\-[^-]+\-$", self.word):
            return True
        else:
            return False

    def is_affix(self):
        if self.is_prefix() or self.is_suffix() or self.is_infix():
            return True
        else:
            return False

    def word_str(self):
        return self.language_of_word + ": " + self.word

    def is_related_to(self, word, dh):
        if type(word) is not ComplexWord:
            raise TypeError("word must be of type ComplexWord")
        elif type(dh) is not DataHandler:
            raise TypeError("dh must be of type DataHandler")
        else:
            return dh.are_related(self, word)

    @staticmethod
    def convert(string, dh):
        if re.match(".{2,}:\s*.+", string) is None:
            raise TypeError("string should contain an ISO 639-3 code, a colon, and then the word")
        elif type(dh) is not DataHandler:
            raise TypeError("dh should be of type DataHandler")
        else:
            return dh.find_first_of_word(string)


class DataHandler:
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

    def find_first_of_word(self, to_find):
        # returns the first entry of the
        # requested word
        # in ComplexWord form
        if type(to_find) != str:
            raise TypeError("to_find should be of type str")
        elif re.match(".{2,}:\s*.+", to_find) is None:
            raise TypeError(
                "to_find should contain an ISO 639-3 code, a colon, and then the word")
        else:
            db = dataset.connect(self.db_url)
            table = db["words"]
            result = table.find_one(word=to_find)
            if result is None:
                return None
            else:
                return ComplexWord(Word(result['word'], result['relation'], result['related']))

    def find_word(self, to_find):
        # Returns an array of ComplexWords
        # Containing every entry for the given word
        if type(to_find) != str:
            raise TypeError("to_find should be of type str")
        elif re.match(".{2,}:\s*.+", to_find) is None:
            raise TypeError("to_find should contain an ISO 639-3 code, a colon, and then the word")
        else:
            db = dataset.connect(self.db_url)
            table = db["words"]

            table_results = table.find(word=to_find)

            results = []

            for result in table_results:
                results.append(ComplexWord(Word(re.sub(r'\n+', '', result['word']), re.sub(r'\n+', '', result['relation']), re.sub(r'\n+', '', result['related']))))

            return results

    def get_all_suffixes(self, language):
        # Returns an array with all of the suffixes
        # of the given language
        if type(language) != str:
            raise TypeError("language should be of type str")
        elif re.match(".{3,}", language) is None:
            raise TypeError("language should be an ISO 639-3 code")
        else:
            db = dataset.connect(self.db_url)
            table = db["words"]

            table_results = db.query("SELECT * FROM words WHERE word LIKE '" + language + ": -%'")

            results = []

            for result in table_results:
                word = ComplexWord(Word(re.sub(r'\n+', '', result['word']), re.sub(r'\n+', '', result['relation']), re.sub(r'\n+', '', result['related'])))
                results.append(word)

            return results

    def print_all_suffixes(self, language):
        if type(language) != str:
            raise TypeError("language should be of type str")
        elif re.match(".{3,}", language) is None:
            raise TypeError("language should be an ISO 639-3 code")
        else:
            results = self.get_all_suffixes(language)
            for result in results:
                print(result)

    def get_all_prefixes(self, language):
        # Returns an array with all of the
        # prefixes of the given language
        if type(language) != str:
            raise TypeError("language should be of type str")
        elif re.match(".{3,}", language) is None:
            raise TypeError("language should be an ISO 639-3 code")
        else:
            db = dataset.connect(self.db_url)
            table = db["words"]

            table_results = db.query("SELECT * FROM words WHERE word LIKE '" + language + ": %-'")

            results = []

            for result in table_results:
                if re.match("^" + language + ":\s[^-]+-$", result["word"]):
                    word = ComplexWord(Word(re.sub(r'\n+', '', result['word']), re.sub(r'\n+', '', result['relation']), re.sub(r'\n+', '', result['related'])))
                    results.append(word)

            return results

    def print_all_prefixes(self, language):
        if type(language) != str:
            raise TypeError("language should be of type str")
        elif re.match(".{3,}", language) is None:
            raise TypeError("language should be an ISO 639-3 code")
        else:
            results = self.get_all_prefixes(language)
            for result in results:
                print(result)

    def get_all_infixes(self, language):
        # Returns an array containing
        # All of the infixes of the given language
        if type(language) != str:
            raise TypeError("language should be of type str")
        elif re.match(".{3,}", language) is None:
            raise TypeError("language should be an ISO 639-3 code")
        else:
            db = dataset.connect(self.db_url)
            table = db["words"]

            table_results = db.query("SELECT * FROM words WHERE word LIKE '" + language + ": %-'")

            results = []

            for result in table_results:
                if re.match("^" + language + ":\s\-[^-]+\-$", result["word"]):
                    word = ComplexWord(Word(re.sub(r'\n+', '', result['word']), re.sub(r'\n+', '', result['relation']), re.sub(r'\n+', '', result['related'])))
                    results.append(word)

            return results

    def print_all_infixes(self, language):
        if type(language) != str:
            raise TypeError("language should be of type str")
        elif re.match(".{3,}", language) is None:
            raise TypeError("language should be an ISO 639-3 code")
        else:
            results = self.get_all_infixes(language)
            for result in results:
                print(result)

    def get_all_affixes(self, language):
        # Returns an array containing all of the affixes
        # in the given language
        if type(language) != str:
            raise TypeError("language should be of type str")
        elif re.match(".{3,}", language) is None:
            raise TypeError("language should be an ISO 639-3 code")
        else:
            prefixes = self.get_all_prefixes(language)
            suffixes = self.get_all_suffixes(language)
            infixes = self.get_all_infixes(language)

            results = []

            results.append(prefixes[:])
            del prefixes
            results.append(suffixes[:])
            del suffixes
            results.append(infixes[:])
            del infixes

            return results

    def print_all_affixes(self, language):
        if type(language) != str:
            raise TypeError("language should be of type str")
        elif re.match(".{3,}", language) is None:
            raise TypeError("language should be an ISO 639-3 code")
        else:
            results = self.get_all_affixes(language)
            for result in results:
                print(result)

    def get_related_of(self, to_find):
        # Returns an array consisting of two arrays
        # The first array (return[0]) is the words that are related
        # The second array (return[1]) is the relations those words have
        #   to the given word.
        if type(to_find) != str:
            raise TypeError("to_find should be of type str")
        elif re.match(".{2,}:\s*.+", to_find) is None:
            raise TypeError("to_find should contain an ISO 639-3 code, a colon, and then the word")
        else:
            table_results = self.find_word(to_find)
            related = []
            relation = []
            
            for result in table_results:
                related.append(result.language_of_related + ": " + result.related_word)
                relation.append(result.relation)

            return [related, relation]

    def print_related_of(self, to_find):
        if type(to_find) != str:
            raise TypeError("to_find should be of type str")
        elif re.match(".{2,}:\s*.+", to_find) is None:
            raise TypeError("to_find should contain an ISO 639-3 code, a colon, and then the word")
        else:
            table_results = self.get_related_of(to_find)[0]

            for result in table_results:
                print(result)

    def are_related(self, word, other_word):
        # Returns an array
        # The array[0] is True or False, if they're related
        # array[1] indicates the word that is the origin
        # array[2] is the relation
        # array[3] indicates derived word
        # Thus word=potato
        # other_word=potatoes
        # are_related(word, other_word) = [True, potatoes, is_derived_from, potato]
        # Otherwise, returns None
        
        if type(word) is ComplexWord and type(other_word) is ComplexWord:
            related_first = self.get_related_of(word.word_str())
            related_second = self.get_related_of(other_word.word_str())

            related_to_first = related_first[0]
            related_to_second = related_second[0]

            relations_to_first = related_first[1]
            relations_to_second = related_second[1]
            
            word_string = word.word_str()
            other_word_string = other_word.word_str()

            i = 0
            while i < len(related_to_first):
                if related_to_first[i] == other_word_string:
                    return [True, word.word, relations_to_first[i], other_word.word]
                i += 1

            i = 0
            while i < len(related_to_second):
                if related_to_second[i] == word_string:
                    return [True, other_word.word, relations_to_second[i], word.word]
                i += 1

            return None
        else:
            raise TypeError("word and other_word should be of type ComplexWord")

    def is_derived_from(self, word, other_word):
        # Returns True if other_word is etymologically
        # derived from word
        if type(word) is ComplexWord and type(other_word) is ComplexWord:
            related_to_first = self.get_related_of(word.word_str())
            related_to_second = self.get_related_of(other_word.word_str())

            word_string = word.word_str()
            other_word_string = other_word.word_str()

            i = 0
            while i < len(related_to_first[0]):
                if related_to_first[0][i] == other_word_string:
                    if related_to_first[1][i] == "etymological_origin_of":
                        return True
                i += 1

            return False
        else:
            raise TypeError("word and other_word should be of type ComplexWord")

    def Entry_to_ComplexWord(self, entry):
        # Converts custom Entry type to ComplexWord
        # All inputs must be in English
        
        if type(entry) is not Entry:
            raise TypeError("entry should be of type Entry")
        else:
            return self.find_first_of_word(ComplexWord.convert("eng: " + entry.lemma))

    def find_ancestor(self, word_one, word_two, cutoff=30):
        # Returns the common ancestor of word_one and word_two
        # Stops searching after the cutoff number of branches
        # Returns none if there is no result
        
        if type(word_one) is not ComplexWord:
            raise TypeError("word_one should be of type ComplexWord")
        elif type(word_two) is not ComplexWord:
            raise TypeError("word_two should be of type ComplexWord")
        else:
            if word_one.is_related_to(word_two, self):
                return [word_one, 1]
            else:
                derv = self.get_related_of(word_one.word_str())[0]
                branch = []
                
                for der in derv:
                    branch.append(ComplexWord.convert(der, self))
                    
                tree = Branch(branch)
                match = tree.check(tree, self, word_two, 0, cutoff)
                
                return [match[0], cutoff-match[3]]

class Branch:
    words = "NA"
    
    def __init__(self, words):
        if type(words) is not list:
            raise TypeError("words should be of type array")
        else:
            for word in words:
                if type(word) is not ComplexWord:
                    raise TypeError("words should be of type ComplexWord")
            self.words = words
            
    def __str__(self):
        return self.words.__str__()

    def check(self, words, dh, check, i, cutoff):
        # Returns an array given the found result
        # Otherwise, it searches all of the related words from before.
        if type(words) is not Branch:
            raise TypeError("words should be of type Branch")
        elif type(dh) is not DataHandler:
            raise TypeError("dh should be of type DataHandler")
        elif type(check) is not ComplexWord:
            raise TypeError("check should be of type Complex Word")
        else:
            if cutoff == 0:
                return None
            else:
                next_step = []
                for word in self.words:
                    if word.is_related_to(check, dh):
                        i += 1
                        return [word, i, words, cutoff]
                    derivatives = dh.get_related_of(word.word_str())[0]
                    for derivative in derivatives:
                        i += 1
                        next_step.append(dh.find_first_of_word(derivative))
                self.check(Branch(next_step), dh, check, i, cutoff-1)
