import notebook_rag


def test_main():
    file_paths = ['V-GEL Información ES PDF.pdf', 'RETO_RAG.pdf']
    question = "¿Cuál es el objetivo del proyecto?"
    assert notebook_rag.Pregunta_LLM(file_paths, question)
