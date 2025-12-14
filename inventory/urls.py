from django.contrib import admin
from django.urls import path, include
from products.views import product_list, add_product, edit_product, delete_product

urlpatterns = [
    path('admin/', admin.site.urls),

    # Products
    path('products/', product_list),
    path('products/add/', add_product),
    path('products/edit/<int:pk>/', edit_product),
    path('products/delete/<int:pk>/', delete_product),

    # Auth (JWT)
    path('auth/', include('accounts.urls')),
]
