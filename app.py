import streamlit as st
from main_orchestrator import start_and_return

# Configuración de página PRIMERO
st.set_page_config(page_title="Comparador IA", page_icon="🤖", layout="wide")

# CSS para ocultar elementos que consumen recursos visuales
st.markdown("""
<style>
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🤖 Comparador Inteligente de Laptops")
st.markdown("---")

# Función con caché: Solo se ejecuta una vez, no en cada recarga
@st.cache_resource
def get_analysis(user_query):
    return start_and_return(user_query)

query = st.text_input("¿Qué producto deseas comparar?", "Laptop Gamer")

if st.button("Ejecutar Análisis Multiagente"):
    with st.spinner("Conectando agentes... (Esto puede tardar unos segundos)"):
        try:
            # Llamamos a la función optimizada
            productos, analisis = start_and_return(query)
            
            st.subheader("💡 Recomendación de la IA")
            st.success(analisis)
            
            st.subheader("📦 Productos Encontrados")
            if productos:
                cols = st.columns(len(productos))
                for i, p in enumerate(productos):
                    with cols[i]:
                        st.metric(label=p.get('source', 'Tienda'), value=f"${p.get('price', 0)}")
                        st.write(f"**{p.get('name', 'Producto')}**")
                        if p.get('link'):
                            st.caption(f"[Ver producto]({p['link']})")
            else:
                st.warning("No se encontraron productos en esta búsqueda simulada.")
                
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            st.info("Intenta recargar la página si el servidor se desconectó.")
