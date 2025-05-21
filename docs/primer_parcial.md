Implementación de Modelos de Lenguaje de Gran Tamaño (LLM) en la resolución de problemas matemáticos

Integrantes:
Joaquin Zuviria
Kevin Gomez

Introducción
En el presente informe se documenta la evaluación inicial del uso de modelos de lenguaje de gran escala (LLM) ejecutados localmente, sin requerir conexión a servidores externos. Se utilizaron como herramientas principales la plataforma Ollama, y los modelos Llama 2 y Llama 3.2.
El objetivo de esta etapa es determinar la viabilidad técnica y funcional de correr LLMs en computadoras personales, analizar su rendimiento en tareas académicas, y comenzar a desarrollar una estrategia de documentación basada en resultados, prompting e iteración.
¿Por qué Ollama?
Se compararon dos plataformas de ejecución local de modelos de lenguaje: Ollama y LM Studio, ambas ampliamente utilizadas por la comunidad de desarrolladores de IA. La elección de Ollama como herramienta principal se justifica por los siguientes motivos:
Código abierto: Ollama es una plataforma de código abierto, lo que permite mayor transparencia, facilidad de implementación, posibilidad de auditoría y adaptación a necesidades específicas.


Facilidad de uso: Posee una interfaz de línea de comandos simple e intuitiva, y cuenta también con integración con interfaces gráficas y otras herramientas si se requiere.


Compatibilidad con múltiples modelos: Permite descargar y utilizar modelos como Llama, Mistral, Gemma, entre otros.


Instalación sencilla en Windows: El proceso de instalación en sistemas Windows es directo y bien documentado.


Requerimientos moderados: Puede correr modelos de tamaño razonable sin necesidad de una GPU de gama alta, aunque se recomienda disponer de al menos 8-16 GB de RAM para un rendimiento aceptable.
Instalación de Ollama en Windows
Para instalar Ollama en Windows se siguieron los siguientes pasos:
Acceso a la web oficial: https://ollama.com


Descarga del instalador para Windows.


Ejecución del instalador, que configura automáticamente el entorno y los servicios necesarios.


Verificación de la instalación desde la terminal con el comando ollama run llama2.


La instalación se completó sin inconvenientes. El software se ejecuta en segundo plano y permite la carga dinámica de modelos bajo demanda.

Modelos utilizados
Llama 2
Desarrollado por Meta AI.


Tamaño aproximado del modelo: 4 GB (cuantizado)


Buen desempeño general en razonamiento lógico y comprensión básica.


Llama 3.2
Versión más reciente y optimizada del mismo desarrollador.


Mejora la capacidad de contextualización y reducción de errores.


Ocupa mayor espacio en disco y demanda más recursos de sistema, aunque sigue siendo viable en hardware de gama media.







