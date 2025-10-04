from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Tag, Post, Comment, Contact, Profile


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 15
    list_max_show_all = 50


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    list_per_page = 15
    list_max_show_all = 50


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_title', 'author', 'categories', 'is_published', 'created_at', 'updated_at', 'display_tags_count', 'display_actions')
    list_filter = ('author', 'tags', 'categories', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title', 'content')
    list_per_page = 15
    list_max_show_all = 30
    filter_horizontal = ('tags',)  # pratique pour ManyToManyField

    def display_tags_count(self, post):
        return len(post.tags.all())

    def display_actions(self, post):
        view_url = reverse("blog-single-post", args=[post.id])

        return format_html(
            '<a class="button" href="{}" target="_blank">View</a>',
            view_url
        )

    def display_title(self, post):
        icon = "✅" if post.is_published else "❌"
        return format_html('{} {}', icon, post.title)

    display_title.short_description = 'Title'
    display_tags_count.short_description = "tags count"
    display_actions.short_description = "Actions"


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'note', 'created_at', 'updated_at')
    list_filter = ('post', 'author', 'created_at')
    search_fields = ('content',)
    list_per_page = 20
    list_max_show_all = 50


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'civility', 'name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at', 'civility')
    list_per_page = 20
    list_max_show_all = 50


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'description')
    search_fields = ('user__username', 'description')
    list_filter = ('user',)
    list_per_page = 20
    list_max_show_all = 50


# Enregistrement dans l’admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Profile, ProfileAdmin)