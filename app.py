import streamlit as st
import time
from main_orchestrator import start_and_return
from database_manager import DatabaseManager

st.set_page_config(page_title="PriceRunner IA - Premium", page_icon="⚖️", layout="wide")

# CSS Moderno y Corrección de Contrastes
st.markdown("""
    <style>
    /* Tipografía Global */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f0f2f6 0%, #e6e9f0 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header estilizado */
    .header-container {
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 30px;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }
    
    /* Tarjetas de Producto */
    .product-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        height: 100%;
    }
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.1);
        border-color: #ffb3c7;
    }
    
    .price-tag { 
        color: #ff3366; 
        font-size: 1.3em; 
        font-weight: 800; 
        margin: 10px 0; 
    }
    
    .trust-score-mini { 
        background-color: #1d1d1f; 
        color: white; 
        padding: 4px 10px; 
        border-radius: 6px; 
        font-size: 0.7em;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* --- NUEVO: Tarjeta de Dictamen (Alta Legibilidad) --- */
    .verdict-card {
        background-color: #ffffff;
        border-left: 6px solid #10b981; /* Verde esmeralda fuerte */
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-top: 20px;
        color: #1f2937; /* Gris muy oscuro para texto */
    }
    
    .verdict-title {
        color: #047857;
        font-size: 1.2em;
        font-weight: 800;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .verdict-text {
        font-size: 1.05em;
        line-height: 1.6;
        color: #374151; /* Gris oscuro legible */
    }

    /* Input de búsqueda */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #e5e7eb !important;
        padding: 12px !important;
        font-size: 1em;
    }
    </style>
    """, unsafe_allow_html=True)

db = DatabaseManager()

# --- HEADER ---
st.markdown('<div class="header-container"><h1 style="color:#111827; margin:0; font-weight:800;">⚖️ PriceRunner <span style="color:#ff3366">IA</span></h1><p style="color:#6b7280; margin-top:5px;">Comparación inteligente de precios y calidad</p></div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
with col_s2:
    query = st.text_input("", placeholder="Ej: iPhone 15 Pro Max 256GB...", label_visibility="collapsed")
    search_btn = st.button("ANALIZAR OFERTAS", type="primary", use_container_width=True)

if search_btn and query:
    with st.status("🧠 Orquestando agentes inteligentes...", expanded=True) as status:
        st.write("🕵️ Rastreando historial de precios (30 días)...")
        st.write("🛡️ Filtrando vendedores con TrustScore bajo...")
        
        # Simulación de datos para la vitrina
        productos_simulados = [
            {"id": i, "nombre": f"Opción Premium {i+1}", "precio": 120 + (i*22), "score": 99 - i}
            for i in range(10)
        ]
        
        # Llamada real a la IA
        _, analisis = start_and_return(query)
        status.update(label="✅ Análisis Completado", state="complete", expanded=False)

    st.markdown(f"<h3 style='margin: 30px 0 20px 0; color:#111827;'>🎯 Top 10 Hallazgos para: <span style='color:#ff3366'>{query}</span></h3>", unsafe_allow_html=True)
    
    # --- VITRINA (GRID) ---
    for row in range(2):
        cols = st.columns(5)
        for i in range(5):
            idx = (row * 5) + i
            p = productos_simulados[idx]
            with cols[i]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="https://picsum.photos/seed/{p['id']+55}/300/300" width="100%" style="border-radius:12px; margin-bottom:10px;">
                    <div><span class="trust-score-mini">TRUST: {p['score']}</span></div>
                    <h5 style="color:#374151; font-size:0.95em; margin: 10px 0; min-height:45px;">{p['nombre']}</h5>
                    <p class="price-tag">${p['precio']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.button("Ver Oferta", key=f"btn_{idx}", use_container_width=True)

    # --- DICTAMEN OFICIAL (CORREGIDO) ---
    st.markdown("---")
    st.markdown(f"""
    <div class="verdict-card">
        <div class="verdict-title">
            📝 Dictamen del Conductor
        </div>
        <div class="verdict-text">
            {analisis}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 📜 Historial Reciente")
    db.obtener_historial()
