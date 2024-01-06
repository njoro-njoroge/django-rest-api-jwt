from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import ClientSerializer, ClientLoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password, check_password
from account.models import Client
from django.contrib.auth import authenticate


@api_view(['POST'])
def register(request):
    serializer = ClientSerializer(data=request.data)

    if serializer.is_valid():
        # Check if email already exists
        email = serializer.validated_data['email']
        if Client.objects.filter(email__iexact=email).exists():
            return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if store name already exists
        store_name = serializer.validated_data['store_name']
        if Client.objects.filter(store_name__iexact=store_name).exists():
            return Response({'message': 'Store name already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Hash the password before saving
        password = serializer.validated_data['password']
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password

        # Save the user with the hashed password
        serializer.save()

        return Response({'message': 'Submitted successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Failed to save', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = ClientLoginSerializer(data=request.data)
    if serializer.is_valid():
        store_name = serializer.validated_data.get('store_name', None)
        email = serializer.validated_data.get('email', None)
        password = serializer.validated_data['password']

        # Use authenticate for password validation
        user = None

        # Try authentication using email
        if email:
            user = authenticate(request, email=email, password=password)

        # If email authentication failed, try store_name
        if not user and store_name:
            try:
                # make store_name case-insensitive
                user = Client.objects.filter(store_name__iexact=store_name).first()
            except Client.DoesNotExist:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # If store_name authentication failed or not provided, try both store_name and email
        if not user and store_name and email:
            try:
                user = Client.objects.get(store_name=store_name, email=email)
            except Client.DoesNotExist:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user is not None and check_password(password, user.password):
            # Password is valid, generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Additional user details from Client model
            client_details = {
                'access_token': access_token,
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_number,
                'email': user.email,
                'store_name': user.store_name
            }

            return Response(client_details)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
