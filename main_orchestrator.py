from srbc_agent import SRBCAgent
from analyst_agent import AnalystAgent
from database_manager import DatabaseManager

def start_and_return(query):
    db = DatabaseManager()
    # Scraper simulado/real
    productos = [
        {"source": "Mercado Libre", "name": f"{query} Pro", "price": 1200, "link": "#"},
        {"source": "Amazon", "name": f"{query} Ultra", "price": 1150, "link": "#"}
    ]
    
    analyst = AnalystAgent()
    analisis = analyst.analyze(query, productos)
    
    return productos, analisis
