"""
Módulo evaluador con IA usando Ollama
Proyecto: ReConéctate IA - Hackathon 2025
Autor: PERSONA 1 (IA + PROMPTS)

Este módulo conecta con Ollama (local) para evaluar respuestas de estudiantes
usando Llama 3.2 3B u otro modelo compatible.
"""

import json
import requests
import re
import logging
from datetime import datetime
from django.db import transaction
from django.conf import settings

# Configurar logging
logger = logging.getLogger(__name__)


class EvaluadorIA:
    """
    Clase principal para evaluación de respuestas abiertas con IA
    
    Funcionalidades:
    1. Obtener datos de evaluación desde BD
    2. Construir prompt estructurado
    3. Llamar a modelo de IA (Ollama)
    4. Parsear respuesta JSON
    5. Guardar resultados en BD
    """
    
    def __init__(self, modelo="llama3.2:3b", url_ollama="http://localhost:11434"):
        """
        Inicializa el evaluador
        
        Args:
            modelo (str): Nombre del modelo en Ollama (default: llama3.2:3b)
            url_ollama (str): URL base de Ollama (default: http://localhost:11434)
        """
        self.modelo = modelo
        self.url_ollama = url_ollama
        logger.info(f"EvaluadorIA inicializado con modelo: {modelo}")
    
    def evaluar_respuestas(self, evaluacion_id, alumno_id):
        """
        Función principal que orquesta todo el proceso de evaluación
        
        Args:
            evaluacion_id (int): ID de la evaluación
            alumno_id (int): ID del alumno
            
        Returns:
            dict: {
                "success": bool,
                "data": dict con evaluaciones,
                "error": str (solo si success=False)
            }
        """
        try:
            logger.info(f"Iniciando evaluación - Evaluacion: {evaluacion_id}, Alumno: {alumno_id}")
            
            # 1. Obtener datos de BD
            datos = self._obtener_datos_evaluacion(evaluacion_id, alumno_id)
            logger.info(f"Datos obtenidos: {len(datos['respuestas'])} respuestas, {len(datos['criterios'])} criterios")
            
            # 2. Construir prompt
            prompt = self._construir_prompt(datos)
            logger.debug(f"Prompt construido (longitud: {len(prompt)} caracteres)")
            
            # 3. Llamar a IA
            respuesta_ia = self._llamar_ia(prompt)
            logger.info("Respuesta de IA recibida")
            
            # 4. Parsear respuesta
            evaluaciones = self._parsear_respuesta(respuesta_ia)
            logger.info(f"Respuesta parseada: {len(evaluaciones.get('evaluaciones', []))} evaluaciones")
            
            # 5. Validar estructura
            self._validar_evaluaciones(evaluaciones, datos)
            
            # 6. Guardar en BD
            reporte = self._guardar_evaluaciones(evaluaciones)
            logger.info(f"Evaluaciones guardadas - Reporte ID: {reporte.reporte_id}")
            
            return {
                "success": True,
                "data": evaluaciones,
                "reporte_id": reporte.reporte_id
            }
            
        except Exception as e:
            logger.error(f"Error en evaluación: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    def _obtener_datos_evaluacion(self, evaluacion_id, alumno_id):
        """
        Consulta la BD y estructura los datos necesarios para el prompt
        
        Args:
            evaluacion_id (int): ID de la evaluación
            alumno_id (int): ID del alumno
            
        Returns:
            dict: Datos estructurados para construir el prompt
        """
        # Importar modelos (aquí para evitar problemas de importación circular)
        from evaluacion.models import Evaluacion, Sesion
        from alumnos.models import Alumno
        
        # TODO: Ajustar según tus modelos reales
        # Este es un ejemplo basado en el modelo de datos del documento
        
        try:
            # Obtener evaluación y sesión
            evaluacion = Evaluacion.objects.select_related('sesion', 'docente').get(
                evaluacion_id=evaluacion_id
            )
            sesion = evaluacion.sesion
            alumno = Alumno.objects.select_related('usuario').get(alumno_id=alumno_id)
            
            # Obtener criterios de la sesión
            # TODO: Ajustar según tu modelo real de Criterio
            criterios = []
            # Ejemplo:
            # criterios = sesion.criterios.all().values('criterio_id', 'nombre_criterio', 'descripcion', 'peso')
            
            # Obtener respuestas del alumno con preguntas relacionadas
            # TODO: Ajustar según tu modelo real de RespuestaAlumno
            respuestas = []
            # Ejemplo:
            # respuestas_queryset = RespuestaAlumno.objects.filter(
            #     evaluacion_id=evaluacion_id,
            #     alumno_id=alumno_id
            # ).select_related('pregunta')
            
            # Estructurar datos para el prompt
            datos = {
                'sesion': {
                    'nombre': getattr(sesion, 'nombre_sesion', 'Sin nombre'),
                    'tema': getattr(getattr(sesion, 'tema', None), 'nombre_tema', 'Sin tema'),
                    'objetivo': getattr(sesion, 'objetivo_sesion', 'Sin objetivo'),
                    'nivel_educativo': '5to grado'  # TODO: Obtener de docente o sesión
                },
                'criterios': criterios,
                'respuestas': respuestas,
                'alumno': {
                    'alumno_id': alumno.alumno_id,
                    'nombre': f"{alumno.usuario.nombres} {alumno.usuario.apellidos}",
                    'grado': getattr(alumno, 'grado_actual', 'Sin grado')
                },
                'evaluacion_id': evaluacion_id
            }
            
            # TODO: Agregar lógica para obtener criterios vinculados a cada pregunta
            # desde la tabla pregunta_criterio
            
            return datos
            
        except Exception as e:
            logger.error(f"Error obteniendo datos de BD: {str(e)}")
            raise
    
    def _construir_prompt(self, datos):
        """
        Construye el prompt usando la plantilla del módulo prompts.py
        
        Args:
            datos (dict): Datos estructurados de la evaluación
            
        Returns:
            str: Prompt formateado
        """
        from .prompts import construir_prompt
        return construir_prompt(datos)
    
    def _llamar_ia(self, prompt, timeout=30):
        """
        Llama a Ollama para generar la evaluación
        
        Args:
            prompt (str): Prompt construido
            timeout (int): Timeout en segundos (default: 30)
            
        Returns:
            str: Respuesta de la IA (texto con JSON)
            
        Raises:
            requests.RequestException: Si hay error en la llamada HTTP
            TimeoutError: Si la llamada supera el timeout
        """
        url = f"{self.url_ollama}/api/generate"
        
        payload = {
            "model": self.modelo,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Respuestas más consistentes y predecibles
                "top_p": 0.9,        # Núcleo de probabilidad
                "num_predict": 2000, # Máximo tokens de respuesta
                "stop": ["\n\n---"]  # Detener si genera texto extra
            }
        }
        
        try:
            logger.debug(f"Llamando a Ollama: {url}")
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            
            resultado = response.json()
            texto_respuesta = resultado.get('response', '')
            
            if not texto_respuesta:
                raise ValueError("Ollama devolvió respuesta vacía")
            
            logger.debug(f"Respuesta de IA recibida (longitud: {len(texto_respuesta)})")
            return texto_respuesta
            
        except requests.Timeout:
            raise TimeoutError(f"La llamada a Ollama superó el timeout de {timeout}s")
        except requests.RequestException as e:
            raise Exception(f"Error conectando con Ollama: {str(e)}")
    
    def _parsear_respuesta(self, texto_respuesta):
        """
        Extrae y valida el JSON de la respuesta de la IA
        
        Args:
            texto_respuesta (str): Texto completo devuelto por la IA
            
        Returns:
            dict: Objeto JSON parseado
            
        Raises:
            ValueError: Si no se puede extraer JSON válido
        """
        # Intentar parsear directamente
        try:
            return json.loads(texto_respuesta)
        except json.JSONDecodeError:
            logger.warning("JSON directo falló, intentando extraer de texto...")
            
            # Intentar encontrar JSON dentro del texto
            # Buscar desde el primer { hasta el último }
            match = re.search(r'\{.*\}', texto_respuesta, re.DOTALL)
            
            if match:
                json_str = match.group()
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON extraído inválido: {str(e)}")
                    logger.debug(f"JSON extraído: {json_str[:500]}...")
                    raise ValueError(f"JSON extraído es inválido: {str(e)}")
            else:
                logger.error("No se encontró estructura JSON en la respuesta")
                logger.debug(f"Respuesta completa: {texto_respuesta[:500]}...")
                raise ValueError("No se pudo encontrar JSON en la respuesta de la IA")
    
    def _validar_evaluaciones(self, evaluaciones, datos_originales):
        """
        Valida que la estructura de evaluaciones sea correcta
        
        Args:
            evaluaciones (dict): Evaluaciones parseadas de la IA
            datos_originales (dict): Datos originales de la evaluación
            
        Raises:
            ValueError: Si la estructura es inválida
        """
        # Validar campos requeridos
        campos_requeridos = ['alumno_id', 'evaluacion_id', 'evaluaciones', 'diagnostico_general']
        for campo in campos_requeridos:
            if campo not in evaluaciones:
                raise ValueError(f"Campo requerido faltante en respuesta: {campo}")
        
        # Validar que haya evaluaciones
        if not evaluaciones['evaluaciones']:
            raise ValueError("No se generaron evaluaciones")
        
        # Validar cada evaluación
        for i, eval_item in enumerate(evaluaciones['evaluaciones']):
            campos_eval = ['respuesta_id', 'criterio_id', 'puntaje_obtenido', 'puntaje_maximo', 
                          'justificacion', 'evidencia']
            for campo in campos_eval:
                if campo not in eval_item:
                    raise ValueError(f"Evaluación {i}: falta campo '{campo}'")
            
            # Validar rango de puntajes
            puntaje = eval_item['puntaje_obtenido']
            if not (0.0 <= puntaje <= 5.0):
                logger.warning(f"Puntaje fuera de rango: {puntaje}, ajustando...")
                eval_item['puntaje_obtenido'] = max(0.0, min(5.0, puntaje))
        
        logger.info(f"Validación exitosa: {len(evaluaciones['evaluaciones'])} evaluaciones válidas")
    
    def _guardar_evaluaciones(self, evaluaciones):
        """
        Guarda los resultados en evaluacion_criterio_respuesta y reporte_ia
        
        Args:
            evaluaciones (dict): Evaluaciones validadas
            
        Returns:
            ReporteIA: Objeto del reporte creado
        """
        # TODO: Importar modelos reales
        # from evaluacion.models import EvaluacionCriterioRespuesta, ReporteIA
        
        # TODO: Implementar guardado real en BD
        # Este es un esqueleto que debes adaptar a tus modelos
        
        logger.warning("ADVERTENCIA: Guardado en BD no implementado (TODO)")
        
        # Ejemplo de implementación:
        """
        with transaction.atomic():
            # Crear reporte general
            reporte = ReporteIA.objects.create(
                evaluacion_id=evaluaciones['evaluacion_id'],
                alumno_id=evaluaciones['alumno_id'],
                diagnostico_general=evaluaciones.get('diagnostico_general', ''),
                fortalezas_identificadas=', '.join(evaluaciones.get('fortalezas', [])),
                areas_mejora=', '.join(evaluaciones.get('areas_mejora', [])),
                fecha_generacion=datetime.now()
            )
            
            # Guardar evaluación por cada par (respuesta, criterio)
            for eval_item in evaluaciones['evaluaciones']:
                EvaluacionCriterioRespuesta.objects.create(
                    respuesta_id=eval_item['respuesta_id'],
                    criterio_id=eval_item['criterio_id'],
                    puntaje_obtenido=eval_item['puntaje_obtenido'],
                    puntaje_maximo=eval_item.get('puntaje_maximo', 5.0),
                    justificacion=eval_item['justificacion'],
                    evidencia=eval_item.get('evidencia', ''),
                    fecha_evaluacion=datetime.now()
                )
            
            return reporte
        """
        
        # Retornar objeto mock por ahora
        class MockReporte:
            reporte_id = 999
        
        return MockReporte()
    
    def verificar_conexion_ollama(self):
        """
        Verifica que Ollama esté corriendo y el modelo esté disponible
        
        Returns:
            dict: {"disponible": bool, "modelos": list, "error": str}
        """
        try:
            # Verificar que Ollama responda
            response = requests.get(f"{self.url_ollama}/api/tags", timeout=5)
            response.raise_for_status()
            
            modelos_data = response.json()
            modelos = [m['name'] for m in modelos_data.get('models', [])]
            
            modelo_disponible = self.modelo in modelos
            
            return {
                "disponible": modelo_disponible,
                "modelos": modelos,
                "error": None if modelo_disponible else f"Modelo '{self.modelo}' no encontrado"
            }
            
        except Exception as e:
            return {
                "disponible": False,
                "modelos": [],
                "error": str(e)
            }
