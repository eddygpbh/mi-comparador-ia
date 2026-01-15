import google.generativeai as genai
import streamlit as st
from srbc_agent import SRBCAgent

class GeminiConductor:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            
            # Forzamos el uso del modelo específico que SI está en v1
            # El nombre 'gemini-1.5-flash' a veces falla en v1beta, 
            # pero 'models/gemini-1.5-flash' es la ruta fija.
            self.model = genai.GenerativeModel('models/gemini-1.5-flash')
        except Exception as e:
            st.error(f"Error al despertar al Conductor: {e}")

    def ejecutar_mision(self, query):
        buscador = SRBCAgent()
        datos_crudos = buscador.search(query)
        
        prompt = f"Actúa como el Conductor. Usuario busca: {query}. Hallazgos: {datos_crudos}. Analiza cuál es mejor y por qué."
        
        try:
            # Forzamos la generación con el modelo configurado
            response = self.model.generate_content(prompt)
            return datos_crudos, response.text
        except Exception as e:
            return datos_crudos, f"El Conductor tuvo un problema de conexión: {e}"

def start_and_return(query):
    conductor = GeminiConductor()
    return conductor.ejecutar_mision(query)
