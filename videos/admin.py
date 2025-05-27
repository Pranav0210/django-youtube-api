from django.contrib import admin

from .models import YouTubeVideo

@admin.register(YouTubeVideo)
class YouTubeVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "description")
    search_fields = ("title", "description")
    list_filter = ("published_at",)
    ordering = ("-published_at",)