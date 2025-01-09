from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario creado correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                print("error: Usuario inactivo")
                return Response({"error": "Usuario inactivo"}, status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(password):
                print("error: Contraseña incorrecta")
                return Response({"error": "Contraseña incorrecta"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken.for_user(user)
            return Response({
                "refresh": str(token),
                "access": str(token.access_token),
                "role": user.role,
            })
        except User.DoesNotExist:
            print("error Usuario no encontrado")
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Confirma que el usuario está autenticado
        if not user.is_authenticated:
            return Response({"error": "Usuario no autenticado"}, status=401)

        # Agrega logs para verificar el usuario
        print(f"Usuario autenticado: {user.email}")

        # Devuelve la lista de usuarios
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        if request.user == user:
            return Response({"error": "No puedes desactivarte a ti mismo"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        return Response({"message": "Usuario desactivado correctamente"}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "role": user.role,
        })
    
class TestJWTView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Funciona correctamente."})