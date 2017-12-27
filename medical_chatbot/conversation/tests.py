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

    def test_count_frequency_in_list(self):
        liste = ['coucou', "test", "coucou", "testdeux"]
        frequency_dict = self.words_manager.count_frequency_in_list(liste)
        self.assertEqual(frequency_dict, {'testdeux': 1, 'coucou': 2,
                                          'test': 1})


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

    def test_return_tokens_dict(self):
        self.assertEqual({1: ['j', 'ai', 'mal', 'au', 'ventre'],
                          2: ['j', 'ai', 'des', 'maux', 'de', 'têtes'],
                          3: ['j', 'ai', 'très', 'mal', 'au', 'dos']},
                          self.chatbot.return_tokens_dict(
                            self.initial_node.get_all_right_edges())
                        )

    def test_create_inversed_index(self):
        inversed_index = self.chatbot.create_inversed_index(self.initial_node.get_all_right_edges())
        self.assertEqual({'de': [(2, 2)], 'tres': [(3, 1)], 'ventr': [(1, 1)],
                          'au': [(1, 1), (3, 1)], 'mal': [(1, 1), (3, 1)],
                          'têt': [(2, 1)], 'ai': [(1, 1), (2, 1), (3, 1)],
                          'dos': [(3, 1)], 'maux': [(2, 1)],
                          'j': [(1, 1), (2, 1), (3, 1)]},
                          inversed_index)

    def test_get_most_pertinent_message(self):
        a = self.chatbot.get_most_pertinent_message(
            self.test_graph, self.initial_node, Message(text="Bobo au ventre"))
