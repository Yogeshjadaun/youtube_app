from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from functools import reduce
from operator import or_
from django.db.models import Q

from .constants import SORT_MAPPER, PUBLISHED_DATE, ERROR_MESSAGE
from .models import YoutubeVideo
from .serializers import YoutubeVideoSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class YoutubeVideoView(APIView, LargeResultsSetPagination):
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        '''
        Get api for fetching videos from database in order of published date
        :param request:
            page:int = page_number
        :return: Return paginated result of videos from database in order of published date.
        '''
        try:
            videos = YoutubeVideo.objects.all().order_by('publishing_date')
            videos = self.paginate_queryset(videos, request, view=self)
            data = YoutubeVideoSerializer(videos, many=True).data
            data = self.get_paginated_response(data)
            return data
        except Exception as e:
            return Response(status=500, data={"error": ERROR_MESSAGE})


class YoutubeVideoSearchView(APIView, LargeResultsSetPagination):
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        '''
        Get api for fetching videos related to particular tags from database in order of published date
        :param request:
            video:str = search text
            page:int = page_number
        :return: Return paginated result of videos related to search query from database in order of published date.
        '''
        try:
            video = request.GET.get('video', None)
            if video:
                videos = YoutubeVideo.objects.filter(reduce(or_, [Q(title__icontains=kw) for kw in video.split(' ')])).order_by('publishing_date')
            else:
                videos = YoutubeVideo.objects.all().order_by('publishing_date')
            videos = self.paginate_queryset(videos, request, view=self)
            data = YoutubeVideoSerializer(videos, many=True).data
            data = self.get_paginated_response(data)
            return data
        except Exception as e:
            print(e.__str__())
            return Response(status=500, data={"error": ERROR_MESSAGE})


class YoutubeVideoDashboardView(APIView, LargeResultsSetPagination):
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        '''
        Get api for Dashboard to fetch videos from database in
        particular order.
        :param request:
            video:str = search text
            sort:str = sort order ['title', 'description',
            'publishing_date', 'channel_title] prefix '-' for reverse order
            page:int = page_number
        :return: Return paginated result of videos related to search query
        from database in particular order.
        '''
        try:
            video = request.GET.get('video', None)
            sort_term = sort = request.GET.get('sort', PUBLISHED_DATE)
            asc_order = True
            sort_field = PUBLISHED_DATE
            if sort[0] == '-':
                sort_term = sort[1:]
                asc_order = False
            if SORT_MAPPER.get(sort_term):
                sort_field = SORT_MAPPER.get(sort_term)
                sort_field = sort_field if asc_order else '-' + sort_field

            if video:
                videos = YoutubeVideo.objects.filter(reduce(or_, [Q(title__icontains=kw) for kw in video.split(' ')])).order_by(sort_field)
            else:
                videos = YoutubeVideo.objects.all()
            videos = self.paginate_queryset(videos, request, view=self)
            data = YoutubeVideoSerializer(videos, many=True).data
            data = self.get_paginated_response(data)
            return data
        except Exception as e:
            return Response(status=500, data={"error": ERROR_MESSAGE})
