import google.generativeai as genai
import streamlit as st

class AnalystAgent:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            st.error(f"Error de API: {e}")

    def analyze(self, query, products):
        try:
            prompt = f"Compara brevemente estos productos para {query}: {products}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error en IA: {e}"
