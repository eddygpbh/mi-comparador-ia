import streamlit as st
from main_orchestrator import start_and_return

st.set_page_config(page_title="Gemini Conductor", page_icon="🧠", layout="wide")

st.title("🧠 Sistema Gemini Conductor")
st.subheader("Comparador Inteligente de Productos")
st.markdown("---")

query = st.text_input("¿Qué misión le darás al Conductor hoy?", "Laptop potente para video")

if st.button("Iniciar Misión"):
    with st.spinner("El Conductor está operando..."):
        productos, analisis = start_and_return(query)
        
        st.markdown("### 📋 Informe del Conductor")
        st.success(analisis)
        
        with st.expander("Ver datos brutos de la búsqueda"):
            st.write(productos)
