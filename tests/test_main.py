from main import main

def test_main():
  file_paths = ['V-GEL Información ES PDF.pdf', 'RETO_RAG.pdf']
  question = "¿Cuál es el objetivo del proyecto?"
  assert main(file_paths,question)
