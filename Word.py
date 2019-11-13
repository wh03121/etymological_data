class Word:
    word = "NA"
    relation = "NA"
    related = "NA"

    def __init__(self, word, relation, related):
        if type(word) == str:
            self.word = word
        else:
            raise TypeError("word should be of type str")
        if type(relation) == str:
            self.relation = relation
        else:
            raise TypeError("relation should be of type str")
        if type(related) == str:
            self.related = related
        else:
            raise TypeError("related should be of type str")

    def __eq__(self, other):
        if type(other) == Word:
            if self.word == other.word:
                return True
            else:
                return False
        elif type(other) == str:
            if self.word[5:] == other:
                return True
            elif self.word == other:
                return True
            else:
                return False
        else:
            raise TypeError("passed value other should be of type Word or str")

    def __str__(self):
        return self.word + "," + self.relation + "," + self.related
