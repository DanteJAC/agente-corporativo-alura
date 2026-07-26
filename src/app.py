import streamlit as st
import os
from agent import CorporateAgent

# Configuración de la página
st.set_page_config(page_title="Agente IA Corporativo", page_icon="🤖", layout="wide")

# Inicialización del Agente (Singleton en la sesión de Streamlit)
@st.cache_resource
def get_agent():
    # Verifica si hay API KEY de Google configurada
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Falta configurar GOOGLE_API_KEY en el entorno (o en un archivo .env)")
        st.stop()
    return CorporateAgent(docs_dir="../docs", persist_dir="../chroma_db")

try:
    agent = get_agent()
except Exception as e:
    st.error(f"Error al inicializar el agente: {e}")
    st.stop()

# Título y aviso de IA
st.title("🤖 Asistente Virtual Corporativo")
st.warning("⚠️ **Aviso:** Estás interactuando con un agente de Inteligencia Artificial. Las respuestas generadas están basadas estrictamente en la base de conocimiento de la empresa, pero siempre es recomendable verificar con los responsables de área en caso de duda.")

# Inicializar el historial de chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy el asistente virtual corporativo de Logística Global. Tengo acceso a las políticas de envíos, siniestros, atención al cliente y recursos humanos. ¿En qué te puedo ayudar hoy?"}
    ]

# Sidebar para filtros por categoría
st.sidebar.title("Configuración de Búsqueda")
categories = ["Todas", "Envios", "Atencion_Cliente", "Siniestros"]
selected_category = st.sidebar.selectbox("Filtrar por Área/Categoría:", categories)
st.sidebar.markdown("---")
st.sidebar.markdown("**Desafío Alura - Agente de IA**")

# Mostrar el historial de chat
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("Ver fuentes de esta respuesta"):
                for source in message["sources"]:
                    st.caption(f"📄 Archivo: {source['file']} | Categoría: {source['category']}")
            
            # Botones de feedback (Simulación visual)
            col1, col2 = st.columns([1, 15])
            with col1:
                if st.button("👍", key=f"up_{i}"):
                    st.toast("¡Gracias por tu retroalimentación positiva!")
            with col2:
                if st.button("👎", key=f"down_{i}"):
                    st.toast("¡Gracias! Tomaremos en cuenta esto para mejorar.")

# Campo de entrada del usuario
if prompt := st.chat_input("Escribe tu pregunta (ej. ¿Cuántos días de vacaciones tengo?)"):
    # Agregar pregunta al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Buscando en los documentos de la empresa..."):
            try:
                answer, sources = agent.answer_question(prompt, category_filter=selected_category)
                st.markdown(answer)
                
                with st.expander("Ver fuentes de esta respuesta"):
                    for source in sources:
                        st.caption(f"📄 Archivo: {source['file']} | Categoría: {source['category']}")
                
                # Guardar respuesta en el historial
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources
                })
                
                # Feedback botones para la respuesta actual
                st.write("¿Te fue útil esta respuesta?")
                col1, col2, _ = st.columns([1, 1, 10])
                with col1:
                    st.button("👍", key="new_up")
                with col2:
                    st.button("👎", key="new_down")
                    
            except Exception as e:
                st.error(f"Ocurrió un error al procesar tu pregunta: {e}")
