from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import json


def product_list(request):
    products = list(Product.objects.values())
    return JsonResponse({'products': products})


@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        Product.objects.create(
            name=data['name'],
            quantity=data['quantity'],
            price=data['price']
        )
        return JsonResponse({'message': 'Product added successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        product.name = data['name']
        product.quantity = data['quantity']
        product.price = data['price']
        product.save()
        return JsonResponse({'message': 'Product updated successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
