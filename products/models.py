from django.db import models
from django.conf import settings  # DO NOT import CustomUser directly!
from django.utils import timezone  # ADDED for default values

class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    
    # FIX: Add default=timezone.now to avoid migration issues
    created_at = models.DateTimeField(default=timezone.now)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def is_low_stock(self):
        return self.quantity < 10

class Purchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    # USE settings.AUTH_USER_MODEL, not CustomUser!
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # CORRECT
        on_delete=models.CASCADE, 
        related_name='purchases'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Customer details at time of purchase
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_mobile = models.CharField(max_length=15)
    customer_address = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    
    # FIX: Add default=timezone.now to avoid migration issues
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # USE customer_name, not customer.username!
        return f"Purchase #{self.id} - {self.customer_name} - {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Calculate total price before saving
        if not self.total_price:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)