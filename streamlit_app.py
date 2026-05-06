import streamlit as st
import google.generativeai as genai
import tempfile
import os


# Configuración de la página
st.set_page_config(page_title="Evaluador Ejecutivo - Diplomado CD", layout="wide")

st.title("👁️ Evaluador Estratégico y Visual de Presentaciones")
st.markdown("""
Esta herramienta analiza tu presentación bajo la óptica de un **Director de Datos (CDO)**. 
El modelo procesará visualmente el PDF para evaluar tanto el enfoque de negocio como el nivel de diseño de tus gráficas.
""")

# Configuración de la API
api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Utilizamos el modelo Pro para un escrutinio visual más analítico y detallado
    model = genai.GenerativeModel('gemini-3-flash-preview') 

    uploaded_file = st.file_uploader("Sube tu presentación en PDF", type="pdf")

    if uploaded_file is not None:
        if st.button("🚀 Iniciar Análisis"):
            with st.spinner("Analizando el contenido de la presentación"):
                
                # Guardar temporalmente el archivo
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                try:
                    # Al subir el archivo así, Gemini lo procesa de forma nativa e integral (imágenes, gráficas, layout y texto)
                    sample_file = genai.upload_file(path=tmp_path)
                    
                    # Prompt maestro con énfasis en la visión
                    prompt = """
                    Actúa como un Chief Data Officer (CDO) y Director de Estrategia de Negocio altamente exigente. Tu objetivo es evaluar las presentaciones ejecutivas (en formato PDF o imágenes) de un equipo de ciencia de datos, correspondientes a la "Práctica 3: Segmentación y Marketing".

                    No estás evaluando el código, estás evaluando su capacidad para traducir modelos matemáticos (Clusters, Matrices de Transición) en inteligencia de negocio accionable y con un alto nivel de diseño visual. 

                    Evalúa la presentación basándote estrictamente en los siguientes 3 pilares y proporciona retroalimentación estructurada:

                    ### 1. Enfoque de Negocio y Accionabilidad (Valor: 40%)
                    * **Lenguaje:** ¿El lenguaje es excesivamente técnico o está orientado a tomadores de decisiones? Penaliza el uso de jerga matemática innecesaria (ej. hablar de "inercias", "siluetas" o "p-values" sin traducir su significado al negocio).
                    * **Storytelling:** ¿La presentación cuenta una historia lógica? Debe ir desde el problema/contexto, pasando por el descubrimiento (segmentos) hasta la solución (campañas).
                    * **Accionabilidad:** Las recomendaciones finales deben ser concretas. Penaliza recomendaciones genéricas como "hay que venderles más a este cluster". Premia estrategias específicas justificadas por los datos (ej. "Enviar la oferta X al cluster Y mediante el canal Z porque tienen una tasa de conversión del N%").

                    ### 2. Calidad Visual y Estética (Valor: 40%)
                    * **Prohibición de Gráficos Genéricos:** Analiza rigurosamente todas las gráficas. Penaliza fuertemente si detectas el estilo visual por defecto de librerías como Matplotlib o Seaborn (ej. paletas de colores azul/naranja estándar, fondos grises con cuadrículas predeterminadas, tipografías pequeñas o ejes sin formato). 
                    * **Armonía Visual:** Evalúa si la presentación mantiene una paleta de colores coherente, alineación de elementos, espacios en blanco (aire) adecuados y tipografía legible. 
                    * **Carga Cognitiva:** Las diapositivas no deben estar saturadas de texto. Los gráficos deben tener títulos declarativos (que cuenten el hallazgo, no solo "Ventas vs Tiempo") y resaltar visualmente la métrica clave.
                    * **"Efecto WoW":** Premia el esfuerzo extra en el diseño, como el uso de mockups, tableros estilizados, o gráficos de alta calidad visual que denoten profesionalismo corporativo.

                    ### 3. Estructura y Cumplimiento (Valor: 20%)
                    * Verifica que la presentación incluya de manera clara: 
                        1. Resultados del EDA.
                        2. Perfilamiento claro de los clusters.
                        3. Comportamiento temporal / Matrices de transición.
                        4. Análisis de efectividad de las campañas.
                        5. Recomendaciones estratégicas.

                    ### FORMATO DE RESPUESTA ESPERADO
                    Para cada presentación analizada, tu respuesta debe tener la siguiente estructura exacta:

                    1.  **Veredicto Ejecutivo:** Un breve párrafo resumiendo la impresión general de la presentación.
                    2.  **Puntos Fuertes:** 2 o 3 viñetas destacando lo mejor del trabajo.
                    3.  **Áreas de Mejora Crítica:**
                        * *Enfoque de Negocio:* [Comentarios específicos]
                        * *Calidad Visual:* [Mencionar específicamente si se detectaron gráficos de Matplotlib/Seaborn sin personalizar o diapositivas saturadas].
                    4.  **Calificación Estimada:** Otorga una calificación preliminar del 0 al 8 (basado en la rúbrica de la presentación) justificando la puntuación.
                    5.  **Plan de Acción para el Alumno:** 2 pasos concretos que deben hacer para mejorar su presentación antes de exponerla a la junta directiva.
                    """

                    response = model.generate_content([prompt, sample_file])
                    
                    st.success("Análisis Completado")
                    st.markdown(response.text)

                except Exception as e:
                    st.error(f"Hubo un error en el análisis: {e}")
                finally:
                    # Limpieza en el sistema operativo local
                    os.unlink(tmp_path) 
                    # Limpieza en la nube de Google para no saturar tu cuota
                    genai.delete_file(sample_file.name) 
else:
    st.info("Por favor, introduce tu API Key en la barra lateral para comenzar.")
