import re

def FiltroArticulos(data):
    """
    Procesa una lista de productos para calcular métricas específicas y recomendaciones.
    :param data: Lista de diccionarios con información de los productos.
    :return: Diccionario con las métricas y recomendaciones.
    """
    if not data:
        return {"error": "No hay datos disponibles para procesar."}

    # Inicializar variables para las métricas
    min_price_product = None
    max_price_product = None
    max_discount_product = None
    best_rated_product = None

    total_price = 0
    total_products = len(data)

    for product in data:
        try:
            # Limpieza del precio: eliminar '$' y '.' antes de convertirlo a float
            raw_price = product.get("precio", "0").replace("$", "").replace(".", "").strip()
            price = float(raw_price)

            # Limpieza del descuento (si existe)
            raw_discount = product.get("descuento", "0%").replace("% OFF", "").strip()
            discount = float(raw_discount) if raw_discount.isdigit() else 0

            # Limpieza de la calificación (si existe)
            raw_rating = product.get("calificacion", "0").strip()
            rating = float(raw_rating) if raw_rating.replace(".", "").isdigit() else 0

            # Acumular precios para calcular el promedio
            total_price += price

            # Producto con el precio más bajo
            if not min_price_product or price < float(min_price_product["precio"].replace("$", "").replace(".", "").strip()):
                min_price_product = product

            # Producto con el precio más alto
            if not max_price_product or price > float(max_price_product["precio"].replace("$", "").replace(".", "").strip()):
                max_price_product = product

            # Producto con el descuento más alto
            if not max_discount_product or discount > float(
                max_discount_product.get("descuento", "0").replace("% OFF", "").strip()
            ):
                max_discount_product = product

            # Producto con la mejor calificación
            if not best_rated_product or rating > float(
                best_rated_product.get("calificacion", "0").strip()
            ):
                best_rated_product = product

        except Exception as e:
            print(f"Error al procesar el producto: {product.get('nombre', 'Sin título')}, Error: {e}")
            continue

    # Calcular el precio promedio
    average_price = total_price / total_products if total_products > 0 else 0

    # Resultado final
    return {
        "ArticuloPrecioBajo": min_price_product,
        "ArticuloPrecioAlto": max_price_product,
        "ArticuloDescuentoAlto": max_discount_product,
        "PrecioPromedio": round(average_price, 2),
        "ArticuloMejorCalificacion": best_rated_product,
    }
