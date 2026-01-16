import google.generativeai as genai
import streamlit as st
from srbc_agent import SRBCAgent
import time

class GeminiConductor:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            
            # --- LISTA DE PRIORIDAD BASADA EN TU CUENTA ---
            # Priorizamos los modelos 'Flash' que suelen tener cuota gratuita
            self.prioridad = [
                'models/gemini-2.0-flash-001',      # Opción 1: Específico y estable
                'models/gemini-2.0-flash',          # Opción 2: Genérico 2.0
                'models/gemini-flash-latest',       # Opción 3: Último flash disponible
                'models/gemini-1.5-flash',          # Opción 4: El clásico 1.5
                'models/gemini-2.0-flash-lite'      # Opción 5: Versión ligera (casi imposible que falle)
            ]
            
            self.model = None
            self.nombre_modelo = "Buscando..."

            # Lógica de selección quirúrgica
            available_models = [m.name for m in genai.list_models()]
            
            for p in self.prioridad:
                if p in available_models:
                    self.model = genai.GenerativeModel(p)
                    self.nombre_modelo = p
                    break
            
            # Si no encuentra los de la lista, usa el primero que encuentre en la cuenta (Fallback)
            if not self.model and available_models:
                self.model = genai.GenerativeModel(available_models[0])
                self.nombre_modelo = available_models[0]

        except Exception as e:
            st.error(f"Error iniciando sistemas: {e}")

    def ejecutar_mision(self, query):
        if not self.model:
            return [], "❌ Error: No hay modelos disponibles en tu cuenta."

        # Buscador
        buscador = SRBCAgent()
        datos = buscador.search(query)
        
        # Conductor
        prompt = f"""
        Eres el Conductor Inteligente. 
        Misión: Analizar opciones de compra para '{query}'.
        Datos encontrados: {datos}
        
        Instrucciones:
        1. Analiza los productos.
        2. Si los datos son pocos, da consejos generales de experto sobre qué buscar.
        3. Sé breve y directo.
        """
        
        try:
            # Intentamos generar. Si da error 429 (Cuota), avisamos al usuario.
            response = self.model.generate_content(prompt)
            return datos, f"✅ **Conductor operando con:** \n\n{response.text}"
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                return datos, f"⚠️ **Límite de Cuota Alcanzado** en .\nGoogle pide esperar un minuto antes de la siguiente pregunta."
            return datos, f"❌ Error en el modelo {self.nombre_modelo}: {e}"

def start_and_return(query):
    conductor = GeminiConductor()
    return conductor.ejecutar_mision(query)
