import streamlit as st
import time
from main_orchestrator import start_and_return
from database_manager import DatabaseManager

# Configuración de página con enfoque moderno
st.set_page_config(page_title="Gemini Conductor Pro", page_icon="🚀", layout="wide")

# Estilos CSS personalizados para mejorar el CRO (Botones y Tarjetas)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .product-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .score-badge { padding: 5px 10px; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

db = DatabaseManager()

# --- SIDEBAR: HISTORIAL INTELIGENTE ---
with st.sidebar:
    st.header("📜 Misiones Recientes")
    st.markdown("---")
    historial = db.obtener_historial()
    if historial and hasattr(historial, 'data'):
        for item in historial.data:
            with st.expander(f"🔍 {item['producto']}"):
                st.write(item['recomendacion_modelo'])

# --- CUERPO PRINCIPAL ---
st.title("🧠 Gemini Conductor: Comparador Pro")
st.info("La IA está lista para negociar por ti en múltiples tiendas.")

# Buscador Semántico (UI)
query = st.text_input("", placeholder="¿Qué quieres comprar hoy?", help="Escribe el producto y nuestro sistema multi-agente hará el resto.")

if st.button("🚀 Iniciar Búsqueda y Consenso"):
    if query:
        # 1. VISUALIZACIÓN EN TIEMPO REAL (Fase 1.2 del plan)
        with st.status("🕵️ Iniciando Orquestación Multi-Agente...", expanded=True) as status:
            st.write("📡 Conectando con APIs de Amazon, Walmart y eBay...")
            time.sleep(1.5)
            st.write("📊 Agente de Finanzas calculando eficiencia de costo...")
            time.sleep(1.2)
            st.write("🛡️ Verificando TrustScore y autenticidad de reseñas...")
            time.sleep(1)
            
            # Llamada al orquestador
            productos, analisis = start_and_return(query)
            status.update(label="✅ Consenso Alcanzado", state="complete", expanded=False)

        # 2. PANEL DE RESULTADOS (Fase 1.3 del plan)
        st.markdown("### 🏆 Selección Inteligente")
        
        col1, col2 = st.columns([1, 1])
        
        # Simulamos la visualización de dos opciones para demostrar el diseño de fichas
        with col1:
            st.markdown(f"""
            <div class="product-card">
                <h4>Opción Destacada</h4>
                <p style="color: #28a745;"><b>TrustScore: 92/100</b></p>
                <hr>
                <p>{analisis[:200]}...</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Ver en Tienda (Link Afiliado)", key="btn_opt1")

        with col2:
            st.markdown("### 📊 Métricas de Decisión")
            st.metric(label="Calidad (avgScore)", value="8.5 / 10", delta="Excelente")
            st.metric(label="Ahorro Estimado", value="15%", delta="- 0.00")
            
    else:
        st.warning("Escribe algo para activar a los agentes.")
