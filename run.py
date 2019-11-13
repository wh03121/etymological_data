import cherrypy
from DataProcessing import *
from iWebHandler import *
import codecs
import os
import re

class Website(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def about(self):
        return open('about.html')

    @cherrypy.expose
    def related(self, word_one, word_two):
        string = codecs.open('front_stub.html', 'r').read()

        print(word_one + word_two)

        if not(re.match("^[a-zA-Z\sÀ-ž]+$", word_one)):
            string += "<h3>First word does not match the pattern. Try again.</h3>"
            string += codecs.open('back_stub.html').read()
            return string
        if not(re.match("^[a-zA-Z\sÀ-ž]+$", word_two)):
            string += "<h3>Second word does not match the pattern. Try again.</h3>"
            string += codecs.open('back_stub.html').read()
            return string

        dh = DataHandler("sqlite:///db.db")
        word_one = dh.find_first_of_word("eng: " + word_one)
        word_two = dh.find_first_of_word("eng: " + word_two)
        
        if word_one is None:
            string += "<h3>The first word you entered wasn't found.</h3>"
            string += codecs.open('back_stub.html', 'r').read()
            return string
        elif word_two is None:
            string += "<h3>The second word you entered wasn't found.</h3>"
            string += codecs.open('back_stub.html', 'r').read()
            return string

        if word_one.__eq__(word_two):
            string += "<h3>These words are the same!</h3>"
            string += word_one.word_str()[4:] + " is the same word as " + word_two.word_str()[4:]
            string += codecs.open('back_stub.html', 'r').read()
            return string
        
        related = word_one.is_related_to(word_two, dh)

        if related is not None:
            string += "<h3>They're related!</h3>\n"
            string += "<p>The word '" + related[1] + "'"
            if related[2] == "has_derived_form":
                string += " is syntactically the same as "
            elif related[2] == "etymology":
                string += " is derived from "
            elif related[2] == "etymologically_related":
                string += " is etymologically related to "
            elif related[2] == "etymological_origin_of":
                string += " is the root of "
            elif related[2] == "is_derived_from":
                string += " is a syntactic derivation of "
            string += "'" + related[3] + "'</p>"
            string += codecs.open('back_stub.html', 'r').read()
            return string
        else:
            string += "<h3>They're not related</h3><p>"
            string += word_one.word_str()[4:] + " is not related to " + word_two.word_str()[4:]
            string += codecs.open('back_stub.html', 'r').read()
            return string

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': '',
    }
}
cherrypy.quickstart(Website(), '/', config=config)
