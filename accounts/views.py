from .models import Account
from .serializers import AccountSerializer, AccountLoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings


class AccountView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class AccountLoginView(generics.CreateAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountLoginSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
        
#         if serializer.is_valid():
#             username = serializer.validated_data.get('username')
#             password = serializer.validated_data.get('password')
            
#             user = authenticate(username=username, password=password)
            
#             if user is not None:
#                 jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#                 jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

#                 payload = jwt_payload_handler(user)
#                 token = jwt_encode_handler(payload)

#                 is_admin = user.is_superuser

#                 return Response({
#                     'token': token,
#                     'is_admin': is_admin,
#                 }, status=status.HTTP_200_OK)

#         return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)