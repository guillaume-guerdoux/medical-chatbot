from django.test import TestCase
from django.urls import reverse
# models
from conversation.models import Message
from graph.models import Graph
from graph.models import Node
# Create your tests here.

# serializers
from conversation.serializers import MessageSerializer


class MessageModelTests(TestCase):
    """ Test only message model fields and functions
    """
    def test_message_creation(self):
        message = Message.objects.create(text="test_message")
        self.assertEqual(message.text, "test_message")


class MessageSerializerTests(TestCase):
    def setUp(self):
        self.test_message = Message.objects.create(text="test_message")
        self.datetime = self.test_message.datetime

    def test_message_to_serializer(self):
        """ TODO : test datetime.
        """
        serializer = MessageSerializer(self.test_message)
        self.assertEqual(serializer.data['text'], 'test_message')

    def test_serializer_to_message(self):
        serializer = MessageSerializer(data={'text': 'test_graph'})
        self.assertTrue(serializer.is_valid)


class InitConversationTests(TestCase):
    def setUp(self):
        self.test_graph = Graph.objects.create(name="test_graph")
        self.test_graph.save()
        self.initial_node = Node.objects.create(
            text="initial_node", graph=self.test_graph, initial_node=True)
        self.initial_node.save()

    def test_init_conversation(self):
        response = self.client.get(reverse('conversation:init_conversation',
                                           kwargs={'pk': self.test_graph.pk}))
        self.assertEqual(response.data['text'],
                         "Bonjour, que puis-je faire pour vous ?")
        session = self.client.session
        self.assertEqual(session.get('active_graph'), 1)
        self.assertEqual(session.get('active_node'), 1)
