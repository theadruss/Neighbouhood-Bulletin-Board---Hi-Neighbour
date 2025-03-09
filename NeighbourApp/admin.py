from django.contrib import admin
from .models import CustomUser  # Import your custom user model
from .models import Post

admin.site.register(CustomUser)  # Register the model

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'timestamp')
