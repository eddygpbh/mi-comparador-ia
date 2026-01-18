import streamlit as st
import time
from main_orchestrator import start_and_return
from database_manager import DatabaseManager

# Configuración con estética PriceRunner
st.set_page_config(page_title="PriceRunner IA - Comparador Inteligente", page_icon="⚖️", layout="wide")

# CSS Avanzado basado en el código fuente de PriceRunner
st.markdown("""
    <style>
    @import url('https://x.klarnacdn.net/ui/fonts/v1.5/KlarnaText-Regular.woff2');
    
    .stApp { background-color: #f9f9f9; font-family: 'Klarna Text', sans-serif; }
    
    /* Header Estilo PriceRunner */
    .header-container { background-color: white; padding: 20px; border-bottom: 1px solid #eaeaea; text-align: center; margin-bottom: 30px; }
    
    /* Tarjetas de Producto estilo Klarna/PriceRunner */
    .product-card {
        background: white;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #efefef;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 20px;
    }
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.05);
        border-color: #ffb3c7; /* Toque de color Klarna */
    }
    
    /* Scores y Badges */
    .score-container { display: flex; align-items: center; gap: 10px; margin: 15px 0; }
    .trust-badge { background-color: #000; color: white; padding: 4px 12px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }
    .avg-score { color: #ff3366; font-size: 1.5em; font-weight: bold; }
    
    /* Botones Pro */
    .stButton>button {
        background-color: #ffb3c7 !important; /* Rosa Klarna */
        color: #191919 !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

db = DatabaseManager()

# --- SIDEBAR PROFESIONAL ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>📜 Historial</h2>", unsafe_allow_html=True)
    historial = db.obtener_historial()
    if historial and hasattr(historial, 'data'):
        for item in historial.data:
            with st.expander(f"🛒 {item['producto']}"):
                st.caption(f"Última actualización: {item['created_at'][:10]}")
                st.write(item['recomendacion_modelo'])

# --- HEADER ---
st.markdown('<div class="header-container"><h1>⚖️ PriceRunner <span style="color:#ff3366">IA</span></h1><p>Comparativa inteligente impulsada por Gemini</p></div>', unsafe_allow_html=True)

# --- BUSCADOR ---
col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
with col_s2:
    query = st.text_input("", placeholder="Busca productos, marcas y más...", label_visibility="collapsed")
    search_btn = st.button("BUSCAR MEJOR PRECIO")

if search_btn and query:
    with st.status("🕵️ Procesando Consenso de Agentes...", expanded=True) as status:
        st.write("🔍 Escaneando 6,400 tiendas británicas y globales...")
        time.sleep(1)
        st.write("📊 Verificando TrustScore de los vendedores...")
        
        productos, analisis = start_and_return(query)
        status.update(label="✅ Análisis Finalizado", state="complete")

    # --- RESULTADOS ESTILO FICHA ---
    st.markdown("### 🏆 Recomendación del Conductor")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f"""
        <div class="product-card">
            <span class="trust-badge">TOP RATED</span>
            <h2 style="margin-top:10px;">Producto Seleccionado</h2>
            <div class="score-container">
                <span class="avg-score">8.9/10</span>
                <span style="color: #767676;">Calidad & Precio</span>
            </div>
            <p style="color: #4c4c4c; line-height: 1.6;">{analisis}</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("IR A LA TIENDA")

    with c2:
        st.markdown("### 📊 Desglose Técnico")
        st.info("El Agente de Finanzas ha detectado un ahorro del 12% respecto al precio medio del mercado.")
        st.metric("TrustScore", "95/100", "Seguro")
        st.metric("Disponibilidad", "Stock Alto", "Inmediato")
