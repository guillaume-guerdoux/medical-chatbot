from django.test import TestCase
from django.urls import reverse

# models
from conversation.models import Message
from conversation.models import Chatbot
from conversation.models import WordsManager
from graph.models import Graph
from graph.models import Node
from graph.models import Edge
# Create your tests here.

# serializers
from conversation.serializers import MessageSerializer


class WordsManagerTests(TestCase):
    def setUp(self):
        self.words_manager = WordsManager()

    def test_string_to_list(self):
        self.assertEqual(["je", "suis", "écarté", "2"],
                         self.words_manager.string_to_list("Je suis écarté 2"))

    def test_string_to_list_apostrophe(self):
        self.assertEqual(["j", "ai", "mal"],
                         self.words_manager.string_to_list("J'ai mal"))

    def test_string_to_list_second_apostrophe(self):
        self.assertEqual(["j", "ai", "mal"],
                         self.words_manager.string_to_list('J"ai mal'))

    def test_lemmatize_french_words(self):
        stem_word = self.words_manager.lemmatize_french_word("voudrais")
        self.assertEqual(stem_word, "voudr")

    def test_lemmatize_french_words_no_lemmatize(self):
        stem_word = self.words_manager.lemmatize_french_word("chocolat")
        self.assertEqual(stem_word, "chocolat")

    def test_lemmatize_french_words_accent(self):
        stem_word = self.words_manager.lemmatize_french_word("écarté")
        self.assertEqual(stem_word, "écart")


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


class ChatBotGetPertinentMessageTests(TestCase):
    def setUp(self):
        self.test_graph = Graph.objects.create(name="test_graph")
        self.test_graph.save()
        self.initial_node = Node.objects.create(
            text="initial_node", graph=self.test_graph, initial_node=True)
        self.initial_node.save()

        self.first_right_node = Node.objects.create(
            text="first_right_node", graph=self.test_graph)
        self.second_right_node = Node.objects.create(
            text="second_right_node", graph=self.test_graph)
        self.third_right_node = Node.objects.create(
            text="third_right_node", graph=self.test_graph)
        self.first_right_node.save()
        self.second_right_node.save()
        self.third_right_node.save()

        self.ventre_edge = Edge.objects.create(
            text='J"ai mal au ventre', left_node=self.initial_node,
            right_node=self.first_right_node)
        self.tete_edge = Edge.objects.create(
            text="J'ai des maux de têtes", left_node=self.initial_node,
            right_node=self.second_right_node)
        self.dos_edge = Edge.objects.create(
            text="J'ai très mal au dos", left_node=self.initial_node,
            right_node=self.third_right_node)

        self.chatbot = Chatbot()

    def test_return_edges_tokens_dict(self):
        self.assertEqual({"jaidemauxdetêt": 2,
                          "jaimalauventr": 1,
                          "jaitresmalaudos": 3},
                         self.chatbot.return_edges_tokens(
                            self.initial_node.get_all_right_edges_by_id_sorted())[1]
                         )

    def test_return_edges_tokens_document_list(self):
        self.assertEqual([['j', 'ai', 'mal', 'au', 'ventr'],
                          ['j', 'ai', 'de', 'maux', 'de', 'têt'],
                          ['j', 'ai', 'tres', 'mal', 'au', 'dos']],
                         self.chatbot.return_edges_tokens(
                            self.initial_node.get_all_right_edges_by_id_sorted())[0]
                         )

    def test_get_most_pertinent_edge_1(self):
        most_pertinent_edge_id = self.chatbot.get_most_pertinent_edge(
            self.test_graph, self.initial_node,
            Message(text="Ca me fait tres mal à la tête"))
        self.assertEqual(most_pertinent_edge_id, 2)

    def test_get_most_pertinent_edge_0(self):
        most_pertinent_edge_id = self.chatbot.get_most_pertinent_edge(
            self.test_graph, self.initial_node,
            Message(text="J'ai mal au ventre quand je mange"))
        self.assertEqual(most_pertinent_edge_id, 1)

    def test_get_most_pertinent_edge_2(self):
        most_pertinent_edge_id = self.chatbot.get_most_pertinent_edge(
            self.test_graph, self.initial_node,
            Message(text="Une douleur dans le dos"))
        self.assertEqual(most_pertinent_edge_id, 3)
