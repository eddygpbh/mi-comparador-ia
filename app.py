import streamlit as st
from src.main_orchestrator import start_and_return # Modificaremos el orquestador para esto

st.set_page_config(page_title="Comparador IA", page_icon="🤖")

st.title("🤖 Comparador Inteligente de Laptops")
st.write("Analizando precios reales y calidad con IA.")

query = st.text_input("¿Qué laptop buscas?", "Laptop Gamer")

if st.button("Buscar y Analizar"):
    with st.spinner("Los agentes están trabajando..."):
        # Aquí llamaremos a la lógica que ya creamos
        st.info("Rastreando fuentes y consultando a la IA...")
        # (Próximo paso: conectar el orquestador aquí)
        st.success("Análisis completado (Ver resultados en consola por ahora)")
