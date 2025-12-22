from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Product, Purchase

# ================= PERMISSION CLASSES =================
class IsAdminUser:
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsCustomerUser:
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

# Helper function to check if user is admin
def check_admin(request):
    if not request.user.is_authenticated:
        return False
    # If using your CustomUser model with role field
    if hasattr(request.user, 'role'):
        return request.user.role == 'admin'
    # Fallback for superusers
    return request.user.is_superuser

# ================= EXISTING PRODUCT VIEWS (UPDATED) =================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    products = Product.objects.all().values()
    return Response({"products": list(products)})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    # Check if user is admin
    if not check_admin(request):
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
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
    # Check if user is admin
    if not check_admin(request):
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    data = request.data
    product = get_object_or_404(Product, id=pk)
    product.name = data.get('name', product.name)
    product.quantity = data.get('quantity', product.quantity)
    product.price = data.get('price', product.price)
    product.save()
    return Response({"message": "Product updated"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    # Check if user is admin
    if not check_admin(request):
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    product = get_object_or_404(Product, id=pk)
    product.delete()
    return Response({"message": "Product deleted"})

# ================= NEW PURCHASE VIEWS =================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def purchase_list(request):
    """
    Admin: See all purchases
    Customer: See only their purchases
    """
    user = request.user
    
    if check_admin(request):
        # Admin sees all
        purchases = Purchase.objects.all()
    else:
        # Customer sees only theirs
        purchases = Purchase.objects.filter(customer=user)
    
    # Convert to list of dictionaries
    purchases_data = []
    for purchase in purchases:
        purchases_data.append({
            'id': purchase.id,
            'customer_name': purchase.customer_name,
            'customer_email': purchase.customer_email,
            'customer_mobile': purchase.customer_mobile,
            'customer_address': purchase.customer_address,
            'product_id': purchase.product.id,
            'product_name': purchase.product.name,
            'quantity': purchase.quantity,
            'unit_price': float(purchase.product.price),  # Get from product
            'total_price': float(purchase.total_price),
            'status': purchase.status,
            'notes': purchase.notes,
            'created_at': purchase.created_at.isoformat(),
        })
    
    return Response({"purchases": purchases_data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_purchase(request):
    """
    Create a new purchase (both admin and customer can create purchases)
    """
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_email', 'customer_mobile', 
                          'customer_address', 'product_id', 'quantity']
        
        for field in required_fields:
            if field not in data:
                return Response(
                    {"error": f"{field} is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Get product
        try:
            product = Product.objects.get(id=data['product_id'])
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check availability
        try:
            quantity = int(data['quantity'])
            if quantity <= 0:
                return Response(
                    {"error": "Quantity must be positive"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return Response(
                {"error": "Quantity must be a valid number"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if product.quantity < quantity:
            return Response(
                {"error": f"Only {product.quantity} units available"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate total price
        total_price = product.price * quantity
        
        # Create purchase - NO unit_price field!
        purchase = Purchase.objects.create(
            customer=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price,  # Calculated total price
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            customer_mobile=data['customer_mobile'],
            customer_address=data['customer_address'],
            notes=data.get('notes', ''),
        )
        
        # Reduce product quantity
        product.quantity -= quantity
        product.save()
        
        return Response({
            "message": "Purchase created successfully",
            "purchase_id": purchase.id,
            "total_price": float(purchase.total_price),
            "unit_price": float(product.price),  # From product, for info only
            "product_name": product.name
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        import traceback
        print("Purchase creation error:", str(e))
        print("Traceback:", traceback.format_exc())
        
        return Response(
            {"error": f"Server error: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_purchase_status(request, pk):
    """
    Update purchase status (admin only)
    """
    # Check if user is admin
    if not check_admin(request):
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    data = request.data
    status_value = data.get('status')
    
    if not status_value:
        return Response(
            {"error": "Status is required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        purchase = Purchase.objects.get(id=pk)
        purchase.status = status_value
        purchase.save()
        
        return Response({"message": "Purchase status updated"})
        
    except Purchase.DoesNotExist:
        return Response(
            {"error": "Purchase not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistics(request):
    """
    Get statistics (admin only)
    """
    # Check if user is admin
    if not check_admin(request):
        return Response(
            {"error": "Admin access required"}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    from django.db.models import Sum, Count
    from datetime import datetime, timedelta
    
    # Calculate statistics
    total_products = Product.objects.count()
    total_purchases = Purchase.objects.count()
    
    total_revenue = Purchase.objects.aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # Recent purchases (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_purchases = Purchase.objects.filter(
        created_at__gte=thirty_days_ago
    ).count()
    
    # Low stock products
    low_stock = Product.objects.filter(quantity__lt=10).count()
    
    return Response({
        'total_products': total_products,
        'total_purchases': total_purchases,
        'total_revenue': float(total_revenue),
        'recent_purchases': recent_purchases,
        'low_stock': low_stock,
    })