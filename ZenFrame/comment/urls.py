from django.urls import path
from .views import (
    CommentCreateView, 
    PostCommentsListView,  
    ThreadCommentsListView,  
    CommentRepliesListView, 
    CommentDeleteView,
    ToggleLikeCommentView,
)

urlpatterns = [
    # Post comment-related URLs
    path('api/posts/<uuid:post_id>/comments/', CommentCreateView.as_view(), name='post-comment-create'),
    path('api/posts/<uuid:post_id>/comments/<uuid:parent_id>/', CommentCreateView.as_view(), name='post-reply-create'),
    path('api/posts/<uuid:post_id>/comments/list/', PostCommentsListView.as_view(), name='post-comments-list'),
    
    # Thread comment-related URLs
    path('api/threads/<uuid:thread_id>/comments/', CommentCreateView.as_view(), name='thread-comment-create'),
    path('api/threads/<uuid:thread_id>/comments/<uuid:parent_id>/', CommentCreateView.as_view(), name='thread-reply-create'),
    path('api/threads/<uuid:thread_id>/comments/list/', ThreadCommentsListView.as_view(), name='thread-comments-list'),
    
    # Comment replies for both posts and threads
    path('api/comments/<uuid:comment_id>/replies/list/', CommentRepliesListView.as_view(), name='comment-replies-list'),
    
    # Comment deletion for both posts and threads
    path('api/comments/<uuid:comment_id>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # Like/Unlike a comment
    path('api/comments/<uuid:comment_id>/like/', ToggleLikeCommentView.as_view(), name='comment-like-toggle'),
]
