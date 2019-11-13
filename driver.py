from DataProcessing import *
from iWebHandler import *

'''
    https://dataset.readthedocs.io/en/latest/

    data.tsv downloaded from http://www1.icsi.berkeley.edu/~demelo/etymwn

    data.tsv data harvested from Wiktionary

    iweb_lexicon.txt from https://www.corpusdata.org/iweb_samples.asp, lexicon link
    
'''
            
if __name__ == '__main__':
    ih = iWebHandler("sqlite:///iweb.db")
    dh = DataHandler("sqlite:///db.db")

    word1 = "eng: new"
    word2 = "eng: neo-"
    word_one = dh.find_first_of_word(word1)
    word_two = dh.find_first_of_word(word2)

    '''derv = dh.get_related_of(word1)[0]
    branch = []
    
    for der in derv:
        branch.append(ComplexWord.convert(der, dh))


    tree = Branch(branch)
    match = tree.check(tree, dh, word_two, 0, 30)
    print(match[0].word_str() + " matched " + word_one.word_str() + " after " + str(match[1]) + " times")
'''
    ancestor = dh.find_ancestor(word_one, word_two, 30)

    print(str(ancestor[0]))
    print()
    print(str(ancestor[1]))
    
