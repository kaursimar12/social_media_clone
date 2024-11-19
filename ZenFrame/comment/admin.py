from django.contrib import admin
from .models import Comment, CommentLike

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'post', 'thread', 'parent_comment', 'created_at', 'updated_at', 'likes_count', 'replies_count')
    list_filter = ('created_at', 'post', 'thread')
    search_fields = ('content', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    def likes_count(self, obj):
        return obj.likes.count()

    def replies_count(self, obj):
        return obj.replies.count()

class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'comment__content')

admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
