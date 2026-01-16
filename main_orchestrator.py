import google.generativeai as genai
import streamlit as st
from srbc_agent import SRBCAgent

class GeminiConductor:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            
            # Lista de modelos a intentar en orden de preferencia
            self.modelos_disponibles = [
                'gemini-1.5-flash', 
                'gemini-1.5-pro', 
                'gemini-1.0-pro', 
                'gemini-pro'
            ]
            self.model = None
            
            # Intentamos despertar al modelo que esté disponible
            for nombre_modelo in self.modelos_disponibles:
                try:
                    m = genai.GenerativeModel(nombre_modelo)
                    # Prueba rápida de conexión
                    m.generate_content("test", generation_config={"max_output_tokens": 1})
                    self.model = m
                    self.modelo_activo = nombre_modelo
                    break
                except:
                    continue
            
            if not self.model:
                st.error("No se pudo conectar con ningún modelo de Gemini. Revisa tu API Key.")
        except Exception as e:
            st.error(f"Error de configuración: {e}")

    def ejecutar_mision(self, query):
        buscador = SRBCAgent()
        datos_crudos = buscador.search(query)
        
        prompt = f"Actúa como el Conductor. Usuario busca: {query}. Hallazgos: {datos_crudos}. Analiza cuál es mejor."
        
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                return datos_crudos, f"(Modelo usado: {self.modelo_activo})\n\n{response.text}"
            else:
                return datos_crudos, "El Conductor no pudo encontrar un cerebro disponible."
        except Exception as e:
            return datos_crudos, f"Fallo crítico en la misión: {e}"

def start_and_return(query):
    conductor = GeminiConductor()
    return conductor.ejecutar_mision(query)
