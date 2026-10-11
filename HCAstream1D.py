import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración inicial de la página
st.set_page_config(page_title="Laboratorio de Hidráulica Avanzado", layout="wide")
st.title("🌊 Laboratorio Virtual: Energía, Fuerza y Perfiles de Remanso (FGV)")
st.sidebar.title("Módulos Didácticos")

tema = st.sidebar.radio(
    "Selecciona el tema a explicar:",
    [
        "1. Energía Específica", 
        "2. Fuerza Específica y Resalto", 
        "3. Clasificación de Perfiles (M, S, C, H, A)",
        "4. Simulación de Perfil Longitudinal con Obstáculo"
    ]
)

g = 9.81

# =============================================================================
# TEMA 1: ENERGÍA ESPECÍFICA
# =============================================================================
if tema == "1. Energía Específica":
    st.header("1. Concepto de Energía Específica (E)")
    st.markdown("La energía específica mide la energía por unidad de peso con respecto al fondo del canal: $E = y + \\frac{Q^2}{2g B^2 y^2}$")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Parámetros del Canal")
        Q = st.slider("Caudal Q (m³/s)", 0.5, 20.0, 5.0, step=0.5)
        B = st.slider("Ancho de solera B (m)", 1.0, 10.0, 3.0, step=0.5)
        
        yc = (Q**2 / (g * B**2))**(1/3)
        Emin = 1.5 * yc
        st.success(f"**Tirante Crítico (yc):** {yc:.3f} m")
        st.info(f"**Energía Mínima (Emin):** {Emin:.3f} m")

    with col2:
        y = np.linspace(0.05, yc * 3, 300)
        E = y + (Q**2) / (2 * g * (B**2) * (y**2))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=E, y=y, mode='lines', name='Curva E vs y', line=dict(color='#1f77b4', width=3)))
        fig.add_trace(go.Scatter(x=E, y=E, mode='lines', name='Asintota y = E', line=dict(dash='dash', color='gray')))
        fig.add_trace(go.Scatter(x=[Emin], y=[yc], mode='markers+text', text=["Punto Crítico"], textposition="top right", marker=dict(color='red', size=10)))
        
        fig.update_layout(
            xaxis_title="Energía Específica, E (m)", yaxis_title="Tirante, y (m)",
            xaxis=dict(range=[0, Emin*2.5]), yaxis=dict(range=[0, yc*3]), template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TEMA 2: FUERZA ESPECÍFICA Y RESALTO
# =============================================================================
elif tema == "2. Fuerza Específica y Resalto":
    st.header("2. Fuerza Específica o Función Momentum (M)")
    st.markdown("Se conserva antes y después de un resalto hidráulico ($M_1 = M_2$): $M = \\frac{Q^2}{g B y} + \\frac{B y^2}{2}$")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Variables Hidráulicas")
        Q = st.slider("Caudal Q (m³/s)", 1.0, 15.0, 4.0, step=0.5)
        B = st.slider("Ancho B (m)", 1.0, 5.0, 2.0, step=0.5)
        
        yc = (Q**2 / (g * B**2))**(1/3)
        
        st.subheader("Simulación de Resalto")
        y1 = st.slider("Tirante Supercrítico Inicial y1 (m)", 0.05, float(yc)*0.9, float(yc)*0.5, step=0.02)
        fr1 = (Q / (B * y1)) / np.sqrt(g * y1)
        y2 = (y1 / 2) * (np.sqrt(1 + 8 * fr1**2) - 1)
        st.success(f"**Tirante Conjugado y2 (Subcrítico):** {y2:.3f} m")

    with col2:
        y = np.linspace(0.05, yc * 3, 300)
        M = (Q**2) / (g * B * y) + (B * y**2) / 2
        M1 = (Q**2) / (g * B * y1) + (B * y1**2) / 2
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=M, y=y, mode='lines', name='Curva M vs y', line=dict(color='#2ca02c', width=3)))
        fig.add_trace(go.Scatter(x=[M1, M1], y=[y1, y2], mode='markers+text', text=["y1 (Supercrítico)", "y2 (Subcrítico)"], textposition=["bottom right", "top right"], marker=dict(color='orange', size=10)))
        fig.add_trace(go.Scatter(x=[M1, M1], y=[y1, y2], mode='lines', name='Resalto', line=dict(dash='dot', color='orange')))
        
        fig.update_layout(xaxis_title="Fuerza Específica, M (m³)", yaxis_title="Tirante, y (m)", xaxis=dict(range=[0, M1*2]), template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TEMA 3: CLASIFICACIÓN DE PERFILES DIDÁCTICOS (NUEVO MÓDULO)
# =============================================================================
elif tema == "3. Clasificación de Perfiles (M, S, C, H, A)":
    st.header("3. Generador Didáctico de Curvas de Remanso")
    st.markdown("""
    Los perfiles se clasifican según la pendiente del canal (**M**ild, **S**teep, **C**ritical, **H**orizontal, **A**dverse) y la zona donde se encuentra el tirante real ($y$) con respecto al tirante normal ($y_n$) y crítico ($y_c$).
    """)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Control de Pendiente Teórica")
        tipo_pendiente = st.selectbox(
            "Selecciona el tipo de pendiente a estudiar:",
            ["M (Suave: yn > yc)", "S (Fuerte: yc > yn)", "C (Crítica: yn = yc)", "H (Horizontal: S0 = 0)", "A (Adversa: S0 < 0)"]
        )
        
        # Valores pedagógicos asignados para ilustrar los límites de zona abiertamente
        if "M" in tipo_pendiente:
            yn, yc = 2.0, 1.0
            info_text = "**Pendiente Suave (M):** Flujo subcrítico en régimen uniforme. Se generan perfiles M1, M2 y M3."
        elif "S" in tipo_pendiente:
            yn, yc = 0.6, 1.4
            info_text = "**Pendiente Fuerte (S):** Flujo supercrítico en régimen uniforme. Se generan perfiles S1, S2 y S3."
        elif "C" in tipo_pendiente:
            yn, yc = 1.2, 1.2
            info_text = "**Pendiente Crítica (C):** El tirante normal coincide con el crítico. Genera perfiles C1 y C3."
        elif "H" in tipo_pendiente:
            yn, yc = np.inf, 1.1
            info_text = "**Pendiente Horizontal (H):** El tirante normal tiende al infinito (no hay flujo uniforme). Genera perfiles H2 y H3."
        else:
            yn, yc = -1, 1.1  # Representación virtual
            info_text = "**Pendiente Adversa (A):** El fondo del canal sube en el sentido del flujo. Genera perfiles A2 y A3."

        st.info(info_text)
        st.subheader("Introducir condición de borde inicial")
        y_inicial = st.slider("Tirante inicial en la sección de control, y (m)", 0.2, 3.0, 1.5, step=0.1)
        
        # Identificación automática de la Zona de trabajo
        if yn == -1 or yn == np.inf: # Casos H y A
            zona = "Zona 2" if y_inicial > yc else "Zona 3"
            nombre_perfil = f"{tipo_pendiente[0]}{zona[-1]}"
        else:
            max_y = max(yn, yc)
            min_y = min(yn, yc)
            if y_inicial > max_y:
                zona = "Zona 1 (y > yn y y > yc)"
                nombre_perfil = f"{tipo_pendiente[0]}1"
            elif min_y < y_inicial <= max_y:
                zona = "Zona 2 (Intermedia)"
                nombre_perfil = f"{tipo_pendiente[0]}2"
            else:
                zona = "Zona 3 (y < yn y y < yc)"
                nombre_perfil = f"{tipo_pendiente[0]}3"
        
        st.write(f"📍 El tirante seleccionado se encuentra en la **{zona}**.")
        st.success(f"📈 Perfil teórico resultante esperado: **Curva {nombre_perfil}**")

    with col2:
        # Dibujo didáctico del espacio de fases del perfil
        x = np.linspace(0, 100, 100)
        fig = go.Figure()
        
        # Dibujar líneas de referencia (Línea de Tirante Normal y Crítico)
        if yn != -1 and yn != np.inf:
            fig.add_trace(go.Scatter(x=x, y=[yn]*100, mode='lines', name='Línea Normal (yn)', line=dict(color='green', dash='dash')))
        fig.add_trace(go.Scatter(x=x, y=[yc]*100, mode='lines', name='Línea Crítica (yc)', line=dict(color='red', dash='dot')))
        
        # Generar una curva sintética cualitativa que refleje la pendiente real de la ecuación diferencial (dy/dx)
        # Resuelve cualitativamente la tendencia del perfil seleccionado para los alumnos
        if "1" in nombre_perfil:
            # Curvas tipo 1 crecen aguas abajo o se elevan
            y_curva = np.linspace(y_inicial, y_inicial + 0.4, 100)
        elif "2" in nombre_perfil:
            # Curvas tipo 2 caen hacia el tirante menor
            y_curva = np.linspace(y_inicial, y_inicial - 0.3, 100) if y_inicial > min(yn, yc) else np.linspace(y_inicial, y_inicial + 0.2, 100)
        else:
            # Curvas tipo 3 crecen desde el fondo hacia la línea crítica/normal
            y_curva = np.linspace(y_inicial, y_inicial + 0.3, 100)

        fig.add_trace(go.Scatter(x=x, y=y_curva, mode='lines', name=f'Perfil Real Simulada ({nombre_perfil})', line=dict(color='blue', width=4)))
        fig.add_trace(go.Scatter(x=[0], y=[y_inicial], mode='markers', name='Condición de Contorno', marker=dict(color='black', size=12)))
        
        fig.update_layout(title=f"Comportamiento de la curva de remanso {nombre_perfil}", xaxis_title="Distancia a lo largo del Canal (m)", yaxis_title="Espesor / Tirante del agua (m)", template="plotly_white", yaxis=dict(range=[0, 3.5]))
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TEMA 4: SIMULACIÓN LONGITUDINAL CON OBSTÁCULO (METODO DEL PASO)
# =============================================================================
elif tema == "4. Simulación de Perfil Longitudinal con Obstáculo":
    st.header("4. Simulación de Flujo Gradualmente Variado (Paso Estándar)")
    st.markdown("Cálculo numérico del perfil del agua cuando se encuentra con un vertedero o sobreelevación del fondo del canal.")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Configuración Física")
        S0 = st.number_input("Pendiente del canal (S0)", value=0.001, format="%.4f")
        n = st.number_input("Rugosidad de Manning (n)", value=0.015, format="%.3f")
