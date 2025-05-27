from django.urls import path
from .views import YouTubeVideoListView, YouTubeVideoSearchAPIView

urlpatterns = [
    path('videos/', YouTubeVideoListView.as_view()),
    path("search/", YouTubeVideoSearchAPIView.as_view(), name="search-videos")
]
