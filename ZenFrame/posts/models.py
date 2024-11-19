from django.conf import settings
from django.db import models
import uuid
from django.utils.text import slugify

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID as primary key
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    caption = models.TextField(blank=True)  # No need for max_length in TextField
    images = models.JSONField(default=list)  # Store image URLs as a JSON array
    location_name = models.CharField(max_length=255, null=True, blank=True)  # Optional field for location name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    # Many-to-Many relationship for likes
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='post_likes',  # Ensure no clashes with other relationships
        through='Like',
        blank=True
    )

    # Many-to-Many relationship for saved posts using the through model
    saved_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='saved_posts',  # Ensure no clashes with other relationships
        through='SavedPost',
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug and self.caption:
            self.slug = slugify(self.caption)
        super().save(*args, **kwargs)


    def __str__(self):
        return f'Post by {self.user.username} - {self.caption[:20]}'

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent the same user liking the same post multiple times

    def __str__(self):
        return f'{self.user.username} liked post {self.post.id}'

class SavedPost(models.Model):
    post = models.ForeignKey(Post, related_name='post_saved', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_saved_posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # Prevent the same user saving the same post multiple times

    def __str__(self):
        return f'{self.user.username} saved post {self.post.id}'
