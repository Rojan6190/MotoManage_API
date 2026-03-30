# vehicles/urls.py

from django.urls import path
from . import views

urlpatterns = [

    # ── Admin: full vehicle management (React dashboard) ──────────────────
    path('vehicles/', views.VehicleList.as_view(),name='vehicle-list'),
    path('vehicles/<int:pk>/', views.VehicleDetail.as_view(),name='vehicle-detail'),
    path('users/<int:user_id>/vehicles/', views.UserVehiclesAdmin.as_view(),name='user-vehicles-admin'),
    path('vehicles/<int:pk>/insurance/', views.VehicleInsuranceDetail.as_view(),name='vehicle-insurance'),

    # ── Admin: insurance management ───────────────────────────────────────
    path('insurances/', views.InsuranceList.as_view(),   name='insurance-list'),
    path('insurances/<int:pk>/', views.InsuranceDetail.as_view(), name='insurance-detail'),

    # ── Mobile: own vehicles ──────────────────────────────────────────────
    path('mobile/vehicles/', views.MyVehicleList.as_view(),      name='my-vehicle-list'),
    path('mobile/vehicles/<int:pk>/', views.MyVehicleDetail.as_view(),    name='my-vehicle-detail'),
    path('mobile/vehicles/<int:pk>/insurance/', views.MyVehicleInsurance.as_view(), name='my-vehicle-insurance'),
]