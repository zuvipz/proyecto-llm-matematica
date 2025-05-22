from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import time
from typing import List, Dict, Any, Optional

OLLAMA_HOST = "http://127.0.0.1:11434"

# Esquema de petición para generar un prompt
class RunRequest(BaseModel):
    model: str
    prompt: str

class BatchTestRequest(BaseModel):
    models: List[str]
    problem_ids: Optional[List[str]] = None  # If None, test all problems

class TestResult(BaseModel):
    problem_id: str
    model: str
    prompt: str
    response: str
    time_ms: int

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

@app.get("/problems")
def list_problems():
    """Lista todos los problemas disponibles para testing."""
    try:
        prompts_dir = "../prompts"  # Ruta relativa a donde se ejecuta la API
        problems = []
        for file in os.listdir(prompts_dir):
            if file.startswith("benchmark_ej") and file.endswith(".txt"):
                problem_id = file.replace(".txt", "")
                with open(os.path.join(prompts_dir, file), "r") as f:
                    content = f.read().strip()
                problems.append({
                    "id": problem_id,
                    "content": content
                })
        return {"problems": sorted(problems, key=lambda x: x["id"])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-test")
def batch_test(req: BatchTestRequest):
    """Ejecuta un lote de problemas en múltiples modelos y devuelve los resultados."""
    try:
        # Obtener la lista de problemas
        prompts_dir = "../prompts"
        if req.problem_ids:
            problem_files = [f"benchmark_ej{id.split('benchmark_ej')[-1]}.txt" 
                            if id.startswith("benchmark_ej") else f"benchmark_ej{id}.txt" 
                            for id in req.problem_ids]
        else:
            problem_files = [f for f in os.listdir(prompts_dir) 
                            if f.startswith("benchmark_ej") and f.endswith(".txt")]
        
        results = []
        
        for model in req.models:
            for file in problem_files:
                problem_path = os.path.join(prompts_dir, file)
                if not os.path.exists(problem_path):
                    continue
                
                with open(problem_path, "r") as f:
                    prompt = f.read().strip()
                
                # Ejecutar el prompt y medir tiempo
                start_time = time.time() * 1000
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                }
                resp = requests.post(
                    f"{OLLAMA_HOST}/v1/chat/completions",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                resp.raise_for_status()
                data = resp.json()
                end_time = time.time() * 1000
                
                # Extraer el contenido de la respuesta
                content = data["choices"][0]["message"]["content"]
                problem_id = file.replace(".txt", "")
                
                results.append(TestResult(
                    problem_id=problem_id,
                    model=model,
                    prompt=prompt,
                    response=content,
                    time_ms=int(end_time - start_time)
                ))
        
        return {"results": [r.dict() for r in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
