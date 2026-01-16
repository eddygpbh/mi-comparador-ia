import st_supabase_connection as st_supabase
import streamlit as st

class DatabaseManager:
    def __init__(self):
        try:
            self.conn = st.connection("supabase", type=st_supabase.SupabaseConnection)
        except Exception as e:
            st.error(f"Error de conexión a base de datos: {e}")

    def guardar_consulta(self, producto, analisis, modelo):
        try:
            data = {
                "producto": producto,
                "analisis": analisis,
                "recomendacion_modelo": modelo
            }
            self.conn.table("consultas_ia").insert(data).execute()
        except Exception as e:
            print(f"No se pudo guardar en el historial: {e}")

    def obtener_historial(self):
        try:
            return self.conn.table("consultas_ia").select("*").order("created_at", desc=True).limit(5).execute()
        except:
            return None
