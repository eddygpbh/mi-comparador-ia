import streamlit as st
from main_orchestrator import start_and_return

st.set_page_config(page_title="Comparador IA", page_icon="🤖", layout="wide")

st.title("🤖 Comparador Inteligente de Laptops")
st.markdown("---")

query = st.text_input("¿Qué producto deseas comparar?", "Laptop Gamer")

if st.button("Ejecutar Análisis Multiagente"):
    st.info(f"Iniciando búsqueda para: {query}...")
    try:
        productos, analisis = start_and_return(query)
        
        st.subheader("💡 Recomendación de la IA")
        if analisis:
            st.success(analisis)
        
        st.subheader(f"📦 Resultados para: {query}")
        if productos:
            cols = st.columns(len(productos))
            for i, p in enumerate(productos):
                with cols[i]:
                    st.metric(label=p.get('source', 'Tienda'), value=f"${p.get('price', 0)}")
                    st.write(f"**{p.get('name', 'Producto')}**")
                    if p.get('link'):
                        st.caption(f"[Ver producto]({p['link']})")
    except Exception as e:
        st.error(f"Error: {e}")
