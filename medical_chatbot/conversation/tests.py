from django.test import TestCase

# models
from conversation.models import Graph
from conversation.models import Node
from conversation.models import Edge

# Create your tests here.


class GraphModelTests(TestCase):
    """ Test only graph model fields and functions
    """
    def test_graph_creation(self):
        graph = Graph.objects.create(name="test_graph")
        graph.save()
        graph = Graph.objects.get(name="test_graph")
        self.assertEqual(graph.name, "test_graph")
        self.assertEqual(graph.__str__(), "Graph test_graph")


class NodeModelTests(TestCase):
    """ Test only node model fields and functions
    """
    def setUp(self):
        self.test_graph = Graph.objects.create(name="test_graph")
        self.test_graph.save()
        self.first_left_node = Node.objects.create(
            text="first_left_node", graph=self.test_graph)
        self.second_left_node = Node.objects.create(
            text="second_left_node", graph=self.test_graph)
        self.first_right_node = Node.objects.create(
            text="first_right_node", graph=self.test_graph)
        self.second_right_node = Node.objects.create(
            text="second_right_node", graph=self.test_graph)
        self.first_left_node.save()
        self.second_left_node.save()
        self.first_right_node.save()
        self.second_right_node.save()

        self.center_node = Node.objects.create(
            text="center_node", graph=self.test_graph)
        self.first_left_edge = Edge.objects.create(
            text="first_left_edge", left_node=self.first_left_node,
            right_node=self.center_node)
        self.second_left_edge = Edge.objects.create(
            text="second_left_edge", left_node=self.second_left_node,
            right_node=self.center_node)
        self.first_right_edge = Edge.objects.create(
            text="first_right_edge", left_node=self.center_node,
            right_node=self.first_right_node)
        self.second_right_edge = Edge.objects.create(
            text="second_right_edge", left_node=self.center_node,
            right_node=self.second_right_node)
        self.center_node.save()
        self.first_left_edge.save()
        self.second_left_edge.save()
        self.first_right_edge.save()
        self.second_right_edge.save()

    def test_node_creation(self):
        node = Node.objects.create(text="Quels sont vos symptômes ?",
                                   graph=self.test_graph)
        node.save()
        node = Node.objects.get(text="Quels sont vos symptômes ?")
        self.assertEqual(node.text, "Quels sont vos symptômes ?")
        self.assertEqual(node.graph, self.test_graph)
        self.assertEqual(node.__str__(),
                         "Node Quels sont vos symptômes ? from "
                         "Graph test_graph")

    def test_get_all_right_edges(self):
        self.assertEqual(set(self.center_node.get_all_right_edges()),
                         {self.first_right_edge, self.second_right_edge})


class EdgeModelTests(TestCase):
    """ Test only edge model fields and functions
    """
    def setUp(self):
        self.test_graph = Graph.objects.create(name="test_graph")
        self.left_node = Node.objects.create(text="Quels sont vos symptômes ?",
                                             graph=self.test_graph)
        self.right_node = Node.objects.create(text="Depuis combien de temps",
                                              graph=self.test_graph)

    def test_edge_creation(self):
        edge = Edge.objects.create(text="Mal au ventre",
                                   left_node=self.left_node,
                                   right_node=self.right_node)
        edge.save()
        edge = Edge.objects.get(text="Mal au ventre")
        self.assertEqual(edge.text, "Mal au ventre")
        self.assertEqual(edge.left_node, self.left_node)
        self.assertEqual(edge.right_node, self.right_node)
        self.assertEqual(edge.__str__(),
                         "Edge Mal au ventre between Node Quels sont vos "
                         "symptômes ? and Node Depuis combien de temps")
