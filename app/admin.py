from django.contrib import admin
from .models import Post, BlogComment

admin.site.site_header = "coDinG Admin"
admin.site.site_title = "coDinG Admin Panel"
admin.site.index_title = "Welcome to coDinG Admin Panel"

admin.site.register(BlogComment)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('tinyInject.js',)