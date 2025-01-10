import re

def FiltroArticulos(data):
    if not data:
        return {"error": "No hay datos disponibles para procesar."}

    min_price_product = None
    max_price_product = None
    max_discount_product = None
    best_rated_product = None

    total_price = 0
    total_products = len(data)

    for product in data:
        try:
            raw_price = product.get("precio", "0").replace("$", "").replace(".", "").strip()
            price = float(raw_price)

            raw_discount = product.get("descuento", "0%").replace("% OFF", "").strip()
            discount = float(raw_discount) if raw_discount.isdigit() else 0

            raw_rating = product.get("calificacion", "").strip()
            rating_match = re.search(r"(\d+(\.\d+)?)", raw_rating)
            rating = float(rating_match.group(1)) if rating_match else 0

            total_price += price

            if not min_price_product or price < float(min_price_product["precio"].replace("$", "").replace(".", "").strip()):
                min_price_product = product

            if not max_price_product or price > float(max_price_product["precio"].replace("$", "").replace(".", "").strip()):
                max_price_product = product

            if not max_discount_product or discount > float(max_discount_product.get("descuento", "0").replace("% OFF", "").strip()):
                max_discount_product = product

            if not best_rated_product:
                best_rated_product = product
            else:
                best_rating_match = re.search(r"(\d+(\.\d+)?)", best_rated_product.get("calificacion", "").strip())
                best_rating = float(best_rating_match.group(1)) if best_rating_match else 0
                if rating > best_rating:
                    best_rated_product = product

        except Exception as e:
            print(f"Error al procesar el producto: {product.get('nombre', 'Sin título')}, Error: {e}")
            continue

    average_price = total_price / total_products if total_products > 0 else 0

    return {
        "ArticuloPrecioBajo": min_price_product,
        "ArticuloPrecioAlto": max_price_product,
        "ArticuloDescuentoAlto": max_discount_product,
        "PrecioPromedio": round(average_price, 2),
        "ArticuloMejorCalificacion": best_rated_product,
    }
