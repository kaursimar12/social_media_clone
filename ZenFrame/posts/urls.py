from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    UpdatePostView,
    DeletePostView,
    toggle_like_post,
    toggle_save_post,
    SavedPostListView,
    SavedPostDetailView
)

urlpatterns = [
    path('api/posts/', PostListView.as_view(), name='post_list'),
    path('api/posts/create/', PostCreateView.as_view(), name='post_create'),
    path('api/posts/<uuid:pk>/update/', UpdatePostView.as_view(), name='post_update'),  # Update endpoint
    path('api/posts/<uuid:pk>/delete/', DeletePostView.as_view(), name='post_delete'),  # Delete endpoint
    path('api/posts/<uuid:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('api/posts/<uuid:id>/like/', toggle_like_post, name='toggle_like_post'),
    path('api/posts/<uuid:id>/save/', toggle_save_post, name='toggle_save_post'),
    path('api/posts/saved/', SavedPostListView.as_view(), name='saved_posts_list'),
    path('api/posts/saved/<uuid:id>/', SavedPostDetailView.as_view(), name='saved_post_detail')
]
