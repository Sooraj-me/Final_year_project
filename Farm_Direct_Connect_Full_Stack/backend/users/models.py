# Farm Direct Connect
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Phone must be 10 digits')]
    )
    email = models.EmailField(unique=True)
    
    # Location fields
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Farmer-specific fields
    farm_name = models.CharField(max_length=100, null=True, blank=True)
    farm_size = models.FloatField(null=True, blank=True, help_text="In acres")
    
    # Profile fields
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, null=True, blank=True)
    
    # Ratings and statistics
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class GramSahayak(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='gram_sahayak')
    location = models.CharField(max_length=100)
    farmers_helped = models.IntegerField(default=0)
    products_listed = models.IntegerField(default=0)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gram_sahayak'
    
    def __str__(self):
        return f"{self.user.username} - {self.status}"