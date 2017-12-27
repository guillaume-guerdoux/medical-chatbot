from django.db import models
import re
from collections import defaultdict

from nltk.stem.snowball import FrenchStemmer

# import models
from graph.models import Graph
from graph.models import Node
from graph.models import Edge

# Create your models here.

stop_words = []


class WordsManager():

    def string_to_list(self, string):
        """ Transform a string in a words list with accent and number.
        """
        return string.replace("'", " ").replace('"', " ").lower().split()

    def filter_common_words(self, word):
        if word not in stop_words:
            return True
        else:
            return False

    def lemmatize_french_word(self, french_word):
        french_stemmer = FrenchStemmer()
        return french_stemmer.stem(french_word)

    def count_frequency_in_list(self, liste):
        w = dict()
        for element in liste:
            w[element] = liste.count(element)
        return w


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
        return edges_tokens_dict

    def create_inversed_index(self, edges):
        """ From a queryset of edges (with text), we create an inversed
        index in real time.
        Input : Edge queryset
        Output : defaultdict : "word1" : [[edge_id, frequency], [edge__id_2, frequency]], "word2" ...
        """
        frequency_dict = dict()
        inversed_index = defaultdict(list)
        for key, value in self.return_tokens_dict(edges).items():
            new_list = []
            for element in value:
                if self.words_manager.filter_common_words(element):
                    lemmatized_element = \
                        self.words_manager.lemmatize_french_word(element)
                    new_list.append(lemmatized_element)
            frequency_dict = self.words_manager.count_frequency_in_list(
                new_list
            )
            for element in list(set(new_list)):
                inversed_index[element].append((key, frequency_dict[element]))
        return inversed_index

    def get_most_pertinent_message(self, graph, node, message):
        return 1
