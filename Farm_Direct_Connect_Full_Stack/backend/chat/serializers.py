# Farm Direct Connect
from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    farmer_name = serializers.CharField(source='farmer.username', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'farmer', 'farmer_name', 'buyer', 'buyer_name', 'product', 
                  'product_name', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']