"""
LLM Service — Genera lectura + preguntas y las persiste en base de datos.

Stack:
  - LangChain (LCEL) + ChatOllama para inferencia
  - Pydantic v2 para validar la salida estructurada
  - Django ORM con transaction.atomic() para persistencia
"""

from __future__ import annotations

import logging
from typing import Annotated, Optional, List
from llm.metrics import WORDS_PER_LEVEL, DEFAULT_QUESTIONS

from django.db import transaction
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field, field_validator

from contenido.models import (
    Lectura as LecturaModel,
    Pregunta as PreguntaModel,
    Categoria,
    Modalidad,
)
from habilidades.models import CriterioHabilidad
from niveles.models import NivelCEFR

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Distribución de criterios por defecto cuando el nivel no tiene configuración.
# Clave = código CEFR, Valor = lista de códigos de criterio por posición de pregunta.
# Las posiciones se repiten/rotan según sea necesario (index % len).
# A1/A2 → más literales; B1/B2 → balance; C1/C2 → más inferencia/crítico
# ---------------------------------------------------------------------------
DEFAULT_DISTRIBUTION: dict[str, list[str]] = {
    "A1": ["comprensión_general", "comprensión_general", "vocabulario", "detalles_específicos", "comprensión_general"],
    "A2": ["comprensión_general", "vocabulario", "comprensión_general", "detalles_específicos", "gramática"],
    "B1": ["comprensión_general", "detalles_específicos", "vocabulario", "inferencia", "comprensión_general"],
    "B2": ["inferencia", "detalles_específicos", "vocabulario", "gramática", "inferencia"],
    "C1": ["inferencia", "gramática", "inferencia", "detalles_específicos", "vocabulario"],
    "C2": ["inferencia", "inferencia", "gramática", "detalles_específicos", "inferencia"],
}
FALLBACK_CRITERIO = "comprensión_general"


# Pydantic schemas — definen la salida esperada del LLM

class LecturaSchema(BaseModel):
    """Lectura en inglés generada por el LLM."""

    titulo: str = Field(description="Título de la lectura en inglés")
    contenido: str = Field(
        description=(
            "Texto COMPLETO de la lectura en inglés. "
            "NO uses tokens, etiquetas ni placeholders como <|B1|>. "
            "Escribe el texto íntegro aquí."
        )
    )
    palabras: int = Field(description="Número aproximado de palabras del contenido")


class PreguntaSchema(BaseModel):
    """Pregunta de opción múltiple sobre la lectura."""

    texto: str = Field(
        description="Question text only — no options, no letters A/B/C/D"
    )
    opciones: Annotated[list[str], Field(min_length=4, max_length=4)] = Field(
        description="Exactly 4 answer options as clean strings, no A./B./C./D. prefixes"
    )
    respuesta_correcta: str = Field(
        description="Exact text of the correct answer, must match one of the 4 opciones strings"
    )

    @field_validator("opciones")
    @classmethod
    def must_have_four_options(cls, v: list[str]) -> list[str]:
        if len(v) != 4:
            raise ValueError(f"opciones must have exactly 4 items, got {len(v)}")
        return v

    @field_validator("respuesta_correcta")
    @classmethod
    def correct_answer_in_options(cls, v: str, info) -> str:
        opciones = (info.data or {}).get("opciones", [])
        if opciones and v not in opciones:
            # Partial match fallback: return first option that starts with the answer
            match = next((o for o in opciones if o.startswith(v[:20])), opciones[0])
            return match
        return v


class BundleSchema(BaseModel):
    """Salida completa del LLM: una lectura y sus preguntas."""

    lectura: LecturaSchema
    preguntas: list[PreguntaSchema]
    tags_applied: list[str] = Field(default_factory=list, description="Tags the model applied")
    tags_ignored: list[str] = Field(default_factory=list, description="Tags the model decided to ignore (with reasons in LLM explanation)")


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

_BUNDLE_PROMPT = """\
You are an experienced English teacher creating reading comprehension material for ESL students.

Everything — the reading passage AND all questions and answer options — must be written in ENGLISH.

Task: Generate a reading passage and exactly {cantidad} multiple-choice comprehension questions.

Topic: {tema}
CEFR Level: {nivel}
{skills_line}
Tags: {tags_line}

=== READING PASSAGE ===
- Write in English, fluent and natural for CEFR level {nivel}
- Approximate word count: A1→300w, A2→400w, B1→500w, B2→600w, C1→700w, C2→800w
- The passage must relate to the topic: {tema}
{skills_reading_note}
- DO NOT include CEFR tags, tokens or placeholders like <|B1|>
- Put the complete passage text in the 'contenido' field

=== COMPREHENSION QUESTIONS ===
- Generate EXACTLY {cantidad} questions IN ENGLISH
- Each question tests reading comprehension of the passage above
{skills_questions_note}
- Each question must have EXACTLY 4 answer options — no more, no less
- Answer options are plain strings, NO A. / B. / C. / D. prefixes
- 'respuesta_correcta' must be the EXACT string of the correct option

Tag handling rules (model responsibility):
- `tags` are user preferences like 'past simple', 'vocabulary:technology', 'speaking'.
- Try to include applicable tags in the passage text, vocabulary or questions.
- If a tag is incompatible with the topic or would create contradictions, IGNORE that tag and list it under `tags_ignored` in the JSON with a short reason.
- List tags that were included under `tags_applied`.

The JSON response MUST include two extra arrays at top level: `tags_applied` and `tags_ignored` (each an array of strings). For ignored tags include a short reason after the tag, separated by ' - '.

Respond ONLY with the JSON object. No extra text, no markdown fences.
"""


# ---------------------------------------------------------------------------
# Criteria distribution helper
# ---------------------------------------------------------------------------

def _get_criterio(nivel_codigo: str, distribucion_db: dict, index: int) -> CriterioHabilidad | None:
    """
    Devuelve el CriterioHabilidad para la pregunta en posición `index` (0-based).

    Prioridad:
      1. distribucion_criterios del nivel almacenado en BD (si no está vacío)
      2. DEFAULT_DISTRIBUTION definido en este módulo
      3. Primer criterio existente en la BD (fallback total)
    """
    codigos: list[str] = []

    if distribucion_db:
        codigos = list(distribucion_db.keys())
    elif nivel_codigo in DEFAULT_DISTRIBUTION:
        codigos = DEFAULT_DISTRIBUTION[nivel_codigo]

    if codigos:
        criterio = CriterioHabilidad.objects.filter(codigo=codigos[index % len(codigos)]).first()
        if criterio:
            return criterio

    return (
        CriterioHabilidad.objects.filter(codigo=FALLBACK_CRITERIO).first()
        or CriterioHabilidad.objects.first()
    )

# Public service

class LLMService:
    """Fachada pública del módulo LLM."""

    @staticmethod
    def create_reading_with_questions(
        user,
        tema: str,
        nivel_codigo: str,
        categoria_codigo: str,
        modalidad_codigo: str,
        cantidad_preguntas: int = 5,
        skills: Optional[list[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> dict:
        """
        Genera una lectura en inglés con preguntas de comprensión y las persiste
        en la base de datos dentro de una transacción atómica.

        Returns:
            dict con 'success': True y los datos guardados,
            o 'success': False + 'error'.
        """
        skills = skills or []
        tags = tags or []

        # --- Validar referencias FK ---
        categoria = Categoria.objects.filter(codigo=categoria_codigo).first()
        if not categoria:
            return {"success": False, "error": f"Categoria '{categoria_codigo}' no encontrada"}

        modalidad = Modalidad.objects.filter(codigo=modalidad_codigo).first()
        if not modalidad:
            return {"success": False, "error": f"Modalidad '{modalidad_codigo}' no encontrada"}

        nivel = NivelCEFR.objects.filter(codigo=nivel_codigo).first()
        if not nivel:
            return {"success": False, "error": f"Nivel CEFR '{nivel_codigo}' no encontrado"}

        # --- Construir y ejecutar cadena LCEL ---
        try:
            llm = ChatOllama(model="qwen2.5:3b", temperature=0.7)
            structured_llm = llm.with_structured_output(BundleSchema)

            prompt = ChatPromptTemplate.from_messages([("human", _BUNDLE_PROMPT)])

            chain = prompt | structured_llm

            skills_line = f"Skills to improve: {', '.join(skills)}" if skills else ""
            skills_reading_note = (
                f"- The passage vocabulary and content should help practice: {', '.join(skills)}"
                if skills else ""
            )
            skills_questions_note = (
                f"- At least some questions should target these skills: {', '.join(skills)}"
                if skills else "- Vary types: literal comprehension, inference, vocabulary"
            )

            tags_line = f"User tags: {', '.join(tags)}" if tags else ""

            bundle: BundleSchema = chain.invoke({
                "tema": tema,
                "nivel": nivel_codigo,
                "cantidad": cantidad_preguntas,
                "skills_line": skills_line,
                "skills_reading_note": skills_reading_note,
                "skills_questions_note": skills_questions_note,
                "tags_line": tags_line,
            })

        except Exception as exc:
            logger.exception("Error llamando al LLM")
            return {"success": False, "error": f"LLM error: {exc.__class__.__name__}: {exc}"}

        # --- Persistir en BD ---
        distribucion_db = nivel.distribucion_criterios or {}

        try:
            with transaction.atomic():
                lectura = LecturaModel.objects.create(
                    usuario_creador=user,
                    nivel_cefr=nivel,
                    categoria=categoria,
                    modalidad=modalidad,
                    titulo=bundle.lectura.titulo or tema,
                    contenido=bundle.lectura.contenido,
                    publicada=False,
                )

                preguntas_guardadas = []
                for idx, p in enumerate(bundle.preguntas):
                    criterio = _get_criterio(nivel_codigo, distribucion_db, idx)
                    pregunta = PreguntaModel.objects.create(
                        lectura=lectura,
                        criterio=criterio,
                        texto=p.texto,
                        tipo="MULTIPLE",
                        opciones=p.opciones,
                        respuesta_correcta=p.respuesta_correcta,
                        orden=idx + 1,
                    )
                    preguntas_guardadas.append(pregunta)

        except Exception as exc:
            logger.exception("Error guardando en base de datos")
            return {"success": False, "error": f"DB error: {exc.__class__.__name__}: {exc}"}

        return {
            "success": True,
            "lectura": {
                "id": lectura.id,
                "titulo": lectura.titulo,
                "nivel": nivel_codigo,
                "palabras": lectura.palabras_count,
                "contenido": lectura.contenido,
            },
            "preguntas": [
                {
                    "id": p.id,
                    "texto": p.texto,
                    "opciones": p.opciones,
                    "respuesta_correcta": p.respuesta_correcta,
                    "criterio": p.criterio.codigo if p.criterio else None,
                    "orden": p.orden,
                }
                for p in preguntas_guardadas
            ],
        }
