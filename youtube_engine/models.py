from django.db import models

# Create your models here.


class BaseMode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class YoutubeApiKey(BaseMode):
    FAILED = "failed"
    SUCCESS = "success"
    KEY_STATUS = (
        (FAILED, "FAILED"),
        (SUCCESS, "SUCCESS"),
    )
    status = models.CharField(max_length=200, blank=True, choices=KEY_STATUS, default=SUCCESS)
    key = models.CharField(max_length=200, blank=True)


class YoutubeVideo(BaseMode):
    video_id = models.CharField(max_length=200, blank=True, null=True)
    channel_id = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    channel_title = models.CharField(max_length=500, blank=True, null=True)
    thumbnails_url = models.URLField(max_length=300)
    publishing_date = models.DateTimeField()

    def __str__(self):
        return str(self.id) + self.title

    class Meta:
        db_table = "youtube_video"
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['description']),
            models.Index(fields=['video_id']),
        ]
        verbose_name = "YoutubeVideo"
        verbose_name_plural = "YoutubeVideos"
