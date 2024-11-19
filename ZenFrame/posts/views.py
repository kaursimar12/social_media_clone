from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, SavedPost
from .serializers import PostSerializer, SavedPostSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
import os
from django.conf import settings
from rest_framework.views import APIView
from django.core.files.storage import default_storage


# List posts
class PostListView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

    # Override the method to pass the request context to the serializer
    def get_serializer_context(self):
        return {'request': self.request}

# Create posts
class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update a specific post
class UpdatePostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({'error': 'You do not have permission to edit this post.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
# Retrieve a specific post
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        return post

# Delete a specific post
class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({'error': 'You do not have permission to delete this post.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)

# Toggle like/unlike a post
@api_view(['POST'])
def toggle_like_post(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user

    if not user.is_authenticated:
        return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    if user in post.likes.all():
        # If the user already liked the post, unlike it
        post.likes.remove(user)
        return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
    else:
        # Otherwise, like the post
        post.likes.add(user)
        return Response({'message': 'Post liked'}, status=status.HTTP_200_OK)

# Toggle save/unsave a post
@api_view(['POST'])
def toggle_save_post(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user

    if not user.is_authenticated:
        return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    saved_post = SavedPost.objects.filter(post=post, user=user).first()

    if saved_post:
        # If the post is already saved, unsave it
        saved_post.delete()
        return Response({'message': 'Post unsaved'}, status=status.HTTP_200_OK)
    else:
        # Otherwise, save the post
        SavedPost.objects.create(post=post, user=user)
        return Response({'message': 'Post saved'}, status=status.HTTP_201_CREATED)

# List saved posts
class SavedPostListView(generics.ListAPIView):
    serializer_class = SavedPostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return all posts saved by the current authenticated user
        return SavedPost.objects.filter(user=self.request.user).select_related('post')

# Retrieve a specific saved post by the post ID
class SavedPostDetailView(generics.RetrieveAPIView):
    serializer_class = SavedPostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the specific saved post of the authenticated user by post ID
        post_id = self.kwargs['id']
        saved_post = get_object_or_404(SavedPost, post_id=post_id, user=self.request.user)
        return saved_post
