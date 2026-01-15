import google.generativeai as genai
import streamlit as st

class AnalystAgent:
    def __init__(self):
        # Usamos el secreto que configuraste en Streamlit Cloud
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze(self, query, products):
        prompt = f"""
        Como experto analista de tecnología, evalúa las siguientes opciones para: {query}.
        Productos: {products}
        Indica cuál es la mejor opción calidad-precio y por qué. 
        Responde de forma breve y profesional en español.
        """
        response = self.model.generate_content(prompt)
        return response.text
