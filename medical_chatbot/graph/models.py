from django.db import models

# Create your models here.


class Graph(models.Model):
    """ Graph which has many nodes and edges.
    A graph is link to a theme (for example : cancer, a liitle sick, etc.)
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return "Graph {0}".format(self.name)

    def get_initial_node(self):
        return Node.objects.filter(graph=self, initial_node=True)[0]


class Node(models.Model):
    """ A node is a chatbot response. It refers to several edges
    """
    text = models.TextField()
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    initial_node = models.BooleanField(default=False)

    def __str__(self):
        return "Node {0} from Graph {1}".format(self.text, self.graph.name)

    def get_all_right_edges(self):
        return Edge.objects.filter(left_node=self)


class Edge(models.Model):
    """ An edge is a user response. It refers to many left nodes and one
    right node
    """
    text = models.TextField()
    left_node = models.ForeignKey(Node, on_delete=models.CASCADE,
                                  related_name="right_edges")
    right_node = models.ForeignKey(Node, on_delete=models.CASCADE,
                                   related_name="left_edges")

    def __str__(self):
        return "Edge {0} between Node {1} and Node {2}".format(
            self.text, self.left_node.text, self.right_node.text)

    def get_right_node(self):
        return self.right_node
