from analyst_agent import AnalystAgent

def start_and_return(query):
    # Simulamos búsqueda dinámica basada en lo que escribes
    # Esto asegura que veas cambios reales en la pantalla
    productos = [
        {
            "source": "MercadoLibre", 
            "name": f"{query} Versión Pro", 
            "price": 1500, 
            "link": "https://mercadolibre.com"
        },
        {
            "source": "Amazon", 
            "name": f"{query} Edición Económica", 
            "price": 950, 
            "link": "https://amazon.com"
        },
        {
            "source": "Tienda Local", 
            "name": f"{query} Refurbished", 
            "price": 800, 
            "link": "#"
        }
    ]
    
    # Iniciamos el agente
    analyst = AnalystAgent()
    analisis = analyst.analyze(query, productos)
    
    return productos, analisis
