import streamlit as st
from pypdf import PdfReader
import re

# Configuración de página premium
st.set_page_config(page_title="Optimizador de CV & Escáner ATS", layout="wide")

st.title("📊 OPTIMIZADOR DE CV & ESCÁNER ATS")
st.subheader("APLICACIÓN INTERACTIVA DE DIAGNÓSTICO PROFESIONAL")

col1, col2 = st.columns([1, 1.3])

with col1:
    st.markdown("### 📥 PANEL DE ENTRADA")
    metodo_entrada = st.radio("Selecciona cómo deseas ingresar tu CV:", ("Cargar archivo (PDF, DOCX, TXT)", "Pegar texto manualmente"))
    
    texto_cv = ""
    if metodo_entrada == "Cargar archivo (PDF, DOCX, TXT)":
        archivo_cargado = st.file_uploader("Arrastra o selecciona tu currículum:", type=["pdf", "docx", "txt"])
        if archivo_cargado is not None:
            nombre_archivo = archivo_cargado.name.lower()
            if nombre_archivo.endswith('.pdf'):
                try:
                    lector_pdf = PdfReader(archivo_cargado)
                    paginas_texto = [pagina.extract_text() for pagina in lector_pdf.pages if pagina.extract_text()]
                    texto_cv = "\n".join(paginas_texto)
                    st.success(f"✅ ¡PDF leído con éxito! ({len(lector_pdf.pages)} páginas)")
                except Exception:
                    st.error("Error al procesar el PDF.")
            elif nombre_archivo.endswith('.txt'):
                try:
                    texto_cv = archivo_cargado.read().decode("utf-8")
                    st.success("✅ ¡Archivo leído con éxito!")
                except Exception:
                    st.error("Error al leer el archivo.")
            elif nombre_archivo.endswith('.docx'):
                try:
                    import zipfile
                    import xml.etree.ElementTree as ET
                    with zipfile.ZipFile(archivo_cargado) as docx:
                        arbol_xml = ET.fromstring(docx.read('word/document.xml'))
                        parrafos = [nodo.text for nodo in arbol_xml.iter() if nodo.tag.endswith('t')]
                        texto_cv = "".join(parrafos)
                    st.success("✅ ¡Documento Word leído con éxito!")
                except Exception:
                    st.error("Error al procesar el archivo Word.")
    else:
        texto_cv = st.text_area("PEGA TU CURRÍCULUM AQUÍ:", placeholder="Pega el texto de tu CV...", height=250)

    st.markdown("---")
    palabras_puesto = st.text_area("🎯 PALABRAS CLAVE O REQUERIMIENTOS DEL PUESTO:", placeholder="Ejemplo: diseñador interior, AutoCAD, SketchUp, Enscape, gestión de proyectos...", height=150)
    boton_escanear = st.button("Iniciar Escaneo ATS", type="primary")

# Función para normalizar texto (eliminar acentos y caracteres especiales para comparar bien)
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[áàäâ]', 'a', texto)
    texto = re.sub(r'[éèëê]', 'e', texto)
    texto = re.sub(r'[íìïî]', 'i', texto)
    texto = re.sub(r'[óòöô]', 'o', texto)
    texto = re.sub(r'[úùüû]', 'u', texto)
    texto = re.sub(r'[^a-z0-9ñç\s]', ' ', texto)
    return " ".join(texto.split())

with col2:
    st.markdown("### 📈 DIAGNÓSTICO DEL ESCÁNER")
    
    if boton_escanear:
        if not texto_cv:
            st.warning("⚠️ Por favor, carga o pega tu CV en el panel izquierdo.")
        elif not palabras_puesto:
            st.warning("⚠️ Por favor, ingresa los requerimientos o palabras clave del puesto.")
        else:
            with st.spinner("Analizando semántica estructural..."):
                # Normalización de textos
                cv_limpio = limpiar_texto(texto_cv)
                
                # Procesar requerimientos ignorando comas o saltos de línea
                req_lineas = [l.strip() for l in re.split(r'[,;\n]', palabras_puesto) if l.strip()]
                
                encontradas = []
                faltantes = []
                
                for req in req_lineas:
                    req_limpio = limpiar_texto(req)
                    if not req_limpio:
                        continue
                    # Buscar la frase exacta o palabra clave en el CV
                    if re.search(r'\b' + re.escape(req_limpio) + r'\b', cv_limpio):
                        encontradas.append(req)
                    else:
                        faltantes.append(req)
                
                total = len(encontradas) + len(faltantes)
                porcentaje = int((len(encontradas) / total) * 100) if total > 0 else 0
                
                # Despliegue de Resultados Premiums
                st.metric(label="Porcentaje de Compatibilidad ATS", value=f"{porcentaje}%")
                
                if porcentaje >= 75:
                    st.success("🎉 ¡Excelente compatibilidad! Tu perfil está listo para superar los filtros ATS de este puesto.")
                elif porcentaje >= 40:
                    st.info("⚡ Ajustes necesarios: Tienes una base sólida, pero necesitas incluir términos críticos para asegurar el pase.")
                else:
                    st.error("🚨 Alerta de Optimización: Tu nivel de coincidencia es bajo. El filtro ATS podría descartar este formato actual.")
                
                st.markdown("---")
                
                # SECCIÓN CLAVE: LO QUE SÍ TIENES Y LO QUE DEBES REPARAR
                c1, c2 = st.columns(2)
                
                with c1:
                    st.markdown("#### ✅ Palabras Clave Detectadas")
                    if encontradas:
                        for item in encontradas:
                            st.write(f"• {item}")
                    else:
                        st.write("*No se detectaron coincidencias exactas.*")
                        
                with c2:
                    st.markdown("#### ❌ Lo que te FALTA incorporar")
                    if faltantes:
                        for item in faltantes:
                            st.write(f"• :red[{item}]")
                    else:
                        st.write("*¡Excelente! No te falta ninguna de las palabras clave ingresadas.*")
                
                st.markdown("---")
                st.markdown("#### 💡 Plan de Acción Inmediato")
                if faltantes:
                    st.info(f"👉 **Estrategia:** Integra de forma natural los términos que te faltan (como **{', '.join(faltantes[:3])}**) dentro de tus secciones de 'Experiencia' o 'Habilidades' en tu CV antes de postularte.")
                else:
                    st.success("💪 Tu CV cubre todos los requerimientos técnicos ingresados. ¡Listo para enviar!")
    else:
        st.info("💡 Configura tu CV y los requerimientos en el panel izquierdo. El escáner te mostrará exactamente qué palabras añadir para optimizar tu perfil.")
