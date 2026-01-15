from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

print("--- Listando modelos disponibles ---")
for m in client.models.list():
    # Imprimimos el diccionario completo del modelo para ver sus claves reales
    print(f"Modelo encontrado: {m.name}")
