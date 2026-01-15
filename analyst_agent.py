import google.generativeai as genai
import streamlit as st

class AnalystAgent:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            # Usamos el nombre completo y actualizado del modelo
            self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
        except Exception as e:
            st.error(f"Error de configuración: {e}")

    def analyze(self, query, products):
        try:
            # Creamos un mensaje simple para probar la conexión
            prompt = f"El usuario busca {query}. Analiza estos productos y dime cuál es mejor: {products}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Si falla, intentamos con el nombre alternativo 'gemini-1.5-flash'
            try:
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                response = self.model.generate_content(prompt)
                return response.text
            except:
                return f"Error de modelo (404): {e}. Verifica que tu API Key sea válida para Gemini 1.5."
