from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model

from contenido.models import Categoria, Modalidad
from niveles.models import NivelCEFR
from habilidades.models import CriterioHabilidad

from llm.llm_service import LLMService, BundleSchema


class LLMServiceTests(TestCase):
    def setUp(self):
        # crear datos básicos en BD
        NivelCEFR.objects.create(codigo='B1', nombre='Intermediate', categoria='INTERMEDIO', vocab_min=1000, vocab_max=1500, cantidad_preguntas=5, puntos_requeridos=60, multiplicador_puntos=1.5)
        Categoria.objects.create(codigo='educacion', nombre='Educación')
        Modalidad.objects.create(codigo='IA_GENERADA', nombre='Generada por IA')
        CriterioHabilidad.objects.create(codigo='comprensión_general', nombre='Comprensión General', descripcion='desc', peso_evaluacion=3)

        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')

    @patch('llm.llm_service.ChatPromptTemplate')
    @patch('llm.llm_service.ChatOllama')
    def test_create_reading_with_questions_with_tags(self, MockChatOllama, MockPromptClass):
        # Mock LLM behaviour
        mock_llm = MockChatOllama.return_value
        structured = MagicMock()

        # Build a valid bundle dict matching BundleSchema
        bundle_dict = {
            "lectura": {"titulo": "Test title", "contenido": "This is a test passage.", "palabras": 5},
            "preguntas": [
                {"texto": "What is this?", "opciones": ["A","B","C","D"], "respuesta_correcta": "A"},
                {"texto": "Choose one.", "opciones": ["W","X","Y","Z"], "respuesta_correcta": "W"},
            ],
            "tags_applied": ["vocabulary"],
            "tags_ignored": ["speaking - not applicable to reading"]
        }

        # Ensure structured.invoke returns a validated BundleSchema
        structured.invoke.return_value = BundleSchema.model_validate(bundle_dict)
        mock_llm.with_structured_output.return_value = structured

        # Mock prompt chaining: make from_messages return an object whose __or__ returns a chain-like object
        class DummyPrompt:
            def __or__(self, other):
                class Chain:
                    def __init__(self, other):
                        self.other = other

                    def invoke(self, payload):
                        return self.other.invoke(payload)

                return Chain(other)

        MockPromptClass.from_messages.return_value = DummyPrompt()

        res = LLMService.create_reading_with_questions(
            self.user,
            tema='technology',
            nivel_codigo='B1',
            categoria_codigo='educacion',
            modalidad_codigo='IA_GENERADA',
            cantidad_preguntas=2,
            skills=['vocabulary'],
            tags=['vocabulary', 'speaking']
        )

        self.assertTrue(res.get('success'))
        self.assertIn('lectura', res)
        self.assertEqual(len(res.get('preguntas', [])), 2)
from django.test import TestCase

# Create your tests here.
