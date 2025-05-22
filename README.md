# Asistente Matemático con LLMs Locales

Este proyecto implementa un sistema para evaluar modelos de lenguaje (LLMs) locales en la resolución de problemas matemáticos. Utilizando [Ollama](https://ollama.ai/) como motor de ejecución, permite comparar diferentes modelos como Llama 2 y Llama 3.2 en su capacidad para resolver problemas matemáticos.

![Vista previa](https://github.com/user/repo/assets/preview.png)

## Características principales

- 🧮 **Resolución de problemas matemáticos** usando LLMs locales
- 📊 **Visualizaciones comparativas** de rendimiento entre modelos
- 🔍 **Análisis detallado** de tiempos de respuesta y precisión
- 📱 **Interfaz web** para fácil interacción con los modelos
- 📈 **Generación de reportes** para análisis cualitativos

## Instalación rápida

### Prerrequisitos

- Python 3.8+
- [Ollama](https://ollama.ai/) instalado con modelos llama2 y llama3.2

### Pasos de instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/user/proyecto-llm-matematicas.git
   cd proyecto-llm-matematicas
   ```

2. Crear y activar entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # o
   .venv\Scripts\activate     # Windows
   ```

3. Instalar dependencias:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

## Uso

### Iniciar el servidor API

```bash
cd api
source .venv/bin/activate  # Si no está activado
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Iniciar la interfaz web

En una nueva terminal:

```bash
cd api
source .venv/bin/activate
streamlit run ui.py
```

La interfaz web se abrirá automáticamente en `http://localhost:8501`.

## Modos de uso

### Modo Individual

- Selecciona un modelo
- Escribe un problema matemático
- Obtén la respuesta al instante

### Modo Test

- Selecciona múltiples modelos para comparar
- Elige entre 10 problemas matemáticos predefinidos
- Visualiza resultados con gráficos comparativos:
  - Barras horizontales por problema
  - Diagrama de Gantt de tiempos
  - Gráfico de radar para patrones de rendimiento
  - Comparativa directa entre modelos

## Generación de reportes

Después de ejecutar pruebas, puedes generar un reporte detallado:

1. Descarga los resultados JSON desde la UI
2. Ejecuta el generador de reportes:
   ```bash
   cd api
   python generate_report.py ruta/a/resultados_test.json -o ../docs/mi_evaluacion.md
   ```

El reporte incluirá:
- Información del sistema (CPU, RAM, GPU)
- Comparativa de tiempos entre modelos
- Plantilla para evaluar la calidad de las respuestas

## Problemas matemáticos incluidos

El sistema incluye 10 problemas matemáticos que cubren:

1. Probabilidad básica (suma de dados)
2. Cálculo - integrales
3. Teoría de números (conteo de primos)
4. Ecuaciones diferenciales
5. Problemas de física - cinemática
6. Desarrollo de expresiones algebraicas
7. Probabilidad avanzada
8. Sistemas de ecuaciones lineales
9. Cálculo - derivadas
10. Geometría (triángulos)

## Estructura del proyecto

```
proyecto-llm-matematicas/
├── api/                # Servidor FastAPI y UI de Streamlit
│   ├── main.py         # API REST para interactuar con Ollama
│   ├── ui.py           # Interfaz de usuario con Streamlit
│   ├── generate_report.py # Generador de reportes de evaluación
│   └── requirements.txt # Dependencias del proyecto
├── prompts/            # Problemas matemáticos predefinidos
│   ├── benchmark_ej1.txt
│   └── ...
├── outputs/            # Almacenamiento de resultados
│   └── benchmark/      # Resultados de comparativas
├── docs/               # Documentación y reportes
└── README.md           # Este archivo
```

## Contribuciones

Las contribuciones son bienvenidas. Puedes:
- Añadir nuevos problemas matemáticos en `prompts/`
- Mejorar las visualizaciones en `api/ui.py`
- Añadir soporte para nuevos modelos

## Licencia

Este proyecto está disponible bajo la licencia MIT.
