# Proyecto 2025: LLM Local para resolución de rjercicios matemáticos

**Asignatura:** Probabilidad y Estadística (T4-17-17)

**Objetivo:** Evaluar la utilización de modelos de lenguaje (LLM) como herramienta de apoyo para resolver ejercicios de matemáticas, promoviendo el trabajo colaborativo y el desarrollo de competencias profesionales.

---

## 1. Organización del equipo

* **Coordinador/a:** Planifica reuniones, distribuye tareas y vela por el avance.
* **Comunicador/a:** Canaliza la comunicación con el docente y documenta las decisiones.
* **Integrantes (hasta 6):** Se reparten roles técnicos (prompt engineering, pruebas, documentación).

---

## 2. Fases del proyecto

| Fase        | Temas                        | Objetivos técnicos                                         |
| ----------- | ---------------------------- | ---------------------------------------------------------- |
| **Primera** | Contenido del primer parcial | - Instalar y configurar Ollama (u otra herramienta local). |

* Descargar y probar modelos matemáticos.
* Resolver ejercicios por prompts.
* Documentar precisión, tiempos y alucinaciones
* Comparar rendimiento en español e inglés.
* Recopilar métricas de hardware y performance.
* Analizar dinámica de equipo.
* Metodología y colaboración.
* Vinculación con resultados de aprendizaje.


---

## 3. Solución técnica paso a paso

### 3.1. Prerrequisitos

* macOS 10.15+ (o Linux/Windows con adaptaciones).
* Homebrew (en macOS) o gestor equivalente.
* Python 3.10+ para la API.

### 3.2. Instalación y configuración de Ollama

```bash
git clone <your-repo-url> proyecto-llm-matematicas
cd proyecto-llm-matematicas

# create & activate venv
python3 -m venv venv
source venv/bin/activate
```

### 3.3. Estructura de carpetas del proyecto

```bash
- prompts/: enunciados (.txt)
- outputs/: respuestas (.md)
- docs/: documentación
- api/: servicio HTTP
```

### 3.4. Primer experimento con CLI

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

### 3.5. API HTTP con FastAPI

#### 3.5.1. Dependencias (`api/requirements.txt`)

```text
fastapi
uvicorn[standard]
requests
pydantic
streamlit
```

#### 4. Virtual environment y arranque

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

## 6. Benchmarking comparativo: llama3.2 vs llama2

Para determinar cuál modelo funciona mejor como asistente matemático local, realiza los siguientes pasos:

### 6.1. Preparación de prompts

1. Identifica o crea un conjunto de ejercicios (5–10) en `prompts/`, nombrándolos como `benchmark_ej1.txt`, `benchmark_ej2.txt`, etc.
2. Asegúrate de que cada archivo contiene únicamente el enunciado del ejercicio.

### 6.2. Script de benchmarking (`benchmark.sh`)

Guarda este script en la raíz del proyecto y dale permisos de ejecución (`chmod +x benchmark.sh`):

Esta versión usa Python para medir milisegundos en macOS. Asegúrate de:

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


## 7. Interfaz de Usuario con Streamlit


![image](https://github.com/user-attachments/assets/27228ff6-cd08-49c7-a8e3-be546a0a5739)


### 7.3. Ejecutar la UI

1. Asegúrate que tu API esté corriendo en `localhost:8000`.
2. En la raíz del proyecto:

   ```bash
   streamlit run ui.py
   ```
3. Se abrirá automáticamente en tu navegador en `http://localhost:8501`.
