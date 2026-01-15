from srbc_agent import SRBCAgent
from analyst_agent import AnalystAgent

def start_and_return(query):
    # 1. Búsqueda REAL
    search_agent = SRBCAgent()
    productos = search_agent.search_amazon(query)
    
    # 2. Análisis REAL
    analyst = AnalystAgent()
    analisis = analyst.analyze(query, productos)
    
    return productos, analisis
