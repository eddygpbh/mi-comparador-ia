import streamlit as st
from main_orchestrator import start_and_return

st.set_page_config(page_title="Comparador IA", page_icon="🤖", layout="wide")

st.title("🤖 Comparador Inteligente de Laptops")
st.markdown("---")

# Input del usuario
query = st.text_input("¿Qué producto deseas comparar?", "Laptop Gamer")

if st.button("Ejecutar Análisis Multiagente"):
    # Quitamos el spinner para ver si hay errores inmediatos
    st.info(f"Iniciando búsqueda para: {query}...")
    
    try:
        # Llamamos directo a la función SIN caché
        productos, analisis = start_and_return(query)
        
        st.subheader("💡 Recomendación de la IA")
        if analisis:
            st.success(analisis)
        else:
            st.warning("La IA no devolvió un análisis.")
        
        st.subheader(f"📦 Resultados para: {query}")
        
        if productos:
            cols = st.columns(len(productos))
            for i, p in enumerate(productos):
                with cols[i]:
                    st.metric(label=p.get('source', 'Tienda'), value=f"${p.get('price', 0)}")
                    st.write(f"**{p.get('name', 'Producto')}**")
                    if p.get('link'):
                        st.caption(f"[Ver producto]({p['link']})")
        else:
            st.warning("No se encontraron productos.")
            
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
EOFcd ~/mi-proyecto-ia
cat <<EOF > app.py
import streamlit as st
from main_orchestrator import start_and_return

st.set_page_config(page_title="Comparador IA", page_icon="🤖", layout="wide")

st.title("🤖 Comparador Inteligente de Laptops")
st.markdown("---")

# Input del usuario
query = st.text_input("¿Qué producto deseas comparar?", "Laptop Gamer")

if st.button("Ejecutar Análisis Multiagente"):
    # Quitamos el spinner para ver si hay errores inmediatos
    st.info(f"Iniciando búsqueda para: {query}...")
    
    try:
        # Llamamos directo a la función SIN caché
        productos, analisis = start_and_return(query)
        
        st.subheader("💡 Recomendación de la IA")
        if analisis:
            st.success(analisis)
        else:
            st.warning("La IA no devolvió un análisis.")
        
        st.subheader(f"📦 Resultados para: {query}")
        
        if productos:
            cols = st.columns(len(productos))
            for i, p in enumerate(productos):
                with cols[i]:
                    st.metric(label=p.get('source', 'Tienda'), value=f"${p.get('price', 0)}")
                    st.write(f"**{p.get('name', 'Producto')}**")
                    if p.get('link'):
                        st.caption(f"[Ver producto]({p['link']})")
        else:
            st.warning("No se encontraron productos.")
            
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
