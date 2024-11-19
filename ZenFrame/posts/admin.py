from django.contrib import admin
from .models import Post, Like

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at')
    search_fields = ('user__username', 'caption')
    list_filter = ('created_at',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)

admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
