from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    #POST /api/login/ -> {access, refresh}  
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            #Return public profile via UserSerializer (no password) 
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)