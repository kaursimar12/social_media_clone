from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import CreateUserView, UserListView, UserDetailView, UserUpdateView, UserDeleteView,  toggle_follow

urlpatterns = [
    path('api/users/', UserListView.as_view(), name='user-list'), 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get access and refresh tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),              # List all users
    path('api/users/create/', CreateUserView.as_view(), name='user-create'),   # Create a new user
    path('api/users/<uuid:pk>/', UserDetailView.as_view(), name='user-detail'),# Retrieve a user by ID
    path('api/users/<uuid:pk>/update/', UserUpdateView.as_view(), name='user-update'),  # Update a user's profile
    path('api/users/<uuid:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),  # Delete a user
    path('api/users/<uuid:user_id>/toggle_follow/', toggle_follow, name='toggle-follow'),
]