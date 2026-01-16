import google.generativeai as genai
import streamlit as st
from srbc_agent import SRBCAgent

class GeminiConductor:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            
            # DIAGNÓSTICO: Listamos qué modelos ve tu API Key realmente
            modelos_en_tu_cuenta = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    modelos_en_tu_cuenta.append(m.name.replace('models/', ''))
            
            # Prioridad de modelos (del más nuevo al más viejo)
            prioridad = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro', 'gemini-1.0-pro']
            
            self.model = None
            self.modelo_elegido = None

            # Buscamos el mejor modelo disponible que esté en tu cuenta
            for p in prioridad:
                if p in modelos_en_tu_cuenta:
                    self.model = genai.GenerativeModel(p)
                    self.modelo_elegido = p
                    break
            
            if not self.model:
                # Si no encontramos ninguno en la lista, intentamos el básico por defecto
                self.model = genai.GenerativeModel('gemini-pro')
                self.modelo_elegido = 'gemini-pro (default)'

        except Exception as e:
            st.error(f"Error de diagnóstico del Conductor: {e}")

    def ejecutar_mision(self, query):
        buscador = SRBCAgent()
        datos_crudos = buscador.search(query)
        
        prompt = f"Actúa como el Conductor. Usuario busca: {query}. Hallazgos: {datos_crudos}. Analiza cuál es mejor."
        
        try:
            response = self.model.generate_content(prompt)
            return datos_crudos, f"✅ **Conductor activo usando:** {self.modelo_elegido}\n\n{response.text}"
        except Exception as e:
            return datos_crudos, f"❌ El modelo {self.modelo_elegido} falló: {e}"

def start_and_return(query):
    conductor = GeminiConductor()
    return conductor.ejecutar_mision(query)
