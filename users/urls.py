from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
     # Auth
    path('register/',       views.RegisterView.as_view(),  name='register'),
    path('login/',          views.LoginView.as_view(),      name='login'),
    path('token/refresh/',  TokenRefreshView.as_view(),     name='token-refresh'),

    #Users
    path('users/', views.UserList.as_view(), name="user-list"),
    path('users/<int:pk>',views.UserDetail.as_view(), name="user-detail"),
]
