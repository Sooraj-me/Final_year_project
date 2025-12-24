# Farm Direct Connect
from django.db import models

class Conversation(models.Model):
    farmer = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='conversations_as_farmer')
    buyer = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='conversations_as_buyer')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'conversations'
        unique_together = ['farmer', 'buyer', 'product']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Chat: {self.farmer.username} - {self.buyer.username}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username}"