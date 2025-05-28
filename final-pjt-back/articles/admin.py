
from django.contrib import admin
from .models import (
    Article,
    Comment,
    ArticleScrap

)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created_at')
    search_fields = ('content',)


@admin.register(ArticleScrap)
class ArticleScrapAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', )
    search_fields = ('user__username', 'article__title')
