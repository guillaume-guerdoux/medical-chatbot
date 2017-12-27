from django.db import models
import re

from nltk.stem.snowball import FrenchStemmer

# import models
from graph.models import Graph
from graph.models import Node
from graph.models import Edge

# Create your models here.


class WordsManager():
    def string_to_list(self, string):
        """ Transform a string in a words list with accent and number.
        """
        return string.replace("'", " ").replace('"', " ").split()

    def lemmatize_french_word(self, french_word):
        french_stemmer = FrenchStemmer()
        return french_stemmer.stem(french_word)


class Message(models.Model):
    text = models.TextField()
    datetime = models.DateTimeField(auto_now=True)


class Chatbot(models.Model):
    """ This chatbot can analyse user answer and ask pertinent
    questions. It uses graph, nodes and edge to go through a 'real'
    conversation. NLTK is used to use NLP.
    """
    words_manager = WordsManager()

    def return_tokens_dict(self, edges):
        edges_tokens_dict = dict()
        for edge in edges:
            edges_tokens_dict[edge.pk] = self.words_manager.string_to_list(
                edge.get_text()
            )
        print(edges_tokens_dict)

    def create_inversed_index(self, edges):
        """ From a queryset of edges (with text), we create an inversed
        index in real time.
        Input : Edge queryset
        Output : defaultdict : "word1" : [[edge_id, frequency], [edge__id_2, frequency]], "word2" ...
        """

    def get_most_pertinent_message(self, graph, node, message):
        return 1
