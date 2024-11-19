from django.contrib import admin
from .models import CustomUser, Follow

class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'bio', 'avatar', 'created_at', 
        'followers_count', 'following_count'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'bio')
    
    def followers_count(self, obj):
        return obj.followers_count()
    followers_count.short_description = 'Followers Count'

    def following_count(self, obj):
        return obj.following_count()
    following_count.short_description = 'Following Count'

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    search_fields = ('follower__username', 'following__username')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow, FollowAdmin)
