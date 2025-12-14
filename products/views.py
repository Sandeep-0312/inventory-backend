from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    products = Product.objects.all().values()
    return Response({"products": list(products)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    data = request.data
    Product.objects.create(
        name=data['name'],
        quantity=data['quantity'],
        price=data['price']
    )
    return Response({"message": "Product added"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_product(request, pk):
    data = request.data
    product = Product.objects.get(id=pk)
    product.name = data['name']
    product.quantity = data['quantity']
    product.price = data['price']
    product.save()
    return Response({"message": "Product updated"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    Product.objects.get(id=pk).delete()
    return Response({"message": "Product deleted"})
