from rest_framework import serializers
from conversation.models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('text', 'datetime', 'final_message')
