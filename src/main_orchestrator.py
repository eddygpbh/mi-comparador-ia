import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.srbc_agent import SRBCAgent
from agents.analyst_agent import AnalystAgent
from database_manager import DatabaseManager

def start():
    product_query = "Laptop Gamer"
    print(f"🚀 Iniciando Sistema Multiagente para: {product_query}")
    
    # Instanciar agentes
    srbc = SRBCAgent()
    analyst = AnalystAgent()
    db = DatabaseManager()
    
    # 1. Obtener Datos
    results = srbc.fetch_product_data(product_query)
    
    # 2. Persistir en DB
    for p in results:
        db.insert_product(p)
    
    # 3. Analizar con IA
    print("🧠 Agente Analista evaluando opciones con Gemini 3 Flash...")
    recommendation = analyst.evaluate_products(results)
    
    print("\n--- RECOMENDACIÓN DEL EXPERTO ---")
    print(recommendation)

if __name__ == "__main__":
    start()
