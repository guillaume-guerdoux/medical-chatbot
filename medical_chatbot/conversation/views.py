from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# models
from conversation.models import Message
from graph.models import Graph
from graph.models import Node

# serializer
from conversation.serializers import MessageSerializer


@api_view(['GET'])
def init_conversation(request, pk, format=None):
    """
    Initialize conversation with chatbot :
        - Choose tree
        - Choose Node
        - Send a first message
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            pass
        else:
            try:
                graph = Graph.objects.get(pk=pk)
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
