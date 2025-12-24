# Farm Direct Connect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from products.models import Product, ProductInventory
from notifications.tasks import send_notification

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return Order.objects.filter(farmer=user)
        return Order.objects.filter(buyer=user)
    
    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            items_data = serializer.validated_data['items']
            total_amount = 0
            farmer = None
            
            order = Order.objects.create(
                buyer=request.user,
                order_number=self.generate_order_number(),
                total_amount=0,
                delivery_address=serializer.validated_data['delivery_address'],
                delivery_state=serializer.validated_data['delivery_state'],
                delivery_district=serializer.validated_data['delivery_district']
            )
            
            for item in items_data:
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']
                subtotal = product.price * quantity
                total_amount += subtotal
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                )