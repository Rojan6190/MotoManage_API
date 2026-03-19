# vehicles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    #Vehicle URLS
    path('vehicles/', views.VehicleList.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', views.VehicleDetail.as_view(), name='vehicle-detail'),
    path('users/<int:user_id>/vehicles/', views.UserVehicles.as_view(), name='user-vehicles'), 
    

    #Insurance URLS
    path('insurances/', views.InsuranceList.as_view(), name='insurance-list'),
    path('insurances/<int:pk>/', views.InsuranceDetail.as_view(), name='insurance-detail'),
    path('vehicles/<int:pk>/insurance/', views.VehicleInsuranceDetail.as_view(), name='vehicle-insurance'),

]