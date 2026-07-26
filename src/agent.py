import os
import glob
import json
import time
import re
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from langchain_community.document_loaders import (
    TextLoader,
    CSVLoader,
    JSONLoader,
    UnstructuredHTMLLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader
)

load_dotenv()

class CorporateAgent:
    def __init__(self, docs_dir="docs", persist_dir="chroma_db"):
        self.docs_dir = docs_dir
        self.persist_dir = persist_dir
        self.log_file = "logs.jsonl"
        
        # Inicializar el LLM de Google Gemini
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
        # Inicializar Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
        
        self.vector_store = self._load_or_create_vector_store()
        self.qa_chain = self._setup_chain()
        
    def _clean_text(self, text):
        """Limpia el texto removiendo espacios y saltos de línea repetidos, y caracteres no deseados."""
        if not text:
            return ""
        # Remover saltos de línea múltiples
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Remover espacios múltiples
        text = re.sub(r' {2,}', ' ', text)
        return text.strip()

    def _load_documents(self):
        """Carga documentos de varios formatos y asigna metadatos basados en la carpeta."""
        docs = []
        for root, _, files in os.walk(self.docs_dir):
            category = os.path.basename(root)
            if category == os.path.basename(self.docs_dir):
                category = "General"
                
            for file in files:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                try:
                    loader = None
                    if ext in ['.md', '.txt']:
                        loader = TextLoader(file_path, encoding='utf-8')
                    elif ext == '.csv':
                        loader = CSVLoader(file_path, encoding='utf-8')
                    elif ext == '.json':
                        # Para JSON, usamos un schema básico
                        loader = JSONLoader(file_path, jq_schema=".", text_content=False)
                    elif ext == '.html':
                        loader = UnstructuredHTMLLoader(file_path)
                    elif ext == '.pdf':
                        loader = PyPDFLoader(file_path)
                    elif ext == '.docx':
                        loader = Docx2txtLoader(file_path)
                    elif ext == '.xlsx':
                        loader = UnstructuredExcelLoader(file_path)
                    elif ext == '.pptx':
                        loader = UnstructuredPowerPointLoader(file_path)
                    
                    if loader:
                        loaded_docs = loader.load()
                        
                        # Extraer fechas de metadatos del sistema
                        c_time = os.path.getctime(file_path)
                        m_time = os.path.getmtime(file_path)
                        created_date = datetime.fromtimestamp(c_time).strftime('%Y-%m-%d %H:%M:%S')
                        modified_date = datetime.fromtimestamp(m_time).strftime('%Y-%m-%d %H:%M:%S')

                        for doc in loaded_docs:
                            # Atribución de metadatos enriquecidos (categoría, archivo, fechas, etc.)
                            # Algunos loaders como PyPDFLoader ya añaden 'page' de forma nativa.
                            doc.metadata['category'] = category
                            doc.metadata['source_file'] = file
                            doc.metadata['created_date'] = created_date
                            doc.metadata['modified_date'] = modified_date
                            
                            # Fase 2: Limpieza del texto
                            doc.page_content = self._clean_text(doc.page_content)
                            
                        docs.extend(loaded_docs)
                except Exception as e:
                    print(f"Error cargando {file_path}: {e}")
                    
        return docs

    def _load_or_create_vector_store(self):
        """Si existe la DB vectorial, la carga. Si no, procesa los documentos y la crea."""
        if os.path.exists(self.persist_dir):
            return Chroma(persist_directory=self.persist_dir, embedding_function=self.embeddings)
            
        print("Creando índice vectorial inicial...")
        documents = self._load_documents()
        
        # Chunking (Etapa 2)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.split_documents(documents)
        
        # Indexación Vectorial (Etapa 3)
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        return vector_store

    def _setup_chain(self):
        """Configura la cadena de recuperación (Etapa 4)."""
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
        
        prompt_template = """Eres un asistente corporativo experto. Tu función es ayudar a los empleados y usuarios a encontrar información en la base de conocimientos de la empresa.
REGLA IMPORTANTE: NO te presentes ni digas "Hola, soy el asistente" en tus respuestas. Ve directo al grano, asume que el usuario ya sabe quién eres.
Excepción: Si el usuario te pregunta explícitamente "quién eres", "qué puedes hacer" o "qué información contienes", entonces sí puedes describir que eres el asistente de Logística Global y tienes acceso a políticas, RRHH, envíos, siniestros, etc.

Para consultas de contenido, usa ÚNICAMENTE los siguientes fragmentos de contexto para construir tu respuesta.
Si la información necesaria no está en el contexto, di educadamente que no tienes esa información exacta en tu base de datos actual.
CRÍTICO: Debes detectar el idioma de la pregunta y responder OBLIGATORIAMENTE en ese mismo idioma.

Contexto:
{context}

Pregunta: {question}
Respuesta:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )
        return qa_chain

    def log_execution(self, query, response, sources, execution_time):
        """Registro de ejecución local (Etapa de Producción)."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "sources": sources,
            "execution_time_ms": round(execution_time * 1000, 2)
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def answer_question(self, query, category_filter=None):
        start_time = time.time()
        
        # Filtro por metadatos opcional (Etapa 4)
        if category_filter and category_filter != "Todas":
            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": 4, "filter": {"category": category_filter}}
            )
            self.qa_chain.retriever = retriever
        else:
            self.qa_chain.retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})

        result = self.qa_chain.invoke({"query": query})
        
        execution_time = time.time() - start_time
        
        answer = result['result']
        sources = [
            {"file": doc.metadata.get('source_file', 'Desconocido'), "category": doc.metadata.get('category', 'Desconocida')}
            for doc in result['source_documents']
        ]
        
        # Registrar ejecución
        self.log_execution(query, answer, sources, execution_time)
        
        return answer, sources
