# Proyecto 2025: LLM Local para Resolución de Ejercicios Matemáticos

**Asignatura:** Probabilidad y Estadística (T4-17-17)

**Objetivo:** Evaluar la utilización de Modelos de Lenguaje de Gran Tamaño (LLM) como herramienta de apoyo para resolver ejercicios de matemáticas, promoviendo el trabajo colaborativo y el desarrollo de competencias profesionales.

---

## 1. Organización del equipo

* **Coordinador/a:** Planifica reuniones, distribuye tareas y vela por el avance.
* **Comunicador/a:** Canaliza la comunicación con el docente y documenta las decisiones.
* **Integrantes (hasta 6):** Se reparten roles técnicos (prompt engineering, pruebas, documentación).

> En caso de desbalance, se reestructuran los grupos; todos pueden retirarse antes del parcial sin impacto en notas.

---

## 2. Fases del proyecto

| Fase        | Temas                        | Objetivos técnicos                                         |
| ----------- | ---------------------------- | ---------------------------------------------------------- |
| **Primera** | Contenido del primer parcial | - Instalar y configurar Ollama (u otra herramienta local). |

* Descargar y probar modelos matemáticos.
* Resolver ejercicios por prompts.
* Documentar precisión, tiempos y alucinaciones. | | **Segunda**      | Contenido del segundo parcial      | - Resolver ejercicios y problemas vía imágenes (OCR + prompt).
* Comparar rendimiento en español e inglés.
* Recopilar métricas de hardware y performance.
* Analizar dinámica de equipo.              | | **Examen Final** | Presentación de resultados         | - Desafíos tecnológicos.
* Metodología y colaboración.
* Vinculación con resultados de aprendizaje. |

---

## 3. Consentimiento informado

```txt
Título: Implementación de LLM en resolución de problemas matemáticos

- **Actividad:** Resolución de ejercicios y documentación de ingeniería de prompts.
- **Beneficios:** Sustitución de parciales, desarrollo de competencias y posible publicación.
- **Riesgos:** Dependencia tecnológica y necesidad de rigor académico.
- **Voluntariedad:** Retiro posible hasta el parcial sin efecto en notas.
```

---

## 4. Solución Técnica Paso a Paso

### 4.1. Prerrequisitos

* macOS 10.15+ (o Linux/Windows con adaptaciones).
* Homebrew (en macOS) o gestor equivalente.
* Python 3.10+ para la API.

### 4.2. Instalación y configuración de Ollama

```bash
#!/usr/bin/env bash
set -euo pipefail

# Modelos a comparar
declare -a MODELOS=("llama2" "llama3.2")
OUTPUT_DIR="outputs/benchmark"
mkdir -p "$OUTPUT_DIR"

# Encabezado CSV de tiempos
echo "ejercicio,modelo,tiempo_ms" > "$OUTPUT_DIR/tiempos.csv"

for modelo in "${MODELOS[@]}"; do
  echo "Benchmarking con $modelo..."
  for archivo in prompts/benchmark_ej*.txt; do
    nombre=$(basename "$archivo" .txt)
    # Timestamp en milisegundos usando Python para compatibilidad macOS
    inicio=$(python3 - << 'PYCODE'
import time; print(int(time.time() * 1000))
PYCODE
)
    ollama run "$modelo" < "$archivo" > "$OUTPUT_DIR/${nombre}_${modelo}.md"
    fin=$(python3 - << 'PYCODE'
import time; print(int(time.time() * 1000))
PYCODE
)
    dur=$((fin - inicio))
    echo "$nombre,$modelo,$dur" >> "$OUTPUT_DIR/tiempos.csv"
  done
done
```

### 4.3. Estructura de carpetas del proyecto

```bash
cd ~/Documents
mkdir proyecto-llm-matematicas && cd proyecto-llm-matematicas

git init
mkdir prompts outputs docs api
cat << 'EOF' > README.md
# Proyecto LLM Matemáticas

- prompts/: enunciados (.txt)
- outputs/: respuestas (.md)
- docs/: documentación
- api/: servicio HTTP
EOF
```

### 4.4. Primer experimento con CLI

```bash
# Enunciado de prueba
cat << 'EOF' > prompts/ej1_probabilidad.txt
Resuelve: Si tiro dos dados, ¿probabilidad de sumar 7?
EOF

# Ejecución y cronometraje
time ollama run llama2 < prompts/ej1_probabilidad.txt > outputs/ej1_probabilidad.md

# Revisión
echo "--- Response ---" && cat outputs/ej1_probabilidad.md
```

Registra en `docs/primer_parcial.md`:

```markdown
# Resultados Primer Parcial

| Ejercicio                 | Modelo  | Precisión | Tiempo (s) | Observaciones            |
|---------------------------|---------|-----------|------------|--------------------------|
| Suma de dos dados = 7    | llama2  | Sí        | 0.8        | Correcto, sin alucinaciones |
```

### 4.5. API HTTP con FastAPI

#### 4.5.1. Dependencias (`api/requirements.txt`)

```text
fastapi
uvicorn[standard]
requests
pydantic
```

#### 4.5.2. Código del servidor (`api/main.py`)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

OLLAMA_HOST = "http://127.0.0.1:11434"

class RunRequest(BaseModel):
    model: str
    prompt: str

app = FastAPI(title="API LLM Matemáticas", version="0.1.0")

@app.get("/models")
def list_models():
    try:
        r = requests.get(f"{OLLAMA_HOST}/v1/models")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/run")
def run_prompt(req: RunRequest):
    payload = {"model": req.model, "messages": [{"role":"user","content":req.prompt}]}
    try:
        r = requests.post(f"{OLLAMA_HOST}/v1/chat/completions", json=payload)
        r.raise_for_status()
        return {"response": r.json()["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(500, str(e))
```

#### 4.5.3. Virtual environment y arranque

```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> Documenta en `docs/api.md` las respuestas de `/models` y `/run`.

---

## 5. Próximos ejercicios y métricas

1. **Segunda etapa**: prompts por imagen (OCR + prompt).
2. **Comparativa**: español vs inglés.
3. **Hardware**: documentar CPU/RAM/GPU.
4. **Rendimiento**: latencia, throughput y tasa de alucinaciones.

---

## 6. Benchmarking comparativo: llama3.2 vs llama2

Para determinar cuál modelo funciona mejor como asistente matemático local, realiza los siguientes pasos:

### 6.1. Preparación de prompts

1. Identifica o crea un conjunto de ejercicios (5–10) en `prompts/`, nombrándolos como `benchmark_ej1.txt`, `benchmark_ej2.txt`, etc.
2. Asegúrate de que cada archivo contiene únicamente el enunciado del ejercicio.

### 6.2. Script de benchmarking (`benchmark.sh`)

Guarda este script en la raíz del proyecto y dale permisos de ejecución (`chmod +x benchmark.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail

# Modelos a comparar
MODELOS=("llama2" "llama3.2")
OUTPUT_DIR="outputs/benchmark"
mkdir -p "$OUTPUT_DIR"

# Crear encabezado CSV de tiempos
echo "ejercicio,modelo,tiempo_ms" > "$OUTPUT_DIR/tiempos.csv"

# Iterar modelos y archivos de prompt
for modelo in "${MODELOS[@]}"; do
  echo "Benchmarking con $modelo..."
  for archivo in prompts/benchmark_ej*.txt; do
    # Nombre base (ej: benchmark_ej1)
    nombre=$(basename "$archivo" .txt)
    # Marca inicio en ms
    inicio=$(python3 - << 'PYCODE'
import time
print(int(time.time() * 1000))
PYCODE
)
    # Ejecutar prompt
    ollama run "$modelo" < "$archivo" > "$OUTPUT_DIR/${nombre}_${modelo}.md"
    # Marca fin en ms
    fin=$(python3 - << 'PYCODE'
import time
print(int(time.time() * 1000))
PYCODE
)
    # Calcular duración
    dur=$((fin - inicio))
    # Anotar en CSV
    echo "$nombre,$modelo,$dur" >> "$OUTPUT_DIR/tiempos.csv"
  done
done
```

Esta versión usa Python para medir milisegundos de manera confiable en macOS. Asegúrate de:

* Haber creado los archivos `prompts/benchmark_ej1.txt` … `prompts/benchmark_ej5.txt` dentro de la carpeta `prompts/`.
* Ejecutar el script desde la raíz del proyecto.

### 6.3. Recopilar resultados

Recopilar resultados

1. Ejecuta el script:

   ```bash
   ./benchmark.sh
   ```
2. Abre `outputs/benchmark/tiempos.csv` para ver los tiempos en milisegundos.
3. Revisa en `outputs/benchmark/*.md` las respuestas generadas.
4. Crea `docs/benchmark_modelos.md` con una tabla:

   | Ejercicio                                                                                                         | Modelo   | Tiempo (ms) | Precisión | Observaciones |
   | ----------------------------------------------------------------------------------------------------------------- | -------- | ----------- | --------- | ------------- |
   | ej1                                                                                                               | llama2   | 1234        | Sí/No     | ...           |
   | ej1                                                                                                               | llama3.2 | 987         | Sí/No     | ...           |
   | Completa la columna **Precisión** evaluando si la respuesta es correcta y añade comentarios en **Observaciones**. |          |             |           |               |

---

> Con este benchmark podrás decidir cuál modelo local ofrece el mejor equilibrio entre velocidad y precisión para tu asistente de matemáticas.

1. **Segunda etapa**: prompts por imagen (OCR + prompt).
2. **Comparativa**: español vs inglés.
3. **Hardware**: documentar CPU/RAM/GPU.
4. **Rendimiento**: latencia, throughput y tasa de alucinaciones.

---

> Con esta guía tienes todo el flujo desde la concepción del proyecto hasta la implementación y pruebas. ¡Manos a la obra!

---

## 7. Interfaz de Usuario con Streamlit

Para facilitar la interacción con tu API de FastAPI, puedes crear una UI sencilla usando Streamlit.

### 7.1. Dependencias

En la raíz del proyecto, crea o actualiza `requirements.txt` para incluir:

```text
streamlit
requests
```

Instala en tu virtualenv principal (no en `api/.venv`):

```bash
pip install streamlit requests
```

### 7.2. Archivo `ui.py`

Crea `ui.py` en la carpeta raíz con este contenido:

```python
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
```

### 7.3. Ejecutar la UI

1. Asegúrate que tu API esté corriendo en `localhost:8000`.
2. En la raíz del proyecto:

   ```bash
   streamlit run ui.py
   ```
3. Se abrirá automáticamente en tu navegador en `http://localhost:8501`.

¡Listo! Ahora tienes una interfaz visual para probar tu asistente matemático local.
