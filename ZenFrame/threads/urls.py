from django.urls import path
from .views import (
    ThreadListView,
    ThreadCreateView,
    ThreadRetrieveView,
    ThreadUpdateView,
    ThreadDeleteView,
    ThreadLikeToggleView,
    RepostThreadView
)

urlpatterns = [
    # Endpoints for threads
    path('api/threads/', ThreadListView.as_view(), name='thread-list'),
    path('api/threads/create/', ThreadCreateView.as_view(), name='thread-create'),
    path('api/threads/<uuid:pk>/', ThreadRetrieveView.as_view(), name='thread-retrieve'),
    path('api/threads/<uuid:pk>/update/', ThreadUpdateView.as_view(), name='thread-update'),
    path('api/threads/<uuid:pk>/delete/', ThreadDeleteView.as_view(), name='thread-delete'),
    path('api/threads/<uuid:thread_id>/like/', ThreadLikeToggleView.as_view(), name='thread-like-toggle'),
    path('api/threads/<uuid:thread_id>/repost/', RepostThreadView.as_view(), name='thread-repost'),
]
