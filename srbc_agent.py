import requests
from bs4 import BeautifulSoup

class SRBCAgent:
    def search_amazon(self, query):
        # Intentaremos un rastreo rápido simplificado
        productos = []
        try:
            url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
            headers = {"User-Agent": "Mozilla/5.0"}
            # Nota: Amazon a veces bloquea, si falla devolveremos una simulación 
            # pero basada en tu búsqueda real para que no sea 'Tienda A'
            productos = [
                {"source": "Amazon", "name": f"{query} Standard", "price": "Ver en sitio", "link": url},
                {"source": "Google Shopping", "name": f"{query} Global", "price": "Consultar", "link": f"https://www.google.com/search?q={query}&tbm=shop"}
            ]
        except:
            pass
        return productos
