import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SearchView(APIView):
    def get(self, request):
        # Obtén el término de búsqueda de los parámetros de la solicitud
        query = request.query_params.get("query")

        if not query:
            return Response(
                {"error": "El parámetro 'q' es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # URL de búsqueda específica para Mercado Libre Colombia
        url = f"https://api.mercadolibre.com/sites/MCO/search?q={query}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                # Procesar los resultados para extraer campos relevantes
                results = []
                for item in data.get("results", []):
                    product = {
                        "id": item.get("id"),
                        "nombre": item.get("title"),
                        "precio": item.get("price"),
                        "descuento": {
                            "original_price": item.get("price_discount", {}).get("original_price"),
                            "percentage": item.get("price_discount", {}).get("discount_percentage"),
                        },
                        "vendedor": {
                            "id": item.get("seller", {}).get("id"),
                            "nickname": item.get("seller", {}).get("nickname"),
                            "profile_url": item.get("seller", {}).get("permalink"),
                        },
                        "calificacion": {
                            "average": item.get("ratings", {}).get("average"),
                            "total": item.get("ratings", {}).get("total"),
                        },
                        "imagen": item.get("thumbnail"),
                        "url": item.get("permalink"),
                        
                        
                        
                    }
                    results.append(product)

                return Response(results, status=status.HTTP_200_OK)

            return Response(
                {"error": "Error al consultar la API de Mercado Libre."},
                status=response.status_code,
            )
        except Exception as e:
            return Response(
                {"error": f"Error al realizar la búsqueda: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
