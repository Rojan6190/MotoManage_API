# users/views/user_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from django.shortcuts import get_object_or_404

from ..models import User
from ..serializers import UserSerializer

# Import from wherever you placed permissions.py
# If you put it in core/permissions.py:  from core.permissions import IsAdmin, IsSelfOrAdmin
# If you put it in users/permissions.py: from .permissions import IsAdmin, IsSelfOrAdmin
from core.permissions import IsAdmin, IsSelfOrAdmin


# ── ADMIN VIEWS (React dashboard) ────────────────────────────────────────────

class UserList(APIView):
    """
    Admin only.
    GET  /api/users/   → list all users
    POST /api/users/   → create a user from the dashboard
                         (no password field — admin creates accounts without one,
                          user sets password via a separate flow, or you can add
                          a password field to UserSerializer later)
    """
    permission_classes = [IsAdmin]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'admin'

    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        return Response(UserSerializer(users, many=True).data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Admin only.
    GET    /api/users/<pk>   → fetch one user
    PUT    /api/users/<pk>   → full update
    PATCH  /api/users/<pk>   → partial update
    DELETE /api/users/<pk>   → delete user
    """
    permission_classes = [IsAdmin]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'admin'

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return Response(UserSerializer(user).data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── MOBILE VIEWS ─────────────────────────────────────────────────────────────

class MyProfile(APIView):
    """
    Mobile app — authenticated user's own profile.
    GET   /api/mobile/profile/   → read own profile
    PATCH /api/mobile/profile/   → update own profile
    """
    permission_classes = [IsSelfOrAdmin]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)