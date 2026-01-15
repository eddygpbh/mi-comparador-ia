import streamlit as st
import sys
import os

# Forzar a Python a encontrar la carpeta 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main_orchestrator import start_and_return

st.set_page_config(page_title="Comparador IA", page_icon="🤖", layout="wide")

st.title("🤖 Comparador Inteligente de Laptops")
st.markdown("---")

query = st.text_input("¿Qué producto deseas comparar?", "Laptop Gamer")

if st.button("Ejecutar Análisis Multiagente"):
    with st.spinner("Los agentes están rastreando y analizando..."):
        try:
            productos, analisis = start_and_return(query)
            
            st.subheader("💡 Recomendación de la IA")
            st.success(analisis)
            
            st.subheader("📦 Productos Encontrados")
            cols = st.columns(len(productos))
            
            for i, p in enumerate(productos):
                with cols[i]:
                    st.metric(label=p['source'], value=f"${p['price']}")
                    st.write(f"**{p['name']}**")
                    st.caption(f"[Ver producto]({p['link']})")
        except Exception as e:
            st.error(f"Hubo un error en el proceso: {e}")
