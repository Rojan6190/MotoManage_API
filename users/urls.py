# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [

    # ── Auth (open to everyone) ────────────────────────────────────────────
    path('register/',      views.RegisterView.as_view(), name='register'),
    path('login/',         views.LoginView.as_view(),    name='login'),
    path('token/refresh/', TokenRefreshView.as_view(),   name='token-refresh'),

    # ── Admin: user management (React dashboard) ──────────────────────────
    path('users/',          views.UserList.as_view(),   name='user-list'),
    path('users/<int:pk>/',  views.UserDetail.as_view(), name='user-detail'),

    # ── Mobile: self-profile ───────────────────────────────────────────────
    path('mobile/profile/', views.MyProfile.as_view(),  name='my-profile'),

    # user deactivate and restore
    path('users/deactivated/', views.DeactivatedUserList.as_view(), name='deactivated-users'),
    path('users/<int:pk>/restore/', views.RestoreUser.as_view(), name='restore-user'),
]