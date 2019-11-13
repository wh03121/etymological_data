class Entry:
    word_id = "NA"
    word = "NA"
    lemma = "NA"
    pos = "NA"
    
    def __init__(self, word_id, word, lemma, pos):
        if type(word_id) is int:
            self.word_id = word_id
        else:
            raise TypeError("word_id should be of type int")

        if type(word) is str:
            self.word = word
        else:
            raise TypeError("word should be of type str")

        if type(lemma) is str:
            self.lemma = lemma
        else:
            raise TypeError("lemma should be of type str")

        if type(pos) is str:
            self.pos = pos
        else:
            raise TypeError("pos should be of type str")

    def __str__(self):
        string = str(self.word_id) + ","
        string += self.word + ","
        string += self.lemma + ","
        string += self.pos
        return string
        
        
