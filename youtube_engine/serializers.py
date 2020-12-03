from rest_framework.serializers import ModelSerializer

from youtube_engine.models import YoutubeVideo


class YoutubeVideoSerializer(ModelSerializer):

    class Meta:
        model = YoutubeVideo
        fields = "__all__"
