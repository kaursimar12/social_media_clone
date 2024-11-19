from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Thread, ThreadLike, Repost

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ThreadLike
        fields = ['id', 'user', 'thread', 'created_at']

class RepostSerializer(serializers.ModelSerializer):
    reposting_user = UserSerializer(read_only=True)

    class Meta:
        model = Repost
        fields = ['id', 'original_thread', 'reposting_user', 'created_at']

class ThreadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    repost_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'like_count', 'liked_by_user', 'repost_count']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'like_count', 'liked_by_user', 'repost_count']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def get_like_count(self, obj):
        return ThreadLike.objects.filter(thread=obj).count()

    def get_liked_by_user(self, obj):
        user = self.context['request'].user
        return ThreadLike.objects.filter(thread=obj, user=user).exists()

    def get_repost_count(self, obj):
        return Repost.objects.filter(original_thread=obj).count()
