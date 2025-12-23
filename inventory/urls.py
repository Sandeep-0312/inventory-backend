# inventory/urls.py (main urls.py)
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ADD THIS!
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Your existing custom auth (keep both if needed)
    path('api/auth/', include('accounts.urls')),

    # Products & Purchases
    path('api/', include('products.urls')),
]