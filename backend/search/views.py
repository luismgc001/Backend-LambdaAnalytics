import requests
from bs4 import BeautifulSoup
from rest_framework.test import APIClient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Articulo
from .serializers import ArticuloSerializer
from django.http import JsonResponse
from .etl import FiltroArticulos

class ScrapingSearchView(APIView):
    def get(self, request):
        # Obtener el término de búsqueda desde los parámetros
        query = request.query_params.get("query")
        if not query:
            return Response(
                {"error": "El parámetro 'q' es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # URL de búsqueda en Mercado Libre Colombia
        search_url = f"https://listado.mercadolibre.com.co/{query}"

        try:
            # Realizar la solicitud GET a Mercado Libre
            response = requests.get(search_url)
            if response.status_code != 200:
                return Response(
                    {"error": "Error al obtener los datos de Mercado Libre."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Analizar el contenido HTML de la respuesta
            soup = BeautifulSoup(response.content, "html.parser")

            # Extraer información relevante de los productos
            items = []
            for product in soup.find_all("div", class_="ui-search-result__wrapper"):
                try:
                    print("Dentro de try")
                    elemento_nombre = product.find("h2", class_="poly-component__title-wrapper")                    
                    nombre = elemento_nombre.text.strip() if elemento_nombre else "Sin nombre"
                    elemento_precio = product.find("span", class_="andes-money-amount andes-money-amount--cents-superscript")
                    precio = elemento_precio.text.strip() if elemento_precio else "Sin precio"
                    print("DEBUG")
                    elemento_enlace = product.find("a", class_="poly-component__title")
                    enlace = elemento_enlace["href"] if elemento_enlace else "Sin enlace"
                    elemento_imagen = product.find("img", class_="poly-component__picture")
                    imagen = elemento_imagen["src"] if elemento_imagen else "Sin imagen"

                    print("Descuento")

                    # Descuento (si existe)
                    elemento_descuento = product.find("span", class_="andes-money-amount__discount")
                    descuento = elemento_descuento.text.strip() if elemento_descuento else "Sin descuento"

                    # Calificación (si existe)
                    elemento_calificacion = product.find("span", class_="andes-visually-hidden")
                    calificacion = elemento_calificacion.text.strip() if elemento_calificacion else "Sin calificación"

                    # Vendedor (si es tienda oficial)
                    elemento_vendedor = product.find("span", class_="poly-component__seller")
                    vendedor = elemento_vendedor.text.strip() if elemento_vendedor else "No especificado"

                    # Agregar los datos al resultado
                    items.append({
                        "nombre": nombre,
                        "precio": precio,
                        "enlace": enlace,
                        "imagen": imagen,
                        "vendedor": vendedor,
                        "descuento": descuento,
                        "calificacion": calificacion,
                    })
                except Exception as e:
                    # Ignorar productos que no tienen toda la información
                    print(f"Error al procesar un producto: {e}")
                    continue
            
            
            return Response(items, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Error al realizar la búsqueda: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

from .views import ScrapingSearchView

class SearchAndETLView(APIView):
    def get(self, request):
        query = request.query_params.get("query")
        if not query:
            return Response({"error": "El parámetro 'query' es obligatorio."}, status=400)

        # Llama directamente a ScrapingSearchView
        scraping_view = ScrapingSearchView()
        scraping_response = scraping_view.get(request)

        if scraping_response.status_code != 200:
            return Response(
                {"error": "Error al obtener los datos desde ScrapingSearchView."},
                status=scraping_response.status_code,
            )

        # Obtener los datos del scraping
        products = scraping_response.data

        # Pasar los datos a la función ETL
        etl_result = FiltroArticulos(products)

        return Response(etl_result, status=200)
    
class ListaDeseosView(APIView):
    def get(self, request):
        articulos = Articulo.objects.all()
        serializer = ArticuloSerializer(articulos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ArticuloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ArticuloDetalleView(APIView):
    def delete(self, request, pk):
        try:
            articulo = Articulo.objects.get(pk=pk)
            articulo.delete()
            return Response({"message": "Artículo eliminado correctamente"}, status=status.HTTP_200_OK)
        except Articulo.DoesNotExist:
            return Response({"error": "Artículo no encontrado"}, status=status.HTTP_404_NOT_FOUND)
