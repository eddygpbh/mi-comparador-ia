import streamlit as st
import time
from main_orchestrator import start_and_return
from database_manager import DatabaseManager

st.set_page_config(page_title="PriceRunner IA - Real", page_icon="⚖️", layout="wide")

# --- ESTILOS CSS (Manteniendo tu diseño Premium) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    .stApp { background: linear-gradient(135deg, #f0f2f6 0%, #e6e9f0 100%); font-family: 'Inter', sans-serif; }
    .header-container { background-color: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); padding: 25px; border-bottom: 1px solid rgba(0,0,0,0.05); text-align: center; margin-bottom: 30px; border-radius: 0 0 20px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }
    .product-card { background: white; padding: 15px; border-radius: 16px; border: 1px solid rgba(0,0,0,0.05); text-align: center; transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.02); height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
    .product-card:hover { transform: translateY(-5px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); border-color: #ffb3c7; }
    .price-tag { color: #ff3366; font-size: 1.2em; font-weight: 800; margin: 10px 0; }
    .trust-score-mini { background-color: #1d1d1f; color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.7em; font-weight: 600; }
    .verdict-card { background-color: #ffffff; border-left: 6px solid #10b981; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-top: 20px; color: #1f2937; }
    .verdict-title { color: #047857; font-size: 1.2em; font-weight: 800; margin-bottom: 10px; }
    img { border-radius: 8px; object-fit: cover; height: 150px; width: 100%; margin-bottom: 10px; }
    a { text-decoration: none; }
    </style>
    """, unsafe_allow_html=True)

db = DatabaseManager()

# --- HEADER ---
st.markdown('<div class="header-container"><h1 style="color:#111827; margin:0; font-weight:800;">⚖️ PriceRunner <span style="color:#ff3366">IA</span></h1><p style="color:#6b7280; margin-top:5px;">Búsqueda Global en Tiempo Real</p></div>', unsafe_allow_html=True)

col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
with col_s2:
    query = st.text_input("", placeholder="Ej: PlayStation 5 Slim...", label_visibility="collapsed")
    search_btn = st.button("ANALIZAR OFERTAS REALES", type="primary", use_container_width=True)

if search_btn and query:
    with st.status("🧠 Activando Protocolo de Búsqueda...", expanded=True) as status:
        st.write(f"🌍 DuckDuckGo Agent: Rastreando web por '{query}'...")
        
        # LLAMADA REAL AL ORQUESTADOR
        productos_reales, analisis = start_and_return(query)
        
        if not productos_reales:
            st.error("No se encontraron productos. Intenta ser más específico.")
            status.update(label="❌ Búsqueda fallida", state="error")
        else:
            st.write("📸 Descargando imágenes de productos...")
            time.sleep(1) # Pequeña pausa dramática para UX
            status.update(label="✅ Datos Recolectados Exitosamente", state="complete", expanded=False)

            st.markdown(f"<h3 style='margin: 30px 0 20px 0; color:#111827;'>🎯 Resultados Encontrados: <span style='color:#ff3366'>{len(productos_reales)}</span></h3>", unsafe_allow_html=True)
            
            # --- VITRINA REAL ---
            # Renderizamos filas de 5 en 5
            for i in range(0, len(productos_reales), 5):
                cols = st.columns(5)
                batch = productos_reales[i:i+5]
                for j, p in enumerate(batch):
                    with cols[j]:
                        # Truncamos el título si es muy largo
                        titulo_corto = (p['nombre'][:50] + '...') if len(p['nombre']) > 50 else p['nombre']
                        
                        st.markdown(f"""
                        <div class="product-card">
                            <img src="{p['imagen']}" onerror="this.src='https://via.placeholder.com/200?text=Sin+Imagen'">
                            <div><span class="trust-score-mini">TRUST: {p['score']}</span></div>
                            <h5 style="color:#374151; font-size:0.85em; margin: 10px 0; height: 40px; overflow: hidden;">{titulo_corto}</h5>
                            <p class="price-tag">{p['precio']}</p>
                            <a href="{p['link']}" target="_blank">
                                <button style="background:#ffb3c7; border:none; border-radius:20px; padding:8px 16px; font-weight:bold; cursor:pointer; width:100%;">VER OFERTA</button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

            # --- DICTAMEN ---
            st.markdown("---")
            st.markdown(f"""
            <div class="verdict-card">
                <div class="verdict-title">📝 Dictamen del Conductor</div>
                <div style="font-size: 1.05em; line-height: 1.6; color: #374151;">{analisis}</div>
            </div>
            """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 📜 Historial")
    db.obtener_historial()
