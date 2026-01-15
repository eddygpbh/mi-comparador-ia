from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def run_conductor():
    try:
        prompt = """
        Actúa como Ingeniero de Datos. 
        TAREA:
        1. Crea un script llamado 'src/database_manager.py' que use la librería 'supabase' para insertar los datos del Agente SRBC.
        2. El script debe incluir una función 'normalize_data' que convierta precios (strings como '.200,50') a float puro (1200.50).
        3. Define la estructura SQL necesaria para crear la tabla 'product_history' en Supabase (id, name, price, source, link, created_at).
        """
        
        response = client.models.generate_content(
            model='gemini-3-flash-preview', 
            contents=prompt
        )
        
        print("\n✨ [CONDUCTOR: CONFIGURACIÓN DE BASE DE DATOS Y NORMALIZACIÓN]")
        print(response.text)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_conductor()
