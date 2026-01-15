import google.generativeai as genai
import streamlit as st

class AnalystAgent:
    def __init__(self):
        try:
            # Configurar la API Key desde los secretos
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            
            # CAMBIO IMPORTANTE: Usamos 'gemini-pro' que es el modelo estándar y estable
            self.model = genai.GenerativeModel('gemini-pro')
            
        except Exception as e:
            st.error(f"Error configurando Gemini: {e}")

    def analyze(self, query, products):
        try:
            # Crear un prompt claro para el modelo
            prompt = f"""
            Actúa como un experto en compras de tecnología.
            El usuario busca: "{query}".
            
            Aquí están los productos encontrados (simulados o reales):
            {products}
            
            Tarea:
            1. Analiza cuál es la mejor opción calidad-precio.
            2. Explica por qué brevemente.
            3. Si la lista está vacía, da recomendaciones generales para comprar ese producto.
            
            Responde en español y sé conciso.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error detallado del modelo: {e}"
