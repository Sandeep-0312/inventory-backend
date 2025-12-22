from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # ✅ Add TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ✅ ADD THIS: Main JWT login endpoint
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Auth (JWT) - accounts app
    path('api/auth/', include('accounts.urls')),
    
    # Products & Purchases - products app
    path('api/', include('products.urls')),
    
    # Token refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]