"""
LLM Service - Generar lectura con preguntas en una sola llamada
Basado en LangChain docs - sin agents, solo model.invoke()
"""

import json
from langchain_ollama import OllamaLLM


class OllamaClient:
    """Cliente centralizado de Ollama"""
    
    MODEL = "phi3:mini"
    
    @staticmethod
    def get_llm():
        """Obtiene instancia de Ollama"""
        return OllamaLLM(model=OllamaClient.MODEL, format="json")


class PromptBuilder:
    """Construye el prompt completo para LLM"""
    
    @staticmethod
    def bundle_prompt(tema, nivel, cantidad, skills=None):
        """
        Arma el prompt completo interpolado (sin placeholders)
        
        Todo se interpola aquí con f-string
        """
        skills = skills or []
        skills_text = ""
        if skills:
            skills_text = f"\nEnfoca la lectura y preguntas en: {', '.join(skills)}"
        
        # Retornar string listo para pasar directamente a model.invoke()
        return f"""Genera una lectura en inglés y sus preguntas.

Tema: {tema}
Nivel CEFR: {nivel}
{skills_text}

REQUISITOS LECTURA:
- 300-400 palabras si nivel es A1
- 400-500 palabras si nivel es A2
- 500-600 palabras si nivel es B1
- 600-700 palabras si nivel es B2
- 700-800 palabras si nivel es C1
- 800-1000 palabras si nivel es C2
- Texto fluido y apropiado para el nivel
- Vocabulario acorde al nivel
- SIN explicaciones, SOLO el texto

REQUISITOS PREGUNTAS:
- {cantidad} preguntas en inglés
- Tipo: MULTIPLE CHOICE (4 opciones)
- Respuesta correcta en posición aleatoria
- Opciones plausibles

RESPONDE SOLO EN JSON VALIDO:
- Usa comillas dobles en todas las claves y valores
- No incluyas texto fuera del JSON
- No uses markdown
- Si necesitas saltos de línea en "contenido", usa \"\\n\" dentro del string
- Devuelve el JSON en una sola línea

JSON esperado:
{{
  "lectura": {{"titulo": "...", "contenido": "...", "palabras": 123}},
  "preguntas": [
    {{"texto": "...?", "opciones": ["A", "B", "C", "D"], "respuesta_correcta": "B"}}
  ]
}}

JSON:"""


class LLMGenerator:
    """Generador de contenido con LLM"""
    
    @staticmethod
    def _safe_json_parse(text):
        """
        Parsea JSON de forma segura desde la respuesta del LLM
        Limpia markdown si tiene ``` y extrae el JSON
        """
        try:
            if isinstance(text, dict):
                return text
            if not isinstance(text, str):
                text = str(text)

            text = text.strip()

            # Remover markdown ```json ... ``` o ``` ... ```
            if "```json" in text:
                start = text.find("```json") + 7
                end = text.find("```", start)
                text = text[start:end]
            elif "```" in text:
                start = text.find("```") + 3
                end = text.find("```", start)
                text = text[start:end]

            text = text.strip()

            # Si hay texto extra, intentar extraer el JSON principal
            if not text.startswith("{") or not text.endswith("}"):
                start = text.find("{")
                end = text.rfind("}")
                if start != -1 and end != -1 and end > start:
                    text = text[start:end + 1]

            return json.loads(text)
        except json.JSONDecodeError:
            return None

    @staticmethod
    def _normalize_bundle(payload):
        """
        Valida estructura JSON devuelto por LLM
        Asegura que tenga lectura y preguntas correctamente
        """
        if not isinstance(payload, dict):
            return None
        
        lectura = payload.get("lectura")
        preguntas = payload.get("preguntas")
        
        # Validar que ambos existan y sean del tipo correcto
        if not isinstance(lectura, dict) or not isinstance(preguntas, list):
            return None
        
        # Extraer y limpiar campos de lectura
        titulo = str(lectura.get("titulo", "")).strip()
        contenido = str(lectura.get("contenido", "")).strip()
        
        if not contenido:
            return None
        
        # Si no tiene palabras, calcular
        palabras = lectura.get("palabras")
        if not isinstance(palabras, int) or palabras <= 0:
            palabras = len(contenido.split())
        
        return {
            "lectura": {
                "titulo": titulo or "Lectura",
                "contenido": contenido,
                "palabras": palabras,
            },
            "preguntas": preguntas,
        }

    @staticmethod
    def generate_bundle(tema, nivel, cantidad=5, skills=None):
        """
        Hace UNA SOLA llamada al LLM para generar lectura + preguntas
        
        Proceso:
        1. Obtener instancia del LLM
        2. Armar prompt completo (interpolado)
        3. Invocar model.invoke(prompt_text)
        4. Parsear respuesta como JSON
        5. Normalizar estructura
        6. Retornar resultado
        """
        try:
            # 1. Obtener LLM
            llm = OllamaClient.get_llm()

            # 2. Armar prompt completo
            prompt_text = PromptBuilder.bundle_prompt(tema, nivel, cantidad, skills)

            # 3. Invocar el modelo - NO usar chain, solo invoke
            response = llm.invoke(prompt_text)
            
            # 4. Parsear JSON
            payload = LLMGenerator._safe_json_parse(response)
            
            if not payload:
                return {
                    "success": False,
                    "error": "No se pudo parsear JSON de la respuesta"
                }
            
            # 5. Normalizar
            normalized = LLMGenerator._normalize_bundle(payload)
            
            if not normalized:
                return {
                    "success": False,
                    "error": "JSON no tiene estructura esperada (lectura + preguntas)"
                }
            
            # 6. Retornar éxito
            return {
                "success": True,
                "lectura": normalized["lectura"],
                "preguntas": normalized["preguntas"],
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error: {str(e)}"
            }


class LLMService:
    """Fachada pública del servicio LLM"""
    
    @staticmethod
    def create_reading_with_questions(tema, nivel, cantidad_preguntas=5, skills=None):
        """
        Endpoint público - delega a LLMGenerator.generate_bundle()
        """
        return LLMGenerator.generate_bundle(tema, nivel, cantidad_preguntas, skills)


