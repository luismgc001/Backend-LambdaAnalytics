from django.urls import path
from .views import ScrapingSearchView, SearchAndETLView, ListaDeseosView, ArticuloDetalleView

urlpatterns = [
    path("search/", ScrapingSearchView.as_view(), name="search"),
    path("search-etl/", SearchAndETLView.as_view(), name="search_etl"),
    path("lista-deseos/", ListaDeseosView.as_view(), name="lista_deseos"),
    path("lista-deseos/<int:pk>/", ArticuloDetalleView.as_view(), name="detalle_deseo"),
]
