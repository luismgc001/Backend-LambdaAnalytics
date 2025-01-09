from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({"error": "Usuario inactivo"}, status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(password):
                return Response({"error": "Contraseña incorrecta"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken.for_user(user)
            return Response({
                "refresh": str(token),
                "access": str(token.access_token),
            })
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        user = User.objects.get(id=pk)
        if request.user == user:
            return Response({"error": "No puedes editarte a ti mismo"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeactivateView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        if request.user == user:
            return Response({"error": "No puedes desactivarte a ti mismo"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        return Response({"message": "Usuario desactivado correctamente"}, status=status.HTTP_200_OK)
