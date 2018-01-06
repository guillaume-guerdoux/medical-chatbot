from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# models
from conversation.models import Message
from conversation.models import Chatbot
from graph.models import Graph
from graph.models import Node

# serializer
from conversation.serializers import MessageSerializer


@api_view(['GET'])
def init_conversation(request, format=None):
    """
    Initialize conversation with chatbot :
        - Choose tree
        - Choose Node
        - Send a first message
    """
    if request.method == 'GET':
        # id_graph = request.POST["pk"]
        if request.user.is_authenticated:
            pass
        else:
            try:
                graph = Graph.objects.all()[0]
            except Graph.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            initial_node = graph.get_initial_node()
            request.session['active_graph'] = graph.id
            request.session['active_node'] = initial_node.id
            welcome_message = Message.objects.create(
                text="Bonjour, que puis-je faire pour vous ?"
            )
            serializer = MessageSerializer(welcome_message)
            return Response(serializer.data)


@api_view(['GET', 'POST'])
def converse(request, format=None):
    """
    Function to discuss with user. User sends his message.
    Chatbot calculate best message to deliver.
    """
    if request.method == 'POST':
        id_graph = request.session.get('active_graph')
        id_node = request.session.get('active_node')
        try:
            graph = Graph.objects.get(pk=id_graph)
        except Graph.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            node = Node.objects.get(pk=id_node)
        except Node.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_message_serializer = MessageSerializer(data=request.data)
        print(user_message_serializer)
        chatbot = Chatbot()
        response_message = Message.objects.create(
            text="TEST"
        )
        serializer = MessageSerializer(response_message)
        return Response(serializer.data)
