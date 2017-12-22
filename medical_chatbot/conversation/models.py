from django.db import models

# import models
from graph.models import Graph
from graph.models import Node
from graph.models import Edge
# Create your models here.


class Message(models.Model):
    text = models.TextField()
    datetime = models.DateTimeField(auto_now=True)


class Chatbot():
    """ This chatbot can analyse user answer and ask pertinent
    questions. It uses graph, nodes and edge to go through a 'real'
    conversation. NLTK is used to use NLP.
    """
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
