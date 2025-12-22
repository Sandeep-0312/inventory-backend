from django.urls import path
from .views import RegisterView, CurrentUserView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # JWT login
    path('me/', CurrentUserView.as_view(), name='current_user'),
]