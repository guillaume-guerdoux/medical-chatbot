from django.db import models
import re
from collections import defaultdict

import numpy as np
from math import log
import gensim

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
        return string.replace("'", " ").replace('"', " ").replace(',',' ').replace('.',' ').lower().split()

    def filter_common_words(self, word):
        if word not in stop_words:
            return True
        else:
            return False

    def lemmatize_french_word(self, french_word):
        french_stemmer = FrenchStemmer()
        return french_stemmer.stem(french_word)

    def normalize_string(self, string):
        """ Transform a string to a normalize list for nlp
        Input : 'coucou les gars'
        Output ['coucou', 'le', 'gar']
        """
        token_list = []
        for token in self.string_to_list(string):
            if self.filter_common_words(token):
                lemmatized_element = \
                    self.lemmatize_french_word(token)
                token_list.append(lemmatized_element)
        return token_list

    def list_to_string(self, liste):
        return ''.join(map(str, liste))


class Message(models.Model):
    text = models.TextField()
    datetime = models.DateTimeField(auto_now=True)
    final_message = models.BooleanField(default=False)


class Chatbot(models.Model):
    """ This chatbot can analyse user answer and ask pertinent
    questions. It uses graph, nodes and edge to go through a 'real'
    conversation. NLTK is used to use NLP.
    """
    words_manager = WordsManager()

    def return_edges_tokens(self, edges):
        """ Create a dictionary with edge's id as key and tokenize sentence
        as value
        input : Edges
        output {1 : ['Je', 'mange'], 2 ...}
        """
        edges_tokens_dict = dict()
        document_list = []
        for edge in edges:
            token_list = self.words_manager.normalize_string(edge.get_text())
            edges_tokens_dict[self.words_manager.list_to_string(token_list)] = edge.pk
            document_list.append(token_list)
        return document_list, edges_tokens_dict

    def get_most_pertinent_edge(self, graph, node, message):
        edges = node.get_all_right_edges_by_id_sorted()
        document_list, edges_tokens_dict = self.return_edges_tokens(edges)

        # Create corpus with all text of all edges / Use model TFIDF then LSI
        dictionary = gensim.corpora.Dictionary(document_list)
        corpus = [dictionary.doc2bow(document) for document in document_list]

        tfidf = gensim.models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]

        lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary,
                                     num_topics=100)
        corpus_lsi = lsi[corpus_tfidf]

        # Treat query
        query = message.text
        normalized_query = self.words_manager.normalize_string(query)
        vec_bow = dictionary.doc2bow(normalized_query)
        vec_lsi = lsi[vec_bow]

        index = gensim.similarities.MatrixSimilarity(lsi[corpus])
        sims = index[vec_lsi]
        sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        most_pertinent_document = document_list[sorted_sims[0][0]]
        edge_id = edges_tokens_dict[self.words_manager.list_to_string(most_pertinent_document)]
        return edge_id
