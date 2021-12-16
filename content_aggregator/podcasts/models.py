
from django.db import models
from django.urls import reverse


class FeedChannel(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    url = models.URLField()

    def get_absolute_url(self):
        return reverse('feed_channel_view', args=[str(self.id)])

    def __str__(self):
        return f"{self.name}: {self.url}"


class Episode(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    podcast_name = models.ForeignKey(FeedChannel, on_delete=models.CASCADE)
    guid = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.podcast_name}: {self.title}"
