from rest_framework import serializers
from .models import Post, SavedPost, Like
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    saved_count = serializers.SerializerMethodField()
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)  # Expect a list of image files
    images_urls = serializers.SerializerMethodField(read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()
    is_saved_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 
            'user', 
            'caption', 
            'location_name', 
            'images',
            'images_urls', 
            'created_at', 
            'likes_count', 
            'saved_count', 
            'is_liked_by_user', 
            'is_saved_by_user',
            'slug'
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_saved_count(self, obj):
        return obj.saved_by.count()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')  # Now this will correctly get the request
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def get_is_saved_by_user(self, obj):
        request = self.context.get('request')  # Now this will correctly get the request
        if request and request.user.is_authenticated:
            return obj.saved_by.filter(id=request.user.id).exists()
        return False
    def get_images_urls(self, obj):
        return obj.images  # Return the stored image URLs

    def create(self, validated_data):
        images = validated_data.pop('images')  # Get the list of images
        post = Post.objects.create(**validated_data)  # Create the post instance

        # Process images and save URLs
        image_urls = []
        for image in images:
            file_name = default_storage.save(image.name, image)  # Save the image
            image_url = default_storage.url(file_name)  # Get the URL
            image_urls.append(image_url)

        post.images = image_urls  # Assign the list of image URLs to the post
        post.save()  # Save the post instance

        return post

class SavedPostSerializer(serializers.ModelSerializer):
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = SavedPost
        fields = ['post', 'created_at', 'is_saved']

    def get_is_saved(self, obj):
        request = self.context.get('request')
        return obj.user == request.user  # Check if the user is the one who saved the post

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user  # Set user from request
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['post', 'created_at', 'is_liked']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        return obj.user == request.user  # Check if the user is the one who liked the post

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user  # Set user from request
        return super().create(validated_data)
