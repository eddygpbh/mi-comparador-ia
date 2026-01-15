import google.generativeai as genai
import streamlit as st

class AnalystAgent:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            # Forzamos la configuración básica para evitar el error v1beta
            genai.configure(api_key=api_key)
            # Usamos el nombre exacto del modelo de producción
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            st.error(f"Error de configuración IA: {e}")

    def analyze(self, query, products):
        try:
            if not products:
                return "No hay productos para analizar."
            
            prompt = f"El usuario busca: {query}. Compara estos productos y dime cuál conviene: {products}. Responde breve en español."
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error en el servidor de Google: {e}"
