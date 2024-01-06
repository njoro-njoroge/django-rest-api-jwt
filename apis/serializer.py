from rest_framework import serializers
from account.models import Client
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email', 'store_name', 'password']
        read_only_fields = ['id']  # exclude  id from updates


class ClientLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    store_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Add custom claims
#         token['email'] = user.email
#
#         return token


# User = get_user_model()


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#
#         # Add custom claims
#         data['email'] = self.user.email
#         data['id'] = self.user.id
#
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#
#         return data
