from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from apps.user.views import CustomTokenObtainPairView

urlpatterns = [
    # auth
    path("login", CustomTokenObtainPairView.as_view()),
    path("token/refresh", jwt_views.TokenRefreshView.as_view()),
]
