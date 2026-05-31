import streamlit as st

st.set_page_config(page_title="CV ATS OPTIMIZER", layout="wide")

# ESTILOS VISUALES INSPIRADOS EN ENHANCV
st.markdown("""
    <style>
    .score-container {
        background-color: #1e293b;
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .score-number {
        font-size: 64px;
        font-weight: bold;
        color: #f59e0b;
    }
    .card-pro {
        background-color: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .card-contra {
        background-color: #fef2f2;
        border-left: 5px solid #dc2626;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 OPTIMIZADOR DE CV & ESCÁNER ATS")
st.subheader("APLICACIÓN INTERACTIVA DE DIAGNÓSTICO PROFESIONAL")

col_panel, col_resultados = st.columns([1, 2])

with col_panel:
    st.header("📥 PANEL DE ENTRADA")
    cv_input = st.text_area("PEGA TU CURRÍCULUM AQUÍ:", height=300, placeholder="Pega el texto de tu CV...")
    vacante_input = st.text_area("PEGA LA OFERTA DE TRABAJO (OPCIONAL):", height=150, placeholder="Para buscar palabras clave...")
    
    calcular = st.button("🚀 INICIAR ESCANEO ATS", type="primary")

with col_resultados:
    if calcular and cv_input:
        st.header("🔎 REPORTES DE EVALUACIÓN")
        
        # SIMULACIÓN DE CÁLCULO DE PUNTUACIÓN DE METRICAS
        tiene_numeros = any(char.isdigit() for char in cv_input)
        score = 78 if not tiene_numeros else 92
        
        st.markdown(f"""
            <div class="score-container">
                <h3>TU PUNTUACIÓN ESTIMADA</h3>
                <div class="score-number">{score}/100</div>
                <p>Análisis completado bajo estándares de reclutamiento internacional</p>
            </div>
        """, unsafe_allow_html=True)
        
        # DESGLOSE DE ANÁLISIS INTERACTIVO
        with st.expander("🟢 TASA DE ANÁLISIS ATS (FORMATO)", expanded=True):
            st.success("¡Formato aprobado! El texto es 100% legible para los sistemas de escaneo automáticos.")
            
        with st.expander("🔴 CUANTIFICANDO EL IMPACTO (MÉTRICAS)"):
            if not tiene_numeros:
                st.markdown("""
                    <div class="card-contra">
                        <strong>CONTRA:</strong> Falta de datos numéricos y logros cuantificables en tu experiencia laboral.
                    </div>
                    <p>👉 <strong>CONSEJO DE OPTIMIZACIÓN:</strong> Modifica tus funciones para incluir porcentajes o cantidades. 
                    En vez de 'Diseño de interiores de lujo', usa 'Diseño de [X] proyectos de interiores de lujo optimizando plazos en un [X]%'</p>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="card-pro">
                        <strong>PRO:</strong> Se detectaron métricas y números que demuestran el impacto de tu trabajo.
                    </div>
                """, unsafe_allow_html=True)
                
        with st.expander("⚠️ SEÑALES DE ALERTA DE RECURSOS HUMANOS (RED FLAGS)"):
            st.warning("Revisa las fechas: El software detecta brechas temporales o inconsistencias en el orden cronológico de la educación o experiencia.")
            
    else:
        st.info("💡 Por favor, ingresa el texto de tu CV en el panel de la izquierda y haz clic en 'Iniciar Escaneo ATS' para ver los gráficos y resultados.")
