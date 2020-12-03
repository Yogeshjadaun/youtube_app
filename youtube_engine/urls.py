from django.urls import path

from .views import YoutubeVideoView, YoutubeVideoSearchView, YoutubeVideoDashboardView


app_name = "youtube_engine"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('youtube-videos/dashboard/', YoutubeVideoDashboardView.as_view()),
    path('youtube-videos/search/', YoutubeVideoSearchView.as_view()),
    path('youtube-videos/', YoutubeVideoView.as_view()),
    ]
