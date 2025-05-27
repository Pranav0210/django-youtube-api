from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import YouTubeVideo
from .serializers import YouTubeVideoSerializer
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
class YouTubeVideoListView(ListAPIView):
    queryset = YouTubeVideo.objects.all()
    serializer_class = YouTubeVideoSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class YouTubeVideoSearchAPIView(ListAPIView):
    serializer_class = YouTubeVideoSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        query = self.request.query_params.get("query", "")
        if query:
            return YouTubeVideo.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).order_by("-published_at")
        return YouTubeVideo.objects.none()