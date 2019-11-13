from DataProcessing import DataHandler, ComplexWord
from Word import *

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
            if i == cutoff:
                return None
            else:
                cutoff += 1
                next_step = []
                for word in self.words:
                    if word.is_related_to(check, dh):
                        i += 1
                        return [word, i, words]
                    derivatives = dh.get_related_of(word.word_str())[0]
                    for derivative in derivatives:
                        i += 1
                        next_step.append(ComplexWord.convert(derivative, dh))
                self.check(next_step, dh, check, i, cutoff)
            
