# Farm Direct Connect
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_purchase', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    farmer_name = serializers.CharField(source='farmer.farm_name', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'buyer_name', 'farmer_name', 'total_amount', 
                  'status', 'payment_status', 'delivery_address', 'delivery_state', 
                  'delivery_district', 'items', 'created_at', 'delivered_at']
        read_only_fields = ['id', 'order_number', 'created_at']


class OrderCreateSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField())
    )
    delivery_address = serializers.CharField()
    delivery_state = serializers.CharField()
    delivery_district = serializers.CharField()