from django.contrib import admin
from .models import User, Post

class UserAdmin(admin.ModelAdmin):
    # Customization for User model in admin site
    list_display = ('username', 'email', 'is_active', 'date_joined')

class PostAdmin(admin.ModelAdmin):
    # Customization for Post model in admin site
    list_display = ('user', 'content', 'timestamp', 'likes_count')

    def likes_count(self, obj):
        # Custom method to display the number of likes for a Post instance
        return obj.likes.count()

# Register the User model with custom admin class
admin.site.register(User, UserAdmin)

# Register the Post model with custom admin class
admin.site.register(Post, PostAdmin)
