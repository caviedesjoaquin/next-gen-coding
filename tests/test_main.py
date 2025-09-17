from notebook_rag import Pregunta_LLM

def test_main():
  file_paths = ['V-GEL Información ES PDF.pdf', 'RETO_RAG.pdf']
  question = "¿Cuál es el objetivo del proyecto?"
  assert Pregunta_LLM(file_paths,question)
