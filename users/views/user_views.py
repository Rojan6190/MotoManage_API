from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..models import User
from ..serializers import UserSerializer


class UserList(APIView):

    def get(self, request):
        """GET /api/users/  →  list all users"""
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

    def post(self, request):
        """POST /api/users/  →  create user from dashboard (admin use)"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):

    def get(self, request, pk):
        """GET /api/users/<pk>"""
        user = get_object_or_404(User, pk=pk)
        return Response(UserSerializer(user).data)

    def put(self, request, pk):
        """PUT /api/users/<pk>  →  full update"""
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """PATCH /api/users/<pk>  →  partial update"""
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """DELETE /api/users/<pk>"""
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    #Or we could have used generics with fewer code that does the same thing:
 # from rest_framework import generics

# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer