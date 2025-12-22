# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... other URLs ...
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    # PURCHASE URLs
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('purchases/create/', views.create_purchase, name='create_purchase'),
    path('purchases/update-status/<int:pk>/', views.update_purchase_status, name='update_purchase_status'),  # ← MAKE SURE THIS EXISTS
    
    path('statistics/', views.statistics, name='statistics'),
]