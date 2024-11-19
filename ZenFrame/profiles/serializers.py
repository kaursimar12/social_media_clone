from rest_framework import serializers
from .models import CustomUser, Follow

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name']

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'bio', 'avatar', 'created_at', 'followers', 'following',
            'followers_count', 'following_count'
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers(self, obj):
        followers = obj.followers.all()
        return UserSimpleSerializer(followers, many=True).data

    def get_following(self, obj):
        following = obj.following.all()
        return UserSimpleSerializer(following, many=True).data