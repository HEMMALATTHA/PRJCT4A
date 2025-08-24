from django.contrib import admin
from .models import Post, Comment, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)  # ✅ Added for autocomplete support

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "created_at")
    list_filter = ("is_published", "categories", "author")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author", "categories")  # ✅ Works now

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("text", "post__title", "user__username")
