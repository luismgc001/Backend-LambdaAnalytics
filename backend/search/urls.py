from django.urls import path
from .views import ScrapingSearchView, ListaDeseosView, ArticuloDetalleView

urlpatterns = [
    path("search/", ScrapingSearchView.as_view(), name="search"),
    path("lista-deseos/", ListaDeseosView.as_view(), name="lista_deseos"),
    path("lista-deseos/<int:pk>/", ArticuloDetalleView.as_view(), name="detalle_deseo"),
]
