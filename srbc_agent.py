import re
from duckduckgo_search import DDGS

class SRBCAgent:
    def __init__(self):
        self.ddgs = DDGS()

    def _extraer_precio(self, texto):
        # Busca patrones como 9.99, 99€, 99.00 USD
        patron = r'[$€£]\s?\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?'
        match = re.search(patron, texto)
        return match.group(0) if match else None

    def search(self, query):
        productos = []
        try:
            # 1. Búsqueda de Texto para encontrar Títulos, Links y Precios
            # Buscamos "buy [producto] price" para forzar resultados de venta
            search_query = f"{query} buy online price"
            results = list(self.ddgs.text(search_query, max_results=12))
            
            # 2. Búsqueda de Imágenes para darle vida a la vitrina
            # Intentamos buscar imágenes que coincidan
            images_gen = self.ddgs.images(query, max_results=12)
            images = list(images_gen) if images_gen else []

            for i, res in enumerate(results):
                # Intentamos cazar un precio del snippet de texto
                precio_encontrado = self._extraer_precio(res.get('body', ''))
                
                # Si no hay precio en el texto, ponemos un placeholder para que la IA lo estime después
                precio_final = precio_encontrado if precio_encontrado else "Ver web"
                
                # Asignamos una imagen si existe, si no una genérica
                img_url = images[i]['image'] if i < len(images) else "https://via.placeholder.com/300?text=No+Image"

                producto = {
                    "id": i,
                    "nombre": res.get('title', 'Producto sin nombre'),
                    "link": res.get('href', '#'),
                    "descripcion": res.get('body', ''),
                    "precio": precio_final,
                    "imagen": img_url,
                    "score": 0 # El orquestador calculará esto después
                }
                productos.append(producto)

            # Filtramos resultados que parecen basura (sin título claro)
            productos = [p for p in productos if len(p['nombre']) > 5][:10]
            
            return productos

        except Exception as e:
            print(f"Error en Agente de Adquisición: {e}")
            return []
