from django.contrib import admin
from .models import Product, Purchase, PurchaseEvent

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']

class PurchaseEventInline(admin.TabularInline):
    model = PurchaseEvent
    extra = 0
    readonly_fields = ['timestamp', 'created_by']
    fields = ['event_type', 'event_message', 'timestamp', 'created_by']

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'get_product_name', 'quantity', 'total_price', 'status', 'tracking_number', 'created_at']
    inlines = [PurchaseEventInline]
    
    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product Name'
    
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'product__name', 'tracking_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('customer', 'product', 'quantity', 'total_price', 'status')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_mobile', 'customer_address')
        }),
        ('Tracking Information', {
            'fields': ('tracking_number', 'delivery_partner', 'estimated_delivery', 'actual_delivery')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )

class PurchaseEventAdmin(admin.ModelAdmin):
    list_display = ['purchase', 'event_type', 'event_message', 'timestamp', 'created_by']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['purchase__id', 'event_message']
    readonly_fields = ['timestamp']

admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseEvent, PurchaseEventAdmin)
