import google.generativeai as genai
import streamlit as st
from srbc_agent import SRBCAgent

class GeminiConductor:
    def __init__(self):
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # Configuramos al modelo con instrucciones de "Conductor"
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction="Eres el Conductor de una app de comparación. Tu objetivo es recibir una búsqueda, analizar los datos crudos que te entregará el buscador y generar un reporte de compra inteligente. Si los datos están vacíos, indica qué debería buscar el usuario."
        )

    def ejecutar_mision(self, query):
        # El conductor ordena al buscador trabajar
        buscador = SRBCAgent()
        datos_crudos = buscador.search(query)
        
        # El conductor procesa y decide qué decir
        prompt = f"El usuario busca: {query}. Aquí tienes los hallazgos: {datos_crudos}. Analiza y da la mejor opción."
        response = self.model.generate_content(prompt)
        
        return datos_crudos, response.text

def start_and_return(query):
    conductor = GeminiConductor()
    return conductor.ejecutar_mision(query)
