from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from ..serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    #POST /api/login/ -> {access, refresh} 
    #  Open to anyone (AllowAny) but rate-limited to 10/min via the 'auth' scope.
    # Both admin and regular users log in here — the JWT payload carries the role.

    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

class RegisterView(APIView):
    """
    POST /api/register/
    Public registration — creates a regular user (role='user').
    Primarily for the mobile app; the React dashboard creates users via
    the admin-only POST /api/users/ endpoint instead.
    Rate-limited to 10/min to prevent bot sign-ups.
    """

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            #Return public profile via UserSerializer (no password) 
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)