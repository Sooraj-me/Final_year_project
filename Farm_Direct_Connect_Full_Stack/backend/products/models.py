# Farm Direct Connect
from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('grains', 'Grains'),
    )
    
    UNIT_CHOICES = (
        ('kg', 'Kilogram'),
        ('dozen', 'Dozen'),
        ('piece', 'Piece'),
        ('liter', 'Liter'),
    )
    
    farmer = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='kg')
    description = models.TextField()
    
    # Location
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    
    # Inventory
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    
    # Media
    image = models.ImageField(upload_to='products/')
    
    # Ratings
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'state']),
            models.Index(fields=['farmer', 'is_available']),
        ]
    
    def __str__(self):
        return f"{self.product_name} - {self.farmer.farm_name}"


class ProductInventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity_available = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)
    quantity_sold = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_inventory'
    
    def __str__(self):
        return f"Inventory: {self.product.product_name}"