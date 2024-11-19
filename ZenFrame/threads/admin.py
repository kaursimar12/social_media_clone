# thread/admin.py

from django.contrib import admin
from .models import Thread, ThreadLike

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ThreadLike)
class ThreadLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'thread', 'created_at')
    search_fields = ('user__username', 'thread__title')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
