import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Asistente Matemático", layout="centered")
st.title("🤖 Asistente Matemático Local")

# Seleccionar modelo
model = st.selectbox("Selecciona modelo", ["llama2", "llama3.2"])

# Input de prompt
enunciado = st.text_area("Ejercicio matemático", height=150)

if st.button("Enviar al LLM"):
    if not enunciado.strip():
        st.warning("Por favor ingresa un ejercicio.")
    else:
        payload = {"model": model, "prompt": enunciado}
        try:
            with st.spinner("Obteniendo respuesta..."):
                resp = requests.post(f"{API_URL}/run", json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                st.subheader("Respuesta del modelo:")
                st.write(data.get("response", "Sin respuesta"))
        except Exception as e:
            st.error(f"Error en la petición: {e}")
