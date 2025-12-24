# Farm Direct Connect
from rest_framework import serializers
from .models import Product, ProductInventory

class ProductSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.farm_name', read_only=True)
    farmer_phone = serializers.CharField(source='farmer.phone', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'price', 'unit', 'description', 
                  'state', 'district', 'quantity', 'is_available', 'image', 
                  'average_rating', 'total_reviews', 'farmer_name', 'farmer_phone', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'average_rating', 'total_reviews', 'created_at', 'updated_at']


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'category', 'price', 'unit', 'description', 
                  'state', 'district', 'quantity', 'is_available', 'image']


class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = ['id', 'quantity_available', 'quantity_reserved', 'quantity_sold', 'last_updated']
        read_only_fields = ['id', 'last_updated']