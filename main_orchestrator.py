import google.generativeai as genai
import streamlit as st
from srbc_agent import SRBCAgent

class GeminiConductor:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            
            # --- FASE DE DIAGNÓSTICO ---
            self.modelos_detectados = []
            try:
                # Obtenemos la lista REAL que ve el servidor
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        self.modelos_detectados.append(m.name)
            except Exception as e:
                st.error(f"Error listando modelos: {e}")

            # Intentamos seleccionar el mejor disponible automáticamente
            self.model = None
            self.nombre_modelo_activo = "Ninguno"

            # Buscamos coincidencias en la lista real
            preferencias = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro', 'gemini-pro']
            
            for pref in preferencias:
                # Buscamos si algún modelo de la lista CONTIENE el nombre preferido
                match = next((m for m in self.modelos_detectados if pref in m), None)
                if match:
                    self.model = genai.GenerativeModel(match)
                    self.nombre_modelo_activo = match
                    break
            
            # Si aún así falla, probamos el primero que haya en la lista
            if not self.model and self.modelos_detectados:
                self.model = genai.GenerativeModel(self.modelos_detectados[0])
                self.nombre_modelo_activo = self.modelos_detectados[0]

        except Exception as e:
            st.error(f"Error crítico de configuración: {e}")

    def ejecutar_mision(self, query):
        # 1. Mostramos al usuario qué modelos ve el sistema (DEBUG)
        debug_info = f"🔍 **Modelos encontrados en tu cuenta:** {self.modelos_detectados}\n\n"
        debug_info += f"🚀 **Intentando usar:** {self.nombre_modelo_activo}"
        
        if not self.model:
            return [], f"{debug_info}\n\n❌ ERROR: No se pudo iniciar ningún modelo."

        # 2. Ejecutamos la búsqueda y análisis
        buscador = SRBCAgent()
        datos_crudos = buscador.search(query)
        
        prompt = f"Actúa como el Conductor. Usuario busca: {query}. Hallazgos: {datos_crudos}. Analiza cuál es mejor."
        
        try:
            response = self.model.generate_content(prompt)
            return datos_crudos, f"{debug_info}\n\n✅ **Respuesta del Conductor:**\n{response.text}"
        except Exception as e:
            return datos_crudos, f"{debug_info}\n\n❌ Error generando contenido: {e}"

def start_and_return(query):
    conductor = GeminiConductor()
    return conductor.ejecutar_mision(query)
