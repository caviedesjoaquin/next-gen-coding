# notebook_rag

`notebook_rag.py` es un módulo de Python diseñado para realizar preguntas a modelos LLM (Large Language Models) sobre el contenido de archivos, especialmente PDFs. Este módulo está pensado para facilitar la recuperación aumentada de información (RAG) desde documentos, ayudando a responder preguntas específicas de manera eficiente.

## Características principales

- Permite consultar modelos LLM con preguntas sobre documentos PDF.
- Fácil de integrar en flujos de trabajo de procesamiento de información y automatización.
- Pensado para proyectos educativos, de investigación o automatización documental.

## Ejemplo de uso

```python
import notebook_rag

file_paths = ['documento1.pdf', 'documento2.pdf']
pregunta = "¿Cuál es el objetivo del proyecto?"

respuesta = notebook_rag.Pregunta_LLM(file_paths, pregunta)
print(respuesta)
```

## Funciones principales

### `Pregunta_LLM(file_paths, pregunta)`

- **Descripción:** Realiza una consulta usando un modelo LLM sobre los archivos indicados y retorna la respuesta.
- **Parámetros:**
  - `file_paths`: Lista de rutas a archivos PDF.
  - `pregunta`: Pregunta en formato texto.
- **Retorno:** Respuesta generada por el modelo LLM.

## Requisitos

- Python 3.8 o superior.
- Dependencias indicadas en `requirements.txt` (ejemplo: PyPDF2, openai, etc).

Instalación recomendada de dependencias:

```bash
pip install -r requirements.txt
```

## Uso en testing

Puedes probar el funcionamiento del módulo usando el archivo de test incluido:

```python
# tests/test_main.py

import notebook_rag

def test_main():
    file_paths = ['archivo1.pdf', 'archivo2.pdf']
    pregunta = "¿Cuál es el objetivo del proyecto?"
    assert notebook_rag.Pregunta_LLM(file_paths, pregunta)
```

## Licencia

Este proyecto está bajo la licencia MIT.

## Autor

Joaquín Caviedes  
[GitHub](https://github.com/caviedesjoaquin)
