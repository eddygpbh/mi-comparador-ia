import google.generativeai as genai
import streamlit as st

class AnalystAgent:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            # Usamos gemini-pro que es el más compatible
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            st.error(f"Error de configuración API: {e}")

    def analyze(self, query, products):
        try:
            # Prompt simplificado
            nombres_productos = ", ".join([p['name'] for p in products])
            prompt = f"El usuario busca '{query}'. Compara estos productos: {nombres_productos}. Recomienda el mejor brevemente."
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error al generar análisis con Gemini: {e}"
