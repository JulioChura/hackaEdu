"""
Central metrics and defaults for LLM-generated readings and questions.

Keep configuration that affects generation here so it is easy to tune and
test (word targets per level, default question counts, scoring defaults).
"""

from typing import Dict

# Minimum target words per CEFR level used in prompts
# (actual output may be slightly longer; the LLM is instructed to meet these minimums)
WORDS_PER_LEVEL: Dict[str, int] = {
    "A1": 540,
    "A2": 750,
    "B1": 1050,
    "B2": 1440,
    "C1": 1860,
    "C2": 2340,
}

# Default number of questions to request when not provided
DEFAULT_QUESTIONS = 5

# Points configuration (base points per question)
DEFAULT_POINTS_PER_QUESTION = 1

# Limits for options / questions
MAX_OPTIONS = 4
MIN_OPTIONS = 4
MAX_QUESTIONS = 20   # hard cap — the real per-level default comes from NivelCEFR.cantidad_preguntas
MIN_QUESTIONS = 1
