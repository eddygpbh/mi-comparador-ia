from analyst_agent import AnalystAgent

def start_and_return(query):
    productos = [
        {"source": "Tienda A", "name": f"{query} Pro", "price": 1200, "link": "#"},
        {"source": "Tienda B", "name": f"{query} Basic", "price": 800, "link": "#"}
    ]
    analyst = AnalystAgent()
    analisis = analyst.analyze(query, productos)
    return productos, analisis
