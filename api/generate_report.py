#!/usr/bin/env python3
"""
Script para generar un reporte de evaluación de modelos a partir de los resultados JSON de pruebas.
"""
import json
import pandas as pd
import argparse
import os
from datetime import datetime
import platform
import psutil
import subprocess

def get_system_info():
    """Obtiene información del sistema para incluir en el reporte."""
    cpu = platform.processor()
    if not cpu:
        cpu = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True).strip().decode()
    
    ram = round(psutil.virtual_memory().total / (1024**3), 2)
    
    # Intentar obtener información de GPU si está disponible
    gpu = "No disponible"
    try:
        if platform.system() == "Darwin":  # macOS
            gpu_info = subprocess.check_output("system_profiler SPDisplaysDataType | grep Chipset", shell=True).strip().decode()
            if gpu_info:
                gpu = gpu_info.split(":")[1].strip()
        elif platform.system() == "Linux":
            gpu_info = subprocess.check_output("lspci | grep -i 'vga\|3d\|2d'", shell=True).strip().decode()
            if gpu_info:
                gpu = gpu_info.split(":")[-1].strip()
    except:
        pass
    
    return {
        "cpu": cpu,
        "ram": f"{ram} GB",
        "gpu": gpu,
        "system": platform.system(),
        "release": platform.release()
    }

def generate_report(results_file, output_file):
    """Genera un reporte Markdown a partir de un archivo JSON de resultados."""
    # Cargar resultados
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Convertir a DataFrame para fácil manipulación
    df = pd.DataFrame(results)
    
    # Obtener modelos únicos
    models = df['model'].unique()
    
    # Crear un DataFrame pivotado para los tiempos
    times_df = df.pivot(index='problem_id', columns='model', values='time_ms')
    
    # Calcular diferencias si hay dos modelos
    if len(models) == 2:
        times_df['diff'] = times_df[models[0]] - times_df[models[1]]
        times_df['diff_percent'] = (times_df['diff'] / times_df[models[1]] * 100).round(1)
    
    # Ordenar los problemas por número
    problem_order = sorted(times_df.index, key=lambda x: int(x.replace('benchmark_ej', '')))
    times_df = times_df.reindex(problem_order)
    
    # Calcular promedios
    averages = times_df.mean().round(1)
    
    # Preparar el informe
    system_info = get_system_info()
    
    # Iniciar el reporte
    report = [
        "# Evaluación Comparativa de Modelos LLM",
        "",
        "## Configuración de la prueba",
        "",
        f"- **Fecha:** {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"- **Modelos probados:** {', '.join(models)}",
        f"- **Número de problemas:** {len(problem_order)}",
        "- **Especificaciones de hardware:** ",
        f"  - CPU: {system_info['cpu']}",
        f"  - RAM: {system_info['ram']}",
        f"  - GPU: {system_info['gpu']}",
        f"  - Sistema: {system_info['system']} {system_info['release']}",
        "",
        "## Resultados de tiempos",
        ""
    ]
    
    # Generar tabla de tiempos
    if len(models) == 1:
        time_table = ["| Problema | {} (ms) |".format(models[0]),
                     "|----------|---------------|"]
                     
        for problem in problem_order:
            problem_name = f"Ejercicio {problem.replace('benchmark_ej', '')}"
            time_table.append(f"| {problem_name} | {times_df.loc[problem, models[0]]} |")
        
        time_table.append(f"| **Promedio** | {averages[models[0]]} |")
    
    else:  # Dos o más modelos
        headers = [models[0], models[1], "Diferencia (ms)", "Diferencia (%)"] if len(models) == 2 else models
        time_table = ["| Problema | " + " | ".join(f"{m} (ms)" for m in models) + (
            " | Diferencia (ms) | Diferencia (%) |" if len(models) == 2 else " |"),
                     "|----------|" + "---------------|" * len(models) + (
            "---------------|---------------|" if len(models) == 2 else "")]
                     
        for problem in problem_order:
            problem_name = f"Ejercicio {problem.replace('benchmark_ej', '')}"
            row = f"| {problem_name} |"
            for model in models:
                row += f" {times_df.loc[problem, model]} |"
            
            if len(models) == 2:
                row += f" {times_df.loc[problem, 'diff']} | {times_df.loc[problem, 'diff_percent']}% |"
            
            time_table.append(row)
        
        # Agregar fila de promedios
        avg_row = "| **Promedio** |"
        for model in models:
            avg_row += f" {averages[model]} |"
        
        if len(models) == 2:
            avg_row += f" {averages['diff']} | {averages['diff_percent']}% |"
        
        time_table.append(avg_row)
    
    report.extend(time_table)
    report.extend([
        "",
        "## Evaluación de calidad",
        "",
        "### Criterios de evaluación",
        "- **Correcto:** La respuesta es matemáticamente correcta.",
        "- **Paso a paso:** La respuesta explica el proceso de solución de forma clara.",
        "- **Notación:** La respuesta utiliza notación matemática adecuada.",
        "- **Completo:** La respuesta aborda todos los aspectos del problema.",
        ""
    ])
    
    # Tabla de problemas para evaluación manual
    problem_descriptions = {
        "benchmark_ej1": "Probabilidad dados | Calcular probabilidad de suma 7 al tirar dos dados",
        "benchmark_ej2": "Integral | Calcular la integral ∫₀¹ x² dx",
        "benchmark_ej3": "Números primos | Contar números primos entre 1 y 100",
        "benchmark_ej4": "Ecuación diferencial | Resolver dy/dx = 3x² con y(0)=5",
        "benchmark_ej5": "Física | Calcular tiempo para recorrer 180 km a 72 km/h",
        "benchmark_ej6": "Álgebra | Desarrollar la expresión (2x - 3)²",
        "benchmark_ej7": "Probabilidad | Probabilidad de extraer 2 bolas del mismo color",
        "benchmark_ej8": "Sistema ecuaciones | Resolver sistema 3x+2y=7, 5x-y=4",
        "benchmark_ej9": "Derivada | Calcular derivada de f(x) = x³ln(x) - 2x²",
        "benchmark_ej10": "Geometría | Verificar triángulo rectángulo y calcular área"
    }
    
    quality_headers = [model for model in models]
    quality_table = [
        "| # | Problema | Descripción | " + " | ".join(quality_headers) + " | Notas |",
        "|---|----------|-------------|" + "----------|" * len(models) + "-------|"
    ]
    
    for problem in problem_order:
        problem_num = problem.replace("benchmark_ej", "")
        problem_type, description = problem_descriptions.get(problem, "|").split("|")
        row = f"| {problem_num} | {problem_type.strip()} | {description.strip()} |"
        for _ in models:
            row += " | "  # Celdas vacías para evaluación manual
        row += " |"
        quality_table.append(row)
    
    report.extend(quality_table)
    report.extend([
        "",
        "## Conclusiones",
        "",
        "[Enumerar las conclusiones principales sobre el rendimiento de los modelos]",
        "",
        "## Recomendaciones",
        "",
        "[Recomendaciones sobre qué modelo utilizar para diferentes tipos de problemas]"
    ])
    
    # Escribir el reporte
    with open(output_file, 'w') as f:
        f.write("\n".join(report))
    
    print(f"Reporte generado en {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera un informe de evaluación a partir de resultados JSON")
    parser.add_argument("results_file", help="Archivo JSON con los resultados de las pruebas")
    parser.add_argument("-o", "--output", default="../docs/evaluacion_modelos.md",
                        help="Archivo de salida para el reporte (por defecto: ../docs/evaluacion_modelos.md)")
    args = parser.parse_args()
    
    generate_report(args.results_file, args.output) 