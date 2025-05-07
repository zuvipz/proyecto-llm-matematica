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
