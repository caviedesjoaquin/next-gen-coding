# Paso 0: Importamos las librerias
import os
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

#Cargamos el TOKEN de OpenAI para poder ejecutar prompts
api_key = os.environ.get('OPENAI_API_KEY')

# Paso 1: Función para cargar documentos
# Dependiendo del tipo de archivo (pdf o txt) llama la función requerida
def load_documents(file_paths):
    documents = []
    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            continue
        documents.extend(loader.load())
    return documents

# Paso 2: Función para dividir texto en fragmentos
# Divide el texto en chunks de tamaño 1000 con un overlap de 200 para mantener
# la continuidad de la información
def chunk_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)

# Paso 3: Función para crear embeddings
# Creamos los embeddings de los chunks directamente cuando se llama a la funcion
# de almacenamiento de los vectores
# Se crea la funcion en el cuerpo de la funcion main

# Paso 4: Almacenamos los emebeddings en la bases de datos de Chroma
# Si la base de datos no existe, la crea; si existe, solamente la carga
# Esto para evitar que se tenga que generar desde 0 la base de datos,
# cada vez que se reciba un prompt del usuario
def store_in_chromadb(chunks, embeddings_model):
    report = 'RetoRAG'
    #db_path = os.environ.get("CHROMA_DATA_PATH", "./chroma")
    db_path='./chroma_db'
    if not os.path.exists(db_path):
        # Create the vector store and persist it
        vector_store = Chroma.from_documents(chunks, embeddings_model, collection_name=report,persist_directory=db_path)
    else:
        # Load the existing vector store
        vector_store = Chroma(persist_directory=db_path, embedding_function=embeddings_model,collection_name=report)
    return vector_store

# Paso 5: Recuperar información relevante
# Obtenemos los 5 primeros fragmentos relevantes de la base de datos
def retrieve_relevant_info(question, vector_store):
    docs = vector_store.similarity_search(question, k=5)
    return docs

# Paso 6: Generar prompt
# Generamos el prompt usando el prompt del usuario, mas los
# fragmentos relevantes
def generate_prompt(question, relevant_docs):
    limit=3750
    # Extraemos el contexto de los documentos
    contexts = [doc.page_content for doc in relevant_docs]
    # build our prompt with the retrieved contexts included
    prompt_start = (
        "Answer the question based on the context below.\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {question}\nAnswer:"
    )
    # Initialize prompt with all contexts
    prompt = (
        prompt_start +
        "\n\n---\n\n".join(contexts) +
        prompt_end
    )
    # If total length exceeds limit, reduce contexts one by one
    for i in range(len(contexts)-1, 0, -1):
        if len("\n\n---\n\n".join(contexts[:i])) < limit:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(contexts[:i]) +
                prompt_end
            )
            break
    return prompt

# Paso 7: Generar respuesta usando GPT-4
# Enviamos el prompt al modelo
def generate_answer(prompt):
    llm = ChatOpenAI(model_name="gpt-4", api_key=api_key, temperature=0)
    return llm.invoke(prompt)

# Paso 8: Función principal
def main(file_paths, question):
    # Cargamos los documentos
    documents = load_documents(file_paths)
    # Fragmentamos los documentos
    chunks = chunk_documents(documents)
    # Definimos la función que realizara los embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small",api_key=api_key)
    # Creamos o guardamos la base de datos de vactores
    vector_store = store_in_chromadb(chunks,embeddings)
    # Busacamos los vectores mas relevantes
    relevant_docs = retrieve_relevant_info(question, vector_store)
    # Generamos el prompt usando la pregunta y el contexto obetenido
    prompt = generate_prompt(question, relevant_docs)
    # Obtenemos la respuesta del LLM
    answer = generate_answer(prompt)
    return answer

# Porgram Principal
if __name__ == "__main__":
    file_paths = ['V-GEL Información ES PDF.pdf', 'RETO_RAG.pdf']
    # Primera pregunta
    question = "¿Cuáles son las instrucciones para el alumno en la Actividad: Creación de un sistema RAG sencillo?"
    answer = main(file_paths, question)
    print(f"Pregunta : {question}. \nRespuesta: {answer.content}\n\n")
    # Segunta pregunta
    question = "Cuales son las ventajas de v-gel?"
    answer = main(file_paths, question)
    print(f"Pregunta : {question}. \nRespuesta: {answer.content}\n\n")

