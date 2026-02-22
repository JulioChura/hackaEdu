"""
LLM Service - Generar lectura con preguntas en una sola llamada
Estructura limpia y mantenible
"""

import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


class OllamaClient:
    """Cliente centralizado de Ollama"""
    
    MODEL = "llama3.2:1b"
    
    @staticmethod
    def get_llm():
        """Obtiene instancia de Ollama"""
        return OllamaLLM(model=OllamaClient.MODEL)


class PromptBuilder:
    """Construye prompts optimizados para cada tarea"""
    
    @staticmethod
    def reading_prompt(tema, nivel):
        """Prompt para generar lectura"""
        return ChatPromptTemplate.from_template(
            """Genera una lectura en inglés sobre: {tema}
Nivel CEFR: {nivel}

REQUISITOS:
- 200-300 palabras
- Texto fluido pero apropiado para el nivel
- Vocabulario acorde
- SIN explicaciones, SOLO el texto

Lectura:"""
        ).format(tema=tema, nivel=nivel)
    
    @staticmethod
    def questions_prompt(lectura, nivel, cantidad):
        """Prompt para generar preguntas"""
        return ChatPromptTemplate.from_template(
            """Basado en esta lectura:
{lectura}

Genera {cantidad} preguntas en inglés - Nivel {nivel}

REQUISITOS:
- Tipo: MULTIPLE CHOICE (4 opciones)
- Respuesta correcta en posición aleatoria
- Opciones plausibles

RESPONDE EXACTAMENTE EN JSON (sin markdown):
[
  {{"texto": "pregunta?", "opciones": ["opt1", "opt2", "opt3", "opt4"], "respuesta_correcta": "opt_correcta"}}
]

JSON:"""
        ).format(lectura=lectura[:500], nivel=nivel, cantidad=cantidad)


class LLMGenerator:
    """Generador principal de contenido"""
    
    @staticmethod
    def _safe_json_parse(text):
        """Parsea JSON de forma segura"""
        try:
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    
    @staticmethod
    def generate_reading(tema, nivel):
        """
        Genera una lectura
        
        Args:
            tema: Tema a desarrollar
            nivel: Nivel CEFR (A1-C2)
        
        Returns:
            dict: {"success": bool, "titulo": str, "contenido": str, "palabras": int, "error": str}
        """
        try:
            llm = OllamaClient.get_llm()
            prompt = PromptBuilder.reading_prompt(tema, nivel)
            
            chain = prompt | llm
            contenido = chain.invoke({})
            
            return {
                "success": True,
                "titulo": f"{tema.title()} ({nivel})",
                "contenido": contenido.strip(),
                "palabras": len(contenido.split())
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generando lectura: {str(e)}"
            }
    
    @staticmethod
    def generate_questions(lectura, nivel, cantidad=5):
        """
        Genera preguntas para una lectura
        
        Args:
            lectura: Texto de la lectura
            nivel: Nivel CEFR
            cantidad: Número de preguntas
        
        Returns:
            dict: {"success": bool, "preguntas": list, "error": str}
        """
        try:
            llm = OllamaClient.get_llm()
            prompt = PromptBuilder.questions_prompt(lectura, nivel, cantidad)
            
            chain = prompt | llm
            response = chain.invoke({})
            
            preguntas = LLMGenerator._safe_json_parse(response)
            
            if not preguntas:
                return {
                    "success": False,
                    "error": "No se pudo parsear respuesta JSON"
                }
            
            return {
                "success": True,
                "preguntas": preguntas
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generando preguntas: {str(e)}"
            }
    
    @staticmethod
    def evaluate_answer(pregunta, respuesta_usuario, respuesta_correcta, nivel):
        """
        Evalúa una respuesta
        
        Args:
            pregunta: Texto de la pregunta
            respuesta_usuario: Respuesta dada
            respuesta_correcta: Respuesta correcta
            nivel: Nivel CEFR
        
        Returns:
            dict: {"success": bool, "es_correcta": bool, "puntos": int, "feedback": str, "error": str}
        """
        try:
            llm = OllamaClient.get_llm()
            
            prompt = ChatPromptTemplate.from_template(
                """Evalúa esta respuesta:
Pregunta: {pregunta}
Respuesta usuario: {respuesta_usuario}
Respuesta correcta: {respuesta_correcta}
Nivel: {nivel}

Responde EXACTAMENTE en JSON:
{{"es_correcta": true/false, "puntos": 0-10, "feedback": "explicación breve"}}

JSON:"""
            )
            
            chain = prompt | llm
            response = chain.invoke({
                "pregunta": pregunta,
                "respuesta_usuario": respuesta_usuario,
                "respuesta_correcta": respuesta_correcta,
                "nivel": nivel
            })
            
            resultado = LLMGenerator._safe_json_parse(response)
            
            if not resultado:
                return {
                    "success": False,
                    "error": "No se pudo parsear evaluación"
                }
            
            return {
                "success": True,
                "es_correcta": resultado.get("es_correcta", False),
                "puntos": resultado.get("puntos", 0),
                "feedback": resultado.get("feedback", "")
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error evaluando: {str(e)}"
            }


class LLMService:
    """Fachada principal - API simplificada"""
    
    @staticmethod
    def create_reading_with_questions(tema, nivel, cantidad_preguntas=5):
        """
        Crea lectura + preguntas en una sola operación
        
        Args:
            tema: Tema de interés
            nivel: Nivel CEFR
            cantidad_preguntas: Número de preguntas a generar
        
        Returns:
            dict: {"success": bool, "lectura": {...}, "preguntas": [...], "error": str}
        """
        # 1. Generar lectura
        lectura_result = LLMGenerator.generate_reading(tema, nivel)
        
        if not lectura_result['success']:
            return lectura_result
        
        lectura = lectura_result
        
        # 2. Generar preguntas basadas en la lectura
        preguntas_result = LLMGenerator.generate_questions(
            lectura['contenido'],
            nivel,
            cantidad_preguntas
        )
        
        if not preguntas_result['success']:
            return preguntas_result
        
        return {
            "success": True,
            "lectura": {
                "titulo": lectura['titulo'],
                "contenido": lectura['contenido'],
                "palabras": lectura['palabras']
            },
            "preguntas": preguntas_result['preguntas']
        }
    
    @staticmethod
    def evaluate_answer(pregunta, respuesta_usuario, respuesta_correcta, nivel):
        """Evalúa respuesta (delegado)"""
        return LLMGenerator.evaluate_answer(pregunta, respuesta_usuario, respuesta_correcta, nivel)
