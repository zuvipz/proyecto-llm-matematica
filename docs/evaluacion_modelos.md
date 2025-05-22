# Evaluación Comparativa de Modelos LLM

## Configuración de la prueba

- **Fecha:** 22/05/2025 09:01
- **Modelos probados:** llama2, llama3.2
- **Número de problemas:** 2
- **Especificaciones de hardware:** 
  - CPU: arm
  - RAM: 16.0 GB
  - GPU: Apple M2 Pro
  - Sistema: Darwin 24.4.0

## Resultados de tiempos

| Problema | llama2 (ms) | llama3.2 (ms) | Diferencia (ms) | Diferencia (%) |
|----------|---------------|---------------|---------------|---------------|
| Ejercicio 1 | 8137 | 6793 | 1344 | 19.8% |
| Ejercicio 2 | 4060 | 3445 | 615 | 17.9% |
| **Promedio** | 6098.5 | 5119.0 | 979.5 | 18.8% |

## Evaluación de calidad

### Criterios de evaluación
- **Correcto:** La respuesta es matemáticamente correcta.
- **Paso a paso:** La respuesta explica el proceso de solución de forma clara.
- **Notación:** La respuesta utiliza notación matemática adecuada.
- **Completo:** La respuesta aborda todos los aspectos del problema.

| # | Problema | Descripción | llama2 | llama3.2 | Notas |
|---|----------|-------------|----------|----------|-------|
| 1 | Probabilidad dados | Calcular probabilidad de suma 7 al tirar dos dados | |  |  |
| 2 | Integral | Calcular la integral ∫₀¹ x² dx | |  |  |

## Conclusiones

[Enumerar las conclusiones principales sobre el rendimiento de los modelos]

## Recomendaciones

[Recomendaciones sobre qué modelo utilizar para diferentes tipos de problemas]
