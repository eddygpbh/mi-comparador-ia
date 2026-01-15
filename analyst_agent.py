import google.generativeai as genai
import streamlit as st

class AnalystAgent:
    def __init__(self):
        # Usamos st.secrets para leer la llave que pusiste en Advanced Settings
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            st.error(f"Error configurando Gemini: {e}")

    def analyze(self, query, products):
        try:
            prompt = f"Analiza estos productos para {query} y recomienda el mejor: {products}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error en el análisis: {e}"
