import google.generativeai as genai
import streamlit as st
from srbc_agent import SRBCAgent
from database_manager import DatabaseManager
import time
import random

class GeminiConductor:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            self.nombre_modelo = 'models/gemini-flash-latest'
            self.model = genai.GenerativeModel(self.nombre_modelo)
            # Inicializamos el gestor de base de datos
            self.db = DatabaseManager()
        except Exception as e:
            st.error(f"Error iniciando sistemas: {e}")

    def generar_con_reintento(self, prompt, intentos_max=3):
        for intento in range(intentos_max):
            try:
                return self.model.generate_content(prompt)
            except Exception as e:
                if "429" in str(e) or "503" in str(e):
                    if intento < intentos_max - 1:
                        tiempo_espera = (2 ** intento) + random.uniform(0, 1)
                        st.warning(f"🚦 Reintentando en {int(tiempo_espera)}s...")
                        time.sleep(tiempo_espera)
                        continue
                raise e

    def ejecutar_mision(self, query):
        buscador = SRBCAgent()
        datos = buscador.search(query)
        
        prompt = f"Usuario busca: '{query}'. Datos: {datos}. Da una recomendación breve."
        
        try:
            response = self.generar_con_reintento(prompt)
            texto_respuesta = response.text
            
            # ACCIÓN DE MEMORIA: Guardamos en Supabase
            self.db.guardar_consulta(query, str(datos), texto_respuesta)
            
            return datos, f"✅ **Conductor activo**\n\n{texto_respuesta}"
            
        except Exception as e:
            return datos, f"❌ Error: {e}"

def start_and_return(query):
    conductor = GeminiConductor()
    return conductor.ejecutar_mision(query)
