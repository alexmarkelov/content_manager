from django.urls import path, include
from .views import LastPodcastsView, HomePageView


app_name = 'podcasts'
urlpatterns = [
    path('last/', LastPodcastsView.as_view(), name="last_podcasts"),
    path('', HomePageView.as_view(), name="homepage"),
]
