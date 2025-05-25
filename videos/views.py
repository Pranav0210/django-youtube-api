from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import YouTubeVideo
from .serializers import YouTubeVideoSerializer
from rest_framework.filters import SearchFilter

# Create your views here.

class YouTubeVideoListView(ListAPIView):
    queryset = YouTubeVideo.objects.all()
    serializer_class = YouTubeVideoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
