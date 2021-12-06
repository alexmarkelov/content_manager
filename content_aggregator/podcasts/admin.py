from django.contrib import admin
from .models import Episode, FeedChannel


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("podcast_name", "title", "pub_date")


@admin.register(FeedChannel)
class FeedChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "url")
