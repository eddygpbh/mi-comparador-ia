import requests
from bs4 import BeautifulSoup
import random

class SRBCAgent:
    def fetch_product_data(self, product_name):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        
        # URL corregida para Mercado Libre México
        query = product_name.replace(' ', '-')
        url = f"https://www.mercadolibre.com.mx/navigation/addresses-hub?redirect=https%3A%2F%2Flista.mercadolibre.com.mx%2F{query}"
        # Intentamos también la versión directa simplificada
        direct_url = f"https://lista.mercadolibre.com.mx/{query}"
        
        try:
            print(f"🔗 Conectando a fuente de datos...")
            response = requests.get(direct_url, headers=headers, timeout=10)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []
            
            # Selectores actualizados para la nueva rejilla de Mercado Libre
            items = soup.select('.ui-search-result__wrapper') or soup.select('.poly-card')
            
            if not items:
                print("⚠️ No se detectaron elementos en el HTML. Usando modo de simulación para Track 2...")
                return self._get_mock_data(product_name)

            for item in items[:5]:
                name = item.select_one('.ui-search-item__title') or item.select_one('.poly-component__title')
                price = item.select_one('.price-tag-fraction') or item.select_one('.poly-price__current .price-tag-fraction')
                link = item.select_one('a')
                
                if name and price:
                    products.append({
                        "source": "MercadoLibre",
                        "name": name.get_text(strip=True),
                        "price": price.get_text(strip=True),
                        "link": link['href'] if link else ""
                    })
            
            return products

        except Exception as e:
            print(f"❌ Error de red: {e}. Activando datos de respaldo...")
            return self._get_mock_data(product_name)

    def _get_mock_data(self, product_name):
        """Genera datos si hay problemas de red para no detener el Track 2"""
        return [
            {"source": "Backup_Local", "name": f"{product_name} Nitro 5", "price": "15,499", "link": "#"},
            {"source": "Backup_Local", "name": f"{product_name} Legion 5", "price": "22,900", "link": "#"}
        ]
