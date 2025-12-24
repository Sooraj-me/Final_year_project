# Farm Direct Connect
from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'buyer_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'order', 'rating', 'comment']