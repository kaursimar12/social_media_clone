from django.conf import settings
from django.db import models
import uuid

class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_threads', through='ThreadLike')

    def __str__(self):
        return self.title

class ThreadLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='thread_likes')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'thread'], name='unique_thread_like')
        ]

    def __str__(self):
        return f'{self.user} likes {self.thread}'

class Repost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_thread = models.ForeignKey(Thread, related_name='reposts', on_delete=models.CASCADE)
    reposting_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reposts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Repost by {self.reposting_user} of thread {self.original_thread}'
