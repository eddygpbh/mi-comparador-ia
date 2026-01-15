from google import genai
import os
import time

class AnalystAgent:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) if api_key else None

    def evaluate_products(self, products):
        if not self.client: return "Falta API KEY."
        if not products: return "Sin productos."

        contexto = "\n".join([f"- {p['name']} | {p['price']} | {p['source']}" for p in products])
        
        prompt = f"Analiza estas laptops gamer y dime cuál es mejor por su precio: {contexto}. Responde en 3 líneas."
        
        # Intentar con el modelo estable 1.5-flash
        try:
            response = self.client.models.generate_content(
                model='gemini-1.5-flash', 
                contents=prompt
            )
            return response.text
        except Exception as e:
            if "429" in str(e):
                return "🕒 Límite de API alcanzado. Espera 60 segundos y vuelve a intentar."
            return f"❌ Error: {e}"
