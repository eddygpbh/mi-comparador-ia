import google.generativeai as genai
import streamlit as st
from srbc_agent import SRBCAgent

class GeminiConductor:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            # Usamos el alias más estable del modelo 1.5 Flash
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            st.error(f"Error de configuración: {e}")

    def ejecutar_mision(self, query):
        # El Conductor ordena buscar
        buscador = SRBCAgent()
        datos_crudos = buscador.search(query)
        
        # El Conductor analiza y decide
        contexto = f"Usuario busca: {query}. Datos encontrados: {datos_crudos}"
        instruccion = "Eres el Conductor. Compara estos productos y da una recomendación final honesta en español."
        
        try:
            response = self.model.generate_content(f"{instruccion}\n\n{contexto}")
            return datos_crudos, response.text
        except Exception as e:
            return datos_crudos, f"Error del Conductor al procesar: {e}"

def start_and_return(query):
    conductor = GeminiConductor()
    return conductor.ejecutar_mision(query)
