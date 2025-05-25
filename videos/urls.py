from django.urls import path
from .views import YouTubeVideoListView

urlpatterns = [
    path('videos/', YouTubeVideoListView.as_view()),
]
