from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .models import Comment, CommentLike
from .serializers import CommentSerializer, CommentLikeSerializer
from posts.models import Post
from threads.models import Thread
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

# Toggle like/unlike a comment
class ToggleLikeCommentView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user
        like, created = CommentLike.objects.get_or_create(user=user, comment=comment)

        if not created:
            like.delete()
            return Response({"message": "Comment unliked."}, status=status.HTTP_200_OK)
        
        return Response({"message": "Comment liked."}, status=status.HTTP_201_CREATED)

# Create a comment (for post or thread)
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        user = self.request.user  # Get the user from the authenticated request
        post_id = self.kwargs.get('post_id')
        thread_id = self.kwargs.get('thread_id')
        parent_comment_id = self.kwargs.get('parent_id')

        parent_comment = get_object_or_404(Comment, id=parent_comment_id) if parent_comment_id else None

        if post_id:
            post = get_object_or_404(Post, id=post_id)
            serializer.save(user=user, post=post, parent_comment=parent_comment)
        elif thread_id:
            thread = get_object_or_404(Thread, id=thread_id)
            serializer.save(user=user, thread=thread, parent_comment=parent_comment)
        else:
            raise PermissionDenied("A comment must be associated with either a post or a thread.")

# List comments for a post
class PostCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post=post, parent_comment__isnull=True)

    def get_serializer_context(self):
        return {'request': self.request}

# List comments for a thread
class ThreadCommentsListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        thread = get_object_or_404(Thread, id=thread_id)
        return Comment.objects.filter(thread=thread, parent_comment__isnull=True)

    def get_serializer_context(self):
        return {'request': self.request}

# List replies to a comment
class CommentRepliesListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        parent_comment = get_object_or_404(Comment, id=comment_id)
        return Comment.objects.filter(parent_comment=parent_comment)

# Delete a comment
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        comment_id = self.kwargs['comment_id']
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this comment.")
        return comment
