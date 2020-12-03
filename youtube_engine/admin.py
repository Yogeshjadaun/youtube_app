from django.contrib import admin
from .models import YoutubeVideo, YoutubeApiKey

# Register your models here.
admin.site.register(YoutubeVideo)
admin.site.register(YoutubeApiKey)
