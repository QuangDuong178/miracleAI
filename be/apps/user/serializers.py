from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.models import User


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD
