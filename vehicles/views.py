# vehicles/views.py

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import Vehicle, Insurance
from .serializers import VehicleSerializer, InsuranceSerializer
from core.permissions import IsAdmin, IsOwnerOrAdmin


# ── ADMIN VIEWS (React dashboard) ────────────────────────────────────────────

class VehicleList(generics.ListCreateAPIView):
    """
    Admin only.
    GET  /api/vehicles/   → list ALL vehicles across all users
    POST /api/vehicles/   → create vehicle for any user (owner set in request body)
    """
    queryset           = Vehicle.objects.select_related('owner').all()
    serializer_class   = VehicleSerializer
    permission_classes = [IsAdmin]
    parser_classes     = [MultiPartParser, FormParser]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'admin'


class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin only.
    GET/PUT/PATCH/DELETE /api/vehicles/<pk>/
    """
    queryset           = Vehicle.objects.select_related('owner').all()
    serializer_class   = VehicleSerializer
    permission_classes = [IsAdmin]
    parser_classes     = [MultiPartParser, FormParser]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'admin'


class UserVehiclesAdmin(generics.ListAPIView):
    """
    Admin only.
    GET /api/users/<user_id>/vehicles/
    Lists all vehicles belonging to a specific user.
    Used by the React dashboard's UserVehicles page.
    """
    serializer_class   = VehicleSerializer
    permission_classes = [IsAdmin]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'admin'

    def get_queryset(self):
        return Vehicle.objects.filter(owner_id=self.kwargs['user_id'])


class InsuranceList(generics.ListCreateAPIView):
    """
    Admin only.
    GET  /api/insurances/   → list all insurance policies
    POST /api/insurances/   → create a policy
    """
    queryset           = Insurance.objects.select_related('vehicle__owner').all()
    serializer_class   = InsuranceSerializer
    permission_classes = [IsAdmin]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'admin'


class InsuranceDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin only.
    GET/PUT/PATCH/DELETE /api/insurances/<pk>/
    """
    queryset           = Insurance.objects.select_related('vehicle__owner').all()
    serializer_class   = InsuranceSerializer
    permission_classes = [IsAdmin]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'admin'


class VehicleInsuranceDetail(generics.RetrieveAPIView):
    """
    Admin only.
    GET /api/vehicles/<pk>/insurance/   → get insurance for a specific vehicle
    """
    queryset           = Vehicle.objects.all()
    serializer_class   = VehicleSerializer
    permission_classes = [IsAdmin]
    throttle_classes   = [ScopedRateThrottle]
    throttle_scope     = 'admin'

    def retrieve(self, request, *args, **kwargs):
        vehicle = self.get_object()
        try:
            serializer = InsuranceSerializer(vehicle.insurance)
            return Response(serializer.data)
        except Insurance.DoesNotExist:
            return Response(
                {"detail": "No insurance found for this vehicle."},
                status=status.HTTP_404_NOT_FOUND,
            )


# ── MOBILE VIEWS ─────────────────────────────────────────────────────────────

class MyVehicleList(APIView):
    """
    Mobile app.
    GET  /api/mobile/vehicles/        → list own vehicles
    POST /api/mobile/vehicles/        → add a vehicle (owner auto-set to request.user)
    """
    permission_classes = [IsOwnerOrAdmin]
    parser_classes     = [MultiPartParser, FormParser]

    def get(self, request):
        vehicles = Vehicle.objects.filter(owner=request.user)
        return Response(VehicleSerializer(vehicles, many=True).data)

    def post(self, request):
        # Force owner to the authenticated user — mobile users can't set owner themselves
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyVehicleDetail(APIView):
    """
    Mobile app.
    GET/PATCH/DELETE /api/mobile/vehicles/<pk>/
    Only the vehicle owner (or an admin) can access.
    """
    permission_classes = [IsOwnerOrAdmin]
    parser_classes     = [MultiPartParser, FormParser]

    def _get_own_vehicle(self, request, pk):
        """Fetch vehicle and enforce object-level permission."""
        vehicle = get_object_or_404(Vehicle, pk=pk)
        self.check_object_permissions(request, vehicle)
        return vehicle

    def get(self, request, pk):
        vehicle = self._get_own_vehicle(request, pk)
        return Response(VehicleSerializer(vehicle).data)

    def patch(self, request, pk):
        vehicle = self._get_own_vehicle(request, pk)
        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        vehicle = self._get_own_vehicle(request, pk)
        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyVehicleInsurance(APIView):
    """
    Mobile app.
    GET /api/mobile/vehicles/<pk>/insurance/
    A user can only view insurance for their own vehicle.
    """
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request, pk):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        self.check_object_permissions(request, vehicle)
        try:
            serializer = InsuranceSerializer(vehicle.insurance)
            return Response(serializer.data)
        except Insurance.DoesNotExist:
            return Response(
                {"detail": "No insurance found for this vehicle."},
                status=status.HTTP_404_NOT_FOUND,
            )