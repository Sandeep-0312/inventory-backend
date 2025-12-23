from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (JWT handled via custom LoginView)
    path('api/auth/', include('accounts.urls')),

    # Products & Purchases
    path('api/', include('products.urls')),

    # Token refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
