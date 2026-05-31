import streamlit as st
from pypdf import PdfReader

# Configuración de página con estilo oscuro premium
st.set_page_config(page_title="Optimizador de CV & Escáner ATS", layout="wide")

# Título Principal
st.title("📊 OPTIMIZADOR DE CV & ESCÁNER ATS")
st.subheader("APLICACIÓN INTERACTIVA DE DIAGNÓSTICO PROFESIONAL")

# Diseño de columnas para la interfaz
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown("### 📥 PANEL DE ENTRADA")
    
    # Selector del formato en el que se ingresará el CV
    metodo_entrada = st.radio("Selecciona cómo deseas ingresar tu CV:", ("Cargar archivo (PDF, DOCX, TXT)", "Pegar texto manualmente"))
    
    texto_cv = ""
    
    if metodo_entrada == "Cargar archivo (PDF, DOCX, TXT)":
        archivo_cargado = st.file_uploader("Arrastra o selecciona tu currículum:", type=["pdf", "docx", "txt"])
        
        if archivo_cargado is not None:
            nombre_archivo = archivo_cargado.name.lower()
            
            # Procesar archivo PDF
            if nombre_archivo.endswith('.pdf'):
                try:
                    lector_pdf = PdfReader(archivo_cargado)
                    paginas_texto = [pagina.extract_text() for pagina in lector_pdf.pages if pagina.extract_text()]
                    texto_cv = "\n".join(paginas_texto)
                    st.success(f"✅ ¡PDF leído con éxito! ({len(lector_pdf.pages)} páginas)")
                except Exception as e:
                    st.error("Error al procesar el archivo PDF. Asegúrate de que no esté protegido o dañado.")
            
            # Procesar archivo TXT
            elif nombre_archivo.endswith('.txt'):
                try:
                    texto_cv = archivo_cargado.read().decode("utf-8")
                    st.success("✅ ¡Archivo de texto leído con éxito!")
                except Exception as e:
                    st.error("Error al leer el archivo de texto.")
            
            # Procesar archivo DOCX (Word)
            elif nombre_archivo.endswith('.docx'):
                # Nota: Para leer DOCX de forma nativa en entornos complejos se requiere docx2txt. 
                # Como alternativa limpia y ligera, leemos los metadatos de texto planos legibles.
                try:
                    import zipfile
                    import xml.etree.ElementTree as ET
                    with zipfile.ZipFile(archivo_cargado) as docx:
                        arbol_xml = ET.fromstring(docx.read('word/document.xml'))
                        namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                        parrafos = [nodo.text for nodo in arbol_xml.iter() if nodo.tag.endswith('t')]
                        texto_cv = "".join(parrafos)
                    st.success("✅ ¡Documento Word leído con éxito!")
                except Exception as e:
                    st.error("Error al procesar el archivo Word. Intenta guardarlo como PDF o TXT.")
                    
    else:
        texto_cv = st.text_area("PEGA TU CURRÍCULUM AQUÍ:", placeholder="Pega el texto de tu CV...", height=300)

    # Espacio para las palabras clave del puesto al que aspiras
    palabras_puesto = st.text_area("🎯 PALABRAS CLAVE O DESCRIPCIÓN DEL PUESTO:", placeholder="Pega los requerimientos del trabajo o las palabras clave aquí...", height=150)
    
    boton_escanear = st.button("Iniciar Escaneo ATS", type="primary")

with col2:
    st.markdown("### 📈 PANEL DE RESULTADOS")
    
    if boton_escanear:
        if not texto_cv:
            st.warning("⚠️ Por favor, carga un archivo válido o pega el texto de tu CV en el panel de la izquierda.")
        elif not palabras_puesto:
            st.warning("⚠️ Por favor, ingresa las palabras clave o la descripción del puesto para comparar.")
        else:
            with st.spinner("Analizando compatibilidad estructural..."):
                # Limpieza básica para la simulación
                palabras_cv = set(texto_cv.lower().split())
                palabras_filtro = set(palabras_puesto.lower().replace(",", " ").replace(";", " ").split())
                
                # Filtrado de conectores cortos
                palabras_filtro = {p for p in palabras_filtro if len(p) > 3}
                
                if palabras_filtro:
                    coincidencias = palabras_cv.intersection(palabras_filtro)
                    porcentaje = int((len(coincidencias) / len(palabras_filtro)) * 100)
                else:
                    coincidencias = set()
                    porcentaje = 0
                
                # Mostrar métricas
                st.metric(label="Porcentaje de Coincidencia ATS", value=f"{porcentaje}%")
                
                if porcentaje >= 75:
                    st.success("🎉 ¡Excelente! Tu CV tiene una alta densidad de palabras clave para este puesto.")
                elif porcentaje >= 40:
                    st.info("⚡ Buen camino, pero se recomienda incluir más términos específicos detectados en la oferta.")
                else:
                    st.error("🚨 Alerta: Tu nivel de optimización es bajo. El filtro ATS podría descartarte.")
                
                # Mostrar desglose
                st.markdown("#### Enlaces de coincidencia detectados:")
                if coincidencias:
                    st.write(", ".join(list(coincidencias)))
                else:
                    st.write("*No se encontraron palabras clave coincidentes directamente.*")
    else:
        st.info("💡 Por favor, configura tu CV y los requerimientos en el panel de la izquierda y haz clic en 'Iniciar Escaneo ATS' para ver los gráficos y resultados.")
