import streamlit as st
import time
from main_orchestrator import start_and_return
from database_manager import DatabaseManager

st.set_page_config(page_title="PriceRunner IA - Premium", page_icon="⚖️", layout="wide")

# CSS Moderno: Fondo Gradiente Suave + Sombras Profundas
st.markdown("""
    <style>
    /* Fondo moderno y atractivo */
    .stApp {
        background: linear-gradient(135deg, #f0f2f6 0%, #e6e9f0 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header estilizado */
    .header-container {
        background-color: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        text-align: center;
        margin-bottom: 40px;
        border-radius: 0 0 20px 20px;
    }
    
    /* Tarjetas de Producto con elevación */
    .product-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: none;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        height: 100%;
    }
    .product-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
    }
    
    .price-tag { 
        color: #ff3366; 
        font-size: 1.4em; 
        font-weight: 800; 
        margin: 12px 0; 
    }
    
    .trust-score-mini { 
        background: linear-gradient(45deg, #2c3e50, #000000); 
        color: white; 
        padding: 4px 12px; 
        border-radius: 6px; 
        font-size: 0.75em;
        letter-spacing: 0.5px;
    }

    /* Input de búsqueda estilizado */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #ddd !important;
        padding: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

db = DatabaseManager()

# --- HEADER ---
st.markdown('<div class="header-container"><h1 style="color:#1d1d1f; font-weight:800;">⚖️ PriceRunner <span style="color:#ff3366">IA</span></h1><p style="color:#6e6e73;">Comparación de élite en tiempo real</p></div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
with col_s2:
    query = st.text_input("", placeholder="Busca productos con inteligencia...", label_visibility="collapsed")
    search_btn = st.button("GENERAR TOP 10 PREMIUM")

if search_btn and query:
    with st.status("🧠 Analizando patrones de precios...", expanded=True) as status:
        st.write("🕵️ Agentes inspeccionando stocks globales...")
        productos_simulados = [
            {"id": i, "nombre": f"Modelo Pro {i+1}", "precio": 120 + (i*22), "score": 99 - i}
            for i in range(10)
        ]
        _, analisis = start_and_return(query)
        status.update(label="✅ Consenso de Calidad Alcanzado", state="complete")

    st.markdown(f"<h3 style='text-align:center; margin: 40px 0;'>🎯 Selección de Élite para: {query}</h3>", unsafe_allow_html=True)
    
    # --- VITRINA TOP 10 ---
    for row in range(2):
        cols = st.columns(5)
        for i in range(5):
            idx = (row * 5) + i
            p = productos_simulados[idx]
            with cols[i]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="https://picsum.photos/seed/{p['id']+100}/300/300" width="100%" style="border-radius:12px;">
                    <div style="margin: 15px 0;">
                        <span class="trust-score-mini">TRUST: {p['score']}%</span>
                    </div>
                    <h5 style="color:#1d1d1f; font-size:1em; min-height:50px;">{p['nombre']}</h5>
                    <p class="price-tag">${p['precio']}.00</p>
                </div>
                """, unsafe_allow_html=True)
                st.button("Ver Oferta", key=f"btn_{idx}", use_container_width=True)

    st.markdown("---")
    with st.container():
        st.markdown("### 📝 Dictamen del Conductor")
        st.success(analisis)

# --- SIDEBAR ---
with st.sidebar:
    st.header("📜 Misiones")
    db.obtener_historial()
