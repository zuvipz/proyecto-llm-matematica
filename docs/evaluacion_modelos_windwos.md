# Evaluación Comparativa de Modelos LLM

## Configuración de la prueba

- **Fecha:** 24/05/2025 21:30
- **Modelos probados:** llama2, llama3.2
- **Número de problemas:** 30
- **Especificaciones de hardware:** 
  - CPU: Ryzen 5 3600 6-Core Processor
  - RAM: 23.93 GB
  - GPU: NVIDIA GeForce GTX 1060 6GB
  - VRAM: 1349.00 MB
  - Sistema: Windows 10

## Resultados de tiempos

| Problema | llama2 | llama3.2 | Diferencia (ms) | Diferencia (%) |
|----------|----------|----------|----------------|----------------|
| Ejercicio 1 ESP| 31223.0 | 17107.0 | 14116.0 | 82.5% |
| Ejercicio 2 ESP| 90548.0 | 8489.0 | 82059.0 | 966.7% |
| Ejercicio 3 ESP| 65131.0 | 23898.0 | 41233.0 | 172.5% |
| Ejercicio 4 ESP| 43636.0 | 13807.0 | 29829.0 | 216.0% |
| Ejercicio 5 ESP| 39475.0 | 20273.0 | 19202.0 | 94.7% |
| Ejercicio 6 ESP| 13552.0 | 14543.0 | -991.0 | -6.8% |
| Ejercicio 7 ESP| 31286.0 | 23192.0 | 8094.0 | 34.9% |
| Ejercicio 8 ESP| 22635.0 | 14042.0 | 8593.0 | 61.2% |
| Ejercicio 9 ESP| 16996.0 | 31702.0 | -14706.0 | -46.4% |
| Ejercicio 10 ESP| 32890.0 | 13669.0 | 19221.0 | 140.6% |
| Ejercicio 11 ESP| 21608.0 | 44626.0 | -23018.0 | -51.6% |
| Ejercicio 12 ESP| 19931.0 | 31767.0 | -11836.0 | -37.3% |
| Ejercicio 13 ESP| 49178.0 | 11621.0 | 37557.0 | 323.2% |
| Ejercicio 14 ESP| 8565.0 | 11727.0 | -3162.0 | -27.0% |
| Ejercicio 15 ESP| 42118.0 | 16088.0 | 26030.0 | 161.8% |
| Ejercicio 1 ENG| 9614.0 | 8520.0 | 1094.0 | 12.8% |
| Ejercicio 2 ENG| 55402.0 | 9049.0 | 46353.0 | 512.2% |
| Ejercicio 3 ENG| 44298.0 | 13307.0 | 30991.0 | 232.9% |
| Ejercicio 4 ENG| 46701.0 | 26394.0 | 20307.0 | 76.9% |
| Ejercicio 5 ENG| 27051.0 | 38335.0 | -11284.0 | -29.4% |
| Ejercicio 6 ENG| 12180.0 | 11406.0 | 774.0 | 6.8% |
| Ejercicio 7 ENG| 28751.0 | 9824.0 | 18927.0 | 192.7% |
| Ejercicio 8 ENG| 16771.0 | 8026.0 | 8745.0 | 109.0% |
| Ejercicio 9 ENG| 15743.0 | 12994.0 | 2749.0 | 21.2% |
| Ejercicio 10 ENG| 26147.0 | 21461.0 | 4686.0 | 21.8% |
| Ejercicio 11 ENG| 20465.0 | 16061.0 | 4404.0 | 27.4% |
| Ejercicio 12 ENG| 26056.0 | 5578.0 | 20478.0 | 367.1% |
| Ejercicio 13 ENG| 23287.0 | 9497.0 | 13790.0 | 145.2% |
| Ejercicio 14 ENG| 27179.0 | 14987.0 | 12192.0 | 81.4% |
| Ejercicio 15 ENG| 33148.0 | 10110.0 | 23038.0 | 227.9% |

## Evaluación de calidad

### Criterios de evaluación
- **Correcto:** La respuesta es matemáticamente correcta.
- **Paso a paso:** La respuesta explica el proceso de solución de forma clara.
- **Notación:** La respuesta utiliza notación matemática adecuada.
- **Completo:** La respuesta aborda todos los aspectos del problema.

| # | Problema | Descripción | llama2 | llama3.2 | Notas |
|---|----------|-------------|----------|----------|-------|
| 1 ESP | Probabilidad dados | Calcular probabilidad de suma 7 al tirar dos dados | |  |  |
| 2 ESP | Integral | Calcular la integral ∫₀¹ x² dx | |  |  |
| 3 ESP | Números primos | Contar números primos entre 1 y 100 | |  |  |
| 4 ESP | Ecuación diferencial | Resolver dy/dx = 3x² con y(0)=5 | |  |  |
| 5 ESP | Física | Calcular tiempo para recorrer 180 km a 72 km/h | |  |  |
| 6 ESP | Álgebra | Desarrollar la expresión (2x - 3)² | |  |  |
| 7 ESP | Probabilidad | Probabilidad de extraer 2 bolas del mismo color | |  |  |
| 8 ESP | Sistema ecuaciones | Resolver sistema 3x+2y=7, 5x-y=4 | |  |  |
| 9 ESP | Derivada | Calcular derivada de f(x) = x³ln(x) - 2x² | |  |  |
| 10 ESP | Geometría | Verificar triángulo rectángulo y calcular área | |  |  |
| 11 ESP |  |  | |  |  |
| 12 ESP |  |  | |  |  |
| 13 ESP |  |  | |  |  |
| 14 ESP |  |  | |  |  |
| 15 ESP |  |  | |  |  |
| 1 ENG |  |  | |  |  |
| 2 ENG |  |  | |  |  |
| 3 ENG |  |  | |  |  |
| 4 ENG |  |  | |  |  |
| 5 ENG |  |  | |  |  |
| 6 ENG |  |  | |  |  |
| 7 ENG |  |  | |  |  |
| 8 ENG |  |  | |  |  |
| 9 ENG |  |  | |  |  |
| 10 ENG |  |  | |  |  |
| 11 ENG |  |  | |  |  |
| 12 ENG |  |  | |  |  |
| 13 ENG |  |  | |  |  |
| 14 ENG |  |  | |  |  |
| 15 ENG |  |  | |  |  |

## Conclusiones

[Enumerar las conclusiones principales sobre el rendimiento de los modelos]

## Recomendaciones

[Recomendaciones sobre qué modelo utilizar para diferentes tipos de problemas]