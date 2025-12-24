# Farm Direct Connect
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='reviews_given')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        unique_together = ['product', 'buyer', 'order']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review: {self.product.product_name} - {self.rating}⭐"