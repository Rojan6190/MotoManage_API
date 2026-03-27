# vehicles/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle, Insurance
from .serializers import VehicleSerializer, InsuranceSerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

class VehicleList(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [IsAuthenticated]  # Uncomment when you add authentication

class VehicleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [IsAuthenticated]  # Uncomment when you add authentication

class UserVehicles(generics.ListAPIView):
    """Get all vehicles for a specific user"""
    serializer_class = VehicleSerializer
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Vehicle.objects.filter(owner_id=user_id)

class InsuranceList(generics.ListCreateAPIView):
    """List all insurance policies or create a new one"""
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer

class InsuranceDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an insurance policy"""
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer

class VehicleInsuranceDetail(generics.RetrieveAPIView):
    """Get insurance details for a specific vehicle"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    
    def retrieve(self, request, *args, **kwargs):
        vehicle = self.get_object()
        try:
            insurance = vehicle.insurance  # Uses the OneToOne relation
            serializer = InsuranceSerializer(insurance)
            return Response(serializer.data)
        except Insurance.DoesNotExist:
            return Response(
                {"detail": "No insurance found for this vehicle"},
                status=404
            )


