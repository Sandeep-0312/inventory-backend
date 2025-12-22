from rest_framework import serializers
from .models import Product, Purchase

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Purchase
        fields = '__all__'
        read_only_fields = ['customer', 'total_price', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set the logged-in user as customer
        validated_data['customer'] = self.context['request'].user
        validated_data['customer_name'] = validated_data['customer'].get_full_name() or validated_data['customer'].username
        validated_data['customer_email'] = validated_data['customer'].email
        
        # Calculate total price
        product = validated_data['product']
        validated_data['total_price'] = product.price * validated_data['quantity']
        
        return super().create(validated_data)