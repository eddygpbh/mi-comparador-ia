import google.generativeai as genai
import streamlit as st
from srbc_agent import SRBCAgent
import time
import random

class GeminiConductor:
    def __init__(self):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
            
            # Usaremos el alias genérico 'flash-latest' que siempre apunta al modelo más rápido y barato
            # Esto evita los errores de "limit: 0" de los modelos Pro experimentales
            self.nombre_modelo = 'models/gemini-flash-latest'
            self.model = genai.GenerativeModel(self.nombre_modelo)

        except Exception as e:
            st.error(f"Error iniciando sistemas: {e}")

    def generar_con_reintento(self, prompt, intentos_max=3):
        """Intenta generar contenido y si falla por cuota, espera y reintenta."""
        for intento in range(intentos_max):
            try:
                return self.model.generate_content(prompt)
            except Exception as e:
                error_str = str(e)
                # Si es error de Cuota (429) o Sobrecarga (503)
                if "429" in error_str or "503" in error_str:
                    if intento < intentos_max - 1:
                        # Tiempo de espera exponencial: 2s, 4s, 8s...
                        tiempo_espera = (2 ** intento) + random.uniform(0, 1)
                        st.warning(f"🚦 Tráfico alto en la IA. Reintentando en {int(tiempo_espera)} segundos... (Intento {intento+1}/{intentos_max})")
                        time.sleep(tiempo_espera)
                        continue
                # Si es otro error o se acabaron los intentos, lanzamos el error
                raise e

    def ejecutar_mision(self, query):
        if not hasattr(self, 'model'):
            return [], "❌ Error: El conductor no tiene cerebro configurado."

        # Buscador
        buscador = SRBCAgent()
        datos = buscador.search(query)
        
        # Conductor
        prompt = f"""
        Eres el Conductor Inteligente de compras.
        Usuario busca: '{query}'.
        Datos encontrados: {datos}
        
        Tarea:
        Da una recomendación de compra basada en los datos (o general si no hay datos).
        Sé breve, directo y útil.
        """
        
        try:
            # Usamos la nueva función con paciencia
            response = self.generar_con_reintento(prompt)
            return datos, f"✅ **Conductor activo** ({self.nombre_modelo})\n\n{response.text}"
            
        except Exception as e:
            if "429" in str(e):
                return datos, "⏳ **El sistema está descansando.** Google ha pedido una pausa de 1 minuto por límite de uso gratuito. Por favor espera un poco antes de buscar de nuevo."
            return datos, f"❌ Error final: {e}"

def start_and_return(query):
    conductor = GeminiConductor()
    return conductor.ejecutar_mision(query)
