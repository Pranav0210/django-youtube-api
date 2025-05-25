from django.db import models

# Create your models here.
class YouTubeVideo(models.Model):
    video_id = models.CharField(max_length=100, unique=True)
    title = models.TextField()
    description = models.TextField(blank=True)
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()

    class Meta:
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['title']),
            models.Index(fields=['description']),
        ]
        ordering = ['-published_at']