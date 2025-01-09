from django.urls import path
from .views import ScrapingSearchView, SearchAndETLView

urlpatterns = [
    path("search/", ScrapingSearchView.as_view(), name="search"),
     path("search-etl/", SearchAndETLView.as_view(), name="search_etl"),
]
