"""
Central metrics and defaults for LLM-generated readings and questions.

Keep configuration that affects generation here so it is easy to tune and
test (word targets per level, default question counts, scoring defaults).
"""

from typing import Dict

# Approximate target words per CEFR level used in prompts
WORDS_PER_LEVEL: Dict[str, int] = {
    "A1": 300,
    "A2": 400,
    "B1": 500,
    "B2": 600,
    "C1": 700,
    "C2": 800,
}

# Default number of questions to request when not provided
DEFAULT_QUESTIONS = 5

# Points configuration (base points per question)
DEFAULT_POINTS_PER_QUESTION = 1

# Limits for options / questions
MAX_OPTIONS = 4
MIN_OPTIONS = 4
MAX_QUESTIONS = 10
MIN_QUESTIONS = 1
