from django.contrib import admin
from .models import Product, Purchase

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'get_product_name', 'quantity', 'total_price', 'status', 'created_at']
    
    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product Name'
    
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)