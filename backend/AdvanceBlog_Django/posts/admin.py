from django.contrib import admin

# Register your models here.
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'draft', 'publish', 'timestamp', 'updated']
    list_display_links = ['title', 'timestamp']
    list_editable = ['publish']
    list_filter = ['timestamp', 'updated']
    search_fields = ['title', 'content']
    
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)