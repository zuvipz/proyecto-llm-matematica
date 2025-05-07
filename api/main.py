from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

OLLAMA_HOST = "http://127.0.0.1:11434"

# Esquema de petición para generar un prompt
class RunRequest(BaseModel):
    model: str
    prompt: str

app = FastAPI(
    title="API Proyecto LLM",
    description="Servicio que envuelve Ollama para ejecutar prompts",
    version="0.1.0"
)

@app.get("/models")
def list_models():
    """Lista los modelos disponibles en Ollama."""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/v1/models")
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run")
def run_prompt(req: RunRequest):
    """Ejecuta un prompt con un modelo y devuelve la respuesta."""
    payload = {
        "model": req.model,
        "messages": [{"role": "user", "content": req.prompt}]
    }
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        resp.raise_for_status()
        data = resp.json()
        # Extraer el contenido de la primera respuesta
        content = data["choices"][0]["message"]["content"]
        return {"response": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
