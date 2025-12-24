# Farm Direct Connect
from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('order_placed', 'Order Placed'),
        ('order_confirmed', 'Order Confirmed'),
        ('order_shipped', 'Order Shipped'),
        ('order_delivered', 'Order Delivered'),
        ('payment_received', 'Payment Received'),
        ('new_message', 'New Message'),
        ('product_review', 'Product Review'),
    )
    
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    related_order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)
    related_product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification: {self.title}"