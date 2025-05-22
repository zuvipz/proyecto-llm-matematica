import streamlit as st
import requests
import pandas as pd
import time
import json
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

API_URL = "http://localhost:8000"

# Set page configuration
st.set_page_config(
    page_title="Asistente Matemático", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced custom CSS for better UI
st.markdown("""
<style>
    /* Improved chart styling */
    .stPlotlyChart {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Header styling */
    h1, h2, h3 {
        padding-top: 10px;
        padding-bottom: 10px;
        margin-top: 20px;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(250, 250, 250, 0.1);
    }
    
    /* Container styling */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 20px;
    }
    
    /* Button styling */
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    
    div.stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    /* Dataframe styling */
    .dataframe-container {
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 24px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: bold;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 4px;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        white-space: pre-wrap;
        border-radius: 4px 4px 0px 0px;
        padding-left: 20px;
        padding-right: 20px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    /* Container padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Success message styling */
    .success-message {
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Info message styling */
    .info-message {
        background-color: #2196F3;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with options
st.sidebar.title("🧮 Asistente Matemático")
page = st.sidebar.radio("Navegación", ["Individual", "Modo Test"])

# Initialize session state
if 'test_results' not in st.session_state:
    st.session_state.test_results = None
if 'last_test_time' not in st.session_state:
    st.session_state.last_test_time = None

# Function to get available models
def get_models():
    try:
        resp = requests.get(f"{API_URL}/models")
        resp.raise_for_status()
        data = resp.json()
        # Extract model IDs from the data structure returned by the API
        models = [model["id"].split(':')[0] for model in data["data"]]
        return models
    except Exception as e:
        st.error(f"Error al obtener modelos: {e}")
        return ["llama2", "llama3.2"]  # Default models if API fails

# Function to get available problems
def get_problems():
    try:
        resp = requests.get(f"{API_URL}/problems")
        resp.raise_for_status()
        return resp.json()["problems"]
    except Exception as e:
        st.error(f"Error al obtener problemas: {e}")
        return []

# Function to run batch test
def run_batch_test(models, problem_ids=None):
    try:
        payload = {"models": models}
        if problem_ids:
            payload["problem_ids"] = problem_ids
        
        with st.spinner("Ejecutando pruebas. Esto puede tardar varios minutos..."):
            start_time = time.time()
            resp = requests.post(f"{API_URL}/batch-test", json=payload, timeout=300)
            resp.raise_for_status()
            data = resp.json()
            end_time = time.time()
            
        # Store in session state
        st.session_state.test_results = data["results"]
        st.session_state.last_test_time = end_time - start_time
        
        return data["results"]
    except Exception as e:
        st.error(f"Error en la prueba por lotes: {e}")
        return None

# Individual page
if page == "Individual":
    st.title("🤖 Asistente Matemático Local")
    
    # Layout with two columns
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("Configuración")
        # Get models
        models = get_models()
        
        # Seleccionar modelo
        model = st.selectbox("Selecciona modelo", models)
        
        # Input de prompt
        enunciado = st.text_area("Ejercicio matemático", height=200)
        
        if st.button("Enviar al LLM", use_container_width=True):
            if not enunciado.strip():
                st.warning("Por favor ingresa un ejercicio.")
            else:
                payload = {"model": model, "prompt": enunciado}
                try:
                    with st.spinner("Obteniendo respuesta..."):
                        resp = requests.post(f"{API_URL}/run", json=payload, timeout=60)
                        resp.raise_for_status()
                        data = resp.json()
                        if 'response' not in st.session_state:
                            st.session_state.response = None
                        st.session_state.response = data.get("response", "Sin respuesta")
                except Exception as e:
                    st.error(f"Error en la petición: {e}")
    
    with col2:
        st.subheader("Respuesta")
        if 'response' in st.session_state and st.session_state.response:
            st.markdown(f"""<div style="background-color: rgba(255, 255, 255, 0.05); 
                          padding: 20px; border-radius: 10px; margin-top: 20px;">
                          {st.session_state.response}
                          </div>""", unsafe_allow_html=True)
        else:
            st.info("Envía un ejercicio para ver la respuesta aquí.")

# Test mode page
else:
    # Create a container to better control layout
    with st.container():
        st.title("🧪 Modo de prueba de modelos")
        
        # Main content in two columns with a better ratio
        col1, col2 = st.columns([5, 7])
        
        with col1:
            # Configuration card
            with st.container():
                st.subheader("Configuración")
                
                # Add some vertical space
                st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                
                # Get models and problems
                models = get_models()
                problems = get_problems()
                
                # Model selection
                selected_models = st.multiselect(
                    "Selecciona modelos a probar", 
                    models,
                    default=models[:2] if len(models) >= 2 else models
                )
                
                # Problem selection with better UI
                st.markdown("#### Selecciona problemas a probar:")
                st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
                
                # Create a container for problems
                problem_container = st.container()
                problem_selections = {}
                
                # Group problems by 5 per row
                with problem_container:
                    for i in range(0, len(problems), 5):
                        cols = st.columns(5)
                        for j in range(5):
                            if i+j < len(problems):
                                problem = problems[i+j]
                                with cols[j]:
                                    problem_selections[problem["id"]] = st.checkbox(
                                        f"{problem['id'].replace('benchmark_ej', '')}",
                                        value=True,
                                        help=problem["content"]
                                    )
                
                # Run test button with better styling
                st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                if st.button("Iniciar prueba", type="primary", use_container_width=True):
                    if not selected_models:
                        st.error("Por favor selecciona al menos un modelo.")
                    else:
                        # Get selected problem IDs
                        selected_problems = [pid for pid, selected in problem_selections.items() if selected]
                        
                        # Run the batch test
                        run_batch_test(selected_models, selected_problems)
                
                # Show visualizations in the left column if results are available
                if st.session_state.test_results:
                    # Convert results to DataFrame for easier display
                    results = st.session_state.test_results
                    
                    # Create summary DataFrame
                    summary_data = []
                    for r in results:
                        summary_data.append({
                            "Problema": r["problem_id"].replace("benchmark_ej", "Ejercicio "),
                            "Modelo": r["model"],
                            "Tiempo (ms)": r["time_ms"]
                        })
                    
                    df_summary = pd.DataFrame(summary_data)
                    
                    # Sort the DataFrame for better visualization
                    df_sorted = df_summary.sort_values(by=["Problema", "Modelo"])
                    
                    # Create a color map based on models
                    unique_models = df_sorted["Modelo"].unique()
                    colors = px.colors.qualitative.Plotly[:len(unique_models)]
                    color_map = {model: color for model, color in zip(unique_models, colors)}
                    
                    # Create visualization section with better styling
                    st.markdown("### Visualización de tiempos")
                    
                    # Create visualizations with tabs
                    tabs = st.tabs(["Barras", "Gantt", "Comparativa", "Radar"])
                    
                    with tabs[0]:
                        # Horizontal Bar Chart - simplified for left panel with better styling
                        fig = px.bar(
                            df_sorted,
                            x="Tiempo (ms)",
                            y="Problema",
                            color="Modelo",
                            orientation='h',
                            barmode='group',
                            height=500,
                            text="Tiempo (ms)",
                            color_discrete_map=color_map
                        )
                        fig.update_layout(
                            margin=dict(l=10, r=10, t=30, b=10),
                            yaxis={'categoryorder':'total ascending'},
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        fig.update_traces(
                            texttemplate='%{text:.0f}', 
                            textposition='outside',
                            hovertemplate='<b>%{y}</b><br>Tiempo: %{x} ms<extra></extra>'
                        )
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                        
                    with tabs[1]:
                        # Gantt Chart - simplified with better styling
                        gantt_data = []
                        reference_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                        
                        for model in unique_models:
                            model_data = df_sorted[df_sorted["Modelo"] == model]
                            current_time = reference_time
                            for _, row in model_data.iterrows():
                                start_time = current_time
                                end_time = start_time + pd.Timedelta(milliseconds=row["Tiempo (ms)"])
                                gantt_data.append({
                                    "Task": row["Problema"],
                                    "Start": start_time,
                                    "Finish": end_time,
                                    "Modelo": row["Modelo"],
                                    "Duración (ms)": row["Tiempo (ms)"]
                                })
                                current_time = end_time
                        
                        gantt_df = pd.DataFrame(gantt_data)
                        fig = px.timeline(
                            gantt_df, 
                            x_start="Start", 
                            x_end="Finish", 
                            y="Task",
                            color="Modelo",
                            hover_data=["Duración (ms)"],
                            color_discrete_map=color_map,
                            height=500
                        )
                        
                        fig.update_layout(
                            margin=dict(l=10, r=10, t=30, b=10),
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white')
                        )
                        # Add text annotations for duration
                        for i, row in enumerate(gantt_df.itertuples()):
                            fig.add_annotation(
                                x=(row.Start + (row.Finish - row.Start)/2),
                                y=row.Task,
                                text=f"{int(row._5)} ms",
                                showarrow=False,
                                font=dict(color="white", size=10)
                            )
                        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                    
                    with tabs[2]:
                        # Model comparison - improved styling
                        if len(unique_models) == 2:
                            model1, model2 = unique_models
                            df_pivot = df_summary.pivot(index="Problema", columns="Modelo", values="Tiempo (ms)").reset_index()
                            df_pivot["Diferencia (ms)"] = df_pivot[model1] - df_pivot[model2]
                            df_pivot["Más rápido"] = df_pivot.apply(
                                lambda row: model1 if row[model1] < row[model2] else model2, 
                                axis=1
                            )
                            
                            # Create a horizontal bar chart of time difference
                            fig = px.bar(
                                df_pivot.sort_values("Diferencia (ms)"),
                                x="Diferencia (ms)",
                                y="Problema",
                                color="Más rápido",
                                orientation='h',
                                text="Diferencia (ms)",
                                height=500,
                                color_discrete_map={model1: colors[0], model2: colors[1]}
                            )
                            fig.update_layout(
                                margin=dict(l=10, r=10, t=30, b=10),
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white')
                            )
                            fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
                            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                        else:
                            st.info("Se necesitan exactamente 2 modelos para la comparativa.")
                        
                    with tabs[3]:
                        # Radar chart - improved styling
                        if len(unique_models) > 1:
                            # Create pivot table
                            pivot = df_summary.pivot(index="Problema", columns="Modelo", values="Tiempo (ms)")
                            
                            # Normalize times to a 0-1 scale for better radar visualization
                            pivot_norm = pivot.copy()
                            for col in pivot_norm.columns:
                                max_val = pivot_norm[col].max()
                                pivot_norm[col] = pivot_norm[col] / max_val
                            
                            # Prepare radar chart
                            radar_fig = go.Figure()
                            categories = pivot_norm.index.tolist()
                            
                            for i, model in enumerate(unique_models):
                                values = pivot_norm[model].tolist()
                                values_radar = values + [values[0]]  # Close the loop
                                categories_radar = categories + [categories[0]]
                                
                                radar_fig.add_trace(go.Scatterpolar(
                                    r=values_radar,
                                    theta=categories_radar,
                                    fill='toself',
                                    name=model,
                                    line_color=colors[i]
                                ))
                            
                            radar_fig.update_layout(
                                polar=dict(
                                    radialaxis=dict(visible=True, range=[0, 1]),
                                    bgcolor='rgba(0,0,0,0)'
                                ),
                                height=500,
                                margin=dict(l=10, r=10, t=30, b=10),
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='white')
                            )
                            
                            st.plotly_chart(radar_fig, use_container_width=True, config={'displayModeBar': False})
                            st.info("Valores normalizados: menor = mejor rendimiento")
                        else:
                            st.info("Se necesitan al menos 2 modelos para el gráfico radar.")
        
        with col2:
            with st.container():
                st.subheader("Resultados")
                
                # Show results if available
                if st.session_state.test_results:
                    # Success message with custom styling
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ Prueba completada en {st.session_state.last_test_time:.2f} segundos
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Convert results to DataFrame for easier display
                    results = st.session_state.test_results
                    
                    # Create summary DataFrame
                    summary_data = []
                    for r in results:
                        summary_data.append({
                            "Problema": r["problem_id"].replace("benchmark_ej", "Ejercicio "),
                            "Modelo": r["model"],
                            "Tiempo (ms)": r["time_ms"]
                        })
                    
                    df_summary = pd.DataFrame(summary_data)
                    
                    # Display pivot table with better styling
                    st.markdown("#### Resumen de tiempos (ms):")
                    pivot = df_summary.pivot(index="Problema", columns="Modelo", values="Tiempo (ms)")
                    st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                    st.dataframe(pivot, use_container_width=True, height=300)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Add a speedup comparison if there are 2 models
                    if len(df_summary["Modelo"].unique()) == 2:
                        st.markdown("### Comparación de rendimiento")
                        
                        # Create a speedup DataFrame
                        model1, model2 = df_summary["Modelo"].unique()
                        df_pivot = df_summary.pivot(index="Problema", columns="Modelo", values="Tiempo (ms)").reset_index()
                        df_pivot["Proporción"] = df_pivot[model1] / df_pivot[model2]
                        df_pivot["Diferencia (ms)"] = df_pivot[model1] - df_pivot[model2]
                        df_pivot["Diferencia (%)"] = (df_pivot["Diferencia (ms)"] / df_pivot[model2] * 100).round(1)
                        df_pivot["Más rápido"] = df_pivot.apply(
                            lambda row: model1 if row[model1] < row[model2] else model2, 
                            axis=1
                        )
                        
                        # Display the comparison table with better styling
                        st.markdown("#### Tabla comparativa detallada:")
                        comparison_table = df_pivot[["Problema", model1, model2, "Diferencia (ms)", "Diferencia (%)", "Más rápido"]]
                        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                        st.dataframe(comparison_table, use_container_width=True, height=300)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display detailed results with expanders
                    st.markdown("### Respuestas detalladas:")
                    for r in results:
                        with st.expander(f"{r['problem_id'].replace('benchmark_ej', 'Ejercicio ')} - {r['model']} ({r['time_ms']} ms)"):
                            col_prompt, col_response = st.columns([1, 2])
                            with col_prompt:
                                st.markdown("**Enunciado:**")
                                st.markdown(f"""<div style="background-color: rgba(255, 255, 255, 0.05); 
                                            padding: 10px; border-radius: 5px;">
                                            {r["prompt"]}
                                            </div>""", unsafe_allow_html=True)
                            with col_response:
                                st.markdown("**Respuesta:**")
                                st.markdown(f"""<div style="background-color: rgba(255, 255, 255, 0.05); 
                                            padding: 10px; border-radius: 5px;">
                                            {r["response"]}
                                            </div>""", unsafe_allow_html=True)
                    
                    # Download results button with better styling
                    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
                    st.download_button(
                        "📥 Descargar resultados como JSON",
                        data=json.dumps(results, indent=2, ensure_ascii=False),
                        file_name="resultados_test.json",
                        mime="application/json",
                        use_container_width=True
                    )
                else:
                    # Info message with custom styling
                    st.markdown("""
                    <div class="info-message">
                        ℹ️ Ejecuta una prueba para ver los resultados aquí.
                    </div>
                    """, unsafe_allow_html=True)
