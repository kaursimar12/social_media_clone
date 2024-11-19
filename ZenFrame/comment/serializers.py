from rest_framework import serializers
from .models import Comment, CommentLike
from django.contrib.auth import get_user_model

User = get_user_model()

# Serializer for User details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Add any additional fields you want to expose

# Serializer for Comment
class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    replies_count = serializers.IntegerField(source='replies.count', read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'thread', 'parent_comment', 'created_at', 'updated_at', 'likes_count', 'replies_count', 'is_liked_by_user']
        extra_kwargs = {
            'post': {'required': False},
            'thread': {'required': False},
            'parent_comment': {'required': False},
        }

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            liked = obj.likes.filter(user=request.user).exists()
            return liked
        return False

    def create(self, validated_data):
        # Automatically assign the user from the context instead of expecting it in the request
        user = self.context['request'].user
        # Remove 'user' from validated_data if it exists to avoid conflict
        validated_data.pop('user', None)
        return Comment.objects.create(user=user, **validated_data)

# Serializer for CommentLike
class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Use nested serializer to include user details

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']
