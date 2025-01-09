from django.urls import path
from .views import ScrapingSearchView

urlpatterns = [
    path("search/", ScrapingSearchView.as_view(), name="search"),
]
