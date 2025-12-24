# Farm Direct Connect
from rest_framework import serializers
from .models import Payment, Transaction

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'payment_method', 'razorpay_order_id', 
                  'status', 'created_at']
        read_only_fields = ['id', 'razorpay_order_id', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'user_name', 'amount', 'transaction_type', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']