import json
import requests
import re
import logging
from datetime import datetime
from django.db import transaction
from django.conf import settings

logger = logging.getLogger(__name__)


class EvaluadorIA:
    
    def __init__(self, modo=None, modelo_groq=None, modelo_ollama=None, url_ollama=None):
        """
        Inicializa el evaluador con soporte para Groq (API rápida) y Ollama (local fallback)
        
        Args:
            modo: 'groq', 'ollama', 'auto' (default: settings.IA_MODE)
            modelo_groq: Modelo de Groq a usar (default: settings.GROQ_MODEL)
            modelo_ollama: Modelo de Ollama a usar (default: settings.OLLAMA_MODEL)
            url_ollama: URL de Ollama (default: settings.OLLAMA_URL)
        """
        self.modo = modo or settings.IA_MODE
        self.modelo_groq = modelo_groq or settings.GROQ_MODEL
        self.modelo_ollama = modelo_ollama or settings.OLLAMA_MODEL
        self.url_ollama = url_ollama or settings.OLLAMA_URL
        self.groq_api_key = settings.GROQ_API_KEY
        
        logger.info(f"EvaluadorIA inicializado - Modo: {self.modo}, Groq: {self.modelo_groq}, Ollama: {self.modelo_ollama}")
    
    def evaluar_respuestas(self, evaluacion_id, alumno_id):
        try:
            logger.info(f"Iniciando evaluación - Evaluacion: {evaluacion_id}, Alumno: {alumno_id}")
            
            datos = self._obtener_datos_evaluacion(evaluacion_id, alumno_id)
            logger.info(f"Datos obtenidos: {len(datos['respuestas'])} respuestas, {len(datos['criterios'])} criterios")
            
            prompt = self._construir_prompt(datos)
            logger.debug(f"Prompt construido (longitud: {len(prompt)} caracteres)")
            
            respuesta_ia = self._llamar_ia(prompt)
            logger.info("Respuesta de IA recibida")
            
            evaluaciones = self._parsear_respuesta(respuesta_ia)
            logger.info(f"Respuesta parseada: {len(evaluaciones.get('evaluaciones', []))} evaluaciones")
            
            self._validar_evaluaciones(evaluaciones, datos)
            
            reporte = self._guardar_evaluaciones(evaluaciones)
            logger.info(f"Evaluaciones guardadas - Reporte ID: {reporte.id}")
            
            return {
                "success": True,
                "data": evaluaciones,
                "reporte_id": reporte.id
            }
            
        except Exception as e:
            logger.error(f"Error en evaluación: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    def _obtener_datos_evaluacion(self, evaluacion_id, alumno_id):
        from evaluacion.models import Evaluacion, Pregunta, RespuestaAlumno, PreguntaCriterio
        from profesores.models import Sesion, CriterioEvaluacion, Tema, Curso, NivelEducativo
        from alumnos.models import Alumno
        
        try:
            evaluacion = Evaluacion.objects.select_related(
                'sesion__tema__curso__nivel',
                'docente'
            ).get(id=evaluacion_id)
            
            sesion = evaluacion.sesion
            tema = sesion.tema
            curso = tema.curso
            nivel = curso.nivel
            
            alumno = Alumno.objects.select_related('usuario').get(id=alumno_id)
            
            criterios_queryset = CriterioEvaluacion.objects.filter(
                sesion=sesion
            ).order_by('orden')
            
            criterios = []
            for criterio in criterios_queryset:
                criterios.append({
                    'criterio_id': criterio.id,
                    'nombre_criterio': criterio.nombre_criterio,
                    'descripcion': criterio.descripcion,
                    'peso': float(criterio.peso)
                })
            
            respuestas_queryset = RespuestaAlumno.objects.filter(
                evaluacion=evaluacion,
                alumno=alumno
            ).select_related('pregunta')
            
            respuestas = []
            for respuesta in respuestas_queryset:
                criterios_vinculados = PreguntaCriterio.objects.filter(
                    pregunta=respuesta.pregunta,
                    activo=True
                ).values_list('criterio_id', flat=True)
                
                respuestas.append({
                    'respuesta_id': respuesta.id,
                    'pregunta': respuesta.pregunta.texto_pregunta,
                    'texto_respuesta': respuesta.texto_respuesta,
                    'criterios_vinculados': list(criterios_vinculados)
                })
            
            datos = {
                'sesion': {
                    'nombre': sesion.nombre_sesion,
                    'tema': tema.nombre_tema if tema else 'Sin tema',
                    'objetivo': sesion.objetivo_sesion,
                    'nivel_educativo': f"{nivel.nombre}" if nivel else 'Sin nivel'
                },
                'criterios': criterios,
                'respuestas': respuestas,
                'alumno': {
                    'alumno_id': alumno.id,
                    'nombre': f"{alumno.usuario.nombres} {alumno.usuario.apellidos}",
                    'grado': alumno.grado_actual
                },
                'evaluacion_id': evaluacion_id
            }
            
            logger.info(f"Datos obtenidos: {len(criterios)} criterios, {len(respuestas)} respuestas")
            return datos
            
        except Evaluacion.DoesNotExist:
            logger.error(f"Evaluación {evaluacion_id} no encontrada")
            raise ValueError(f"Evaluación {evaluacion_id} no existe")
        except Alumno.DoesNotExist:
            logger.error(f"Alumno {alumno_id} no encontrado")
            raise ValueError(f"Alumno {alumno_id} no existe")
        except Exception as e:
            logger.error(f"Error obteniendo datos de BD: {str(e)}", exc_info=True)
            raise
    
    def _construir_prompt(self, datos):
        from .prompts import construir_prompt
        return construir_prompt(datos)
    
    def _llamar_ia(self, prompt, timeout=60):
        """
        Llama a la IA según el modo configurado.
        Modo 'auto': intenta Groq primero, luego Ollama como fallback
        """
        if self.modo == 'groq':
            return self._llamar_groq(prompt)
        elif self.modo == 'ollama':
            return self._llamar_ollama(prompt, timeout)
        else:  # modo 'auto'
            try:
                logger.info("Modo AUTO: Intentando con Groq primero...")
                return self._llamar_groq(prompt)
            except Exception as e:
                logger.warning(f"Groq falló ({str(e)}), intentando con Ollama local...")
                return self._llamar_ollama(prompt, timeout)
    
    def _llamar_groq(self, prompt):
        """
        Llama a Groq API (rápida, en la nube)
        """
        try:
            from groq import Groq
            
            if not self.groq_api_key or self.groq_api_key == 'gsk_pendiente':
                raise ValueError("API Key de Groq no configurada")
            
            client = Groq(api_key=self.groq_api_key)
            
            logger.info(f"Llamando a Groq API con modelo: {self.modelo_groq}")
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un evaluador pedagógico experto. Responde ÚNICAMENTE con JSON válido, sin markdown ni texto adicional."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.modelo_groq,
                temperature=0.2,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            respuesta = chat_completion.choices[0].message.content
            logger.info(f"✓ Respuesta de Groq recibida ({len(respuesta)} caracteres)")
            return respuesta
            
        except Exception as e:
            logger.error(f"Error llamando a Groq: {str(e)}")
            raise
    
    def _llamar_ollama(self, prompt, timeout=180):
        """
        Llama a Ollama local (más lento pero gratuito y privado)
        """
        url = f"{self.url_ollama}/api/generate"
        
        payload = {
            "model": self.modelo_ollama,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9,
                "num_predict": 2000,
                "num_ctx": 4096
            }
        }
        
        try:
            logger.info(f"Llamando a Ollama local: {self.modelo_ollama}")
            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()
            
            resultado = response.json()
            texto_respuesta = resultado.get('response', '')
            
            if not texto_respuesta:
                raise ValueError("Ollama devolvió respuesta vacía")
            
            logger.info(f"✓ Respuesta de Ollama recibida ({len(texto_respuesta)} caracteres)")
            return texto_respuesta
            
        except requests.Timeout:
            raise TimeoutError(f"La llamada a Ollama superó el timeout de {timeout}s")
        except requests.RequestException as e:
            raise Exception(f"Error conectando con Ollama: {str(e)}")
    
    def _parsear_respuesta(self, texto_respuesta):
        try:
            return json.loads(texto_respuesta)
        except json.JSONDecodeError:
            logger.warning("JSON directo falló, intentando extraer de texto...")
            
            match = re.search(r'\{.*\}', texto_respuesta, re.DOTALL)
            
            if match:
                json_str = match.group()
                try:
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON extraído inválido: {str(e)}")
                    raise ValueError(f"JSON extraído es inválido: {str(e)}")
            else:
                logger.error("No se encontró estructura JSON en la respuesta")
                raise ValueError("No se pudo encontrar JSON en la respuesta de la IA")
    
    def _validar_evaluaciones(self, evaluaciones, datos_originales):
        campos_requeridos = ['alumno_id', 'evaluacion_id', 'evaluaciones', 'diagnostico_general']
        for campo in campos_requeridos:
            if campo not in evaluaciones:
                raise ValueError(f"Campo requerido faltante en respuesta: {campo}")
        
        if not evaluaciones['evaluaciones']:
            raise ValueError("No se generaron evaluaciones")
        
        for i, eval_item in enumerate(evaluaciones['evaluaciones']):
            campos_eval = ['respuesta_id', 'criterio_id', 'puntaje_obtenido', 'puntaje_maximo', 
                          'justificacion', 'evidencia']
            for campo in campos_eval:
                if campo not in eval_item:
                    raise ValueError(f"Evaluación {i}: falta campo '{campo}'")
            
            puntaje = eval_item['puntaje_obtenido']
            if not (0.0 <= puntaje <= 5.0):
                logger.warning(f"Puntaje fuera de rango: {puntaje}, ajustando...")
                eval_item['puntaje_obtenido'] = max(0.0, min(5.0, puntaje))
        
        logger.info(f"Validación exitosa: {len(evaluaciones['evaluaciones'])} evaluaciones válidas")
    
    def _guardar_evaluaciones(self, evaluaciones):
        from reportes.models import EvaluacionCriterioRespuesta, ReporteIA
        from evaluacion.models import Evaluacion, RespuestaAlumno
        from alumnos.models import Alumno
        from profesores.models import NivelDesempeno
        from django.db import transaction
        from datetime import datetime
        
        try:
            with transaction.atomic():
                evaluacion = Evaluacion.objects.get(id=evaluaciones['evaluacion_id'])
                alumno = Alumno.objects.get(id=evaluaciones['alumno_id'])
                
                if evaluaciones['evaluaciones']:
                    puntajes = [e['puntaje_obtenido'] for e in evaluaciones['evaluaciones']]
                    puntaje_total = sum(puntajes) / len(puntajes)
                else:
                    puntaje_total = 0.0
                
                nivel_desempeno = NivelDesempeno.objects.filter(
                    puntaje_minimo__lte=puntaje_total,
                    puntaje_maximo__gte=puntaje_total
                ).first()
                
                reporte = ReporteIA.objects.create(
                    evaluacion=evaluacion,
                    alumno=alumno,
                    puntaje_total=puntaje_total,
                    nivel_desempeno=nivel_desempeno,
                    diagnostico_general=evaluaciones.get('diagnostico_general', ''),
                    fortalezas_identificadas='\n'.join(evaluaciones.get('fortalezas', [])),
                    areas_mejora='\n'.join(evaluaciones.get('areas_mejora', [])),
                    fecha_generacion=datetime.now()
                )
                
                logger.info(f"Reporte creado: ID={reporte.id}, Puntaje={puntaje_total:.2f}")
                
                evaluaciones_guardadas = 0
                for eval_item in evaluaciones['evaluaciones']:
                    try:
                        respuesta = RespuestaAlumno.objects.get(id=eval_item['respuesta_id'])
                        
                        EvaluacionCriterioRespuesta.objects.create(
                            respuesta=respuesta,
                            criterio_id=eval_item['criterio_id'],
                            puntaje_obtenido=eval_item['puntaje_obtenido'],
                            puntaje_maximo=eval_item.get('puntaje_maximo', 5.0),
                            justificacion=eval_item['justificacion'],
                            evidencia=eval_item.get('evidencia', ''),
                            fecha_evaluacion=datetime.now()
                        )
                        evaluaciones_guardadas += 1
                        
                    except RespuestaAlumno.DoesNotExist:
                        logger.error(f"Respuesta {eval_item['respuesta_id']} no encontrada")
                        continue
                    except Exception as e:
                        logger.error(f"Error guardando evaluación: {str(e)}")
                        continue
                
                logger.info(f"Guardadas {evaluaciones_guardadas} evaluaciones")
                
                return reporte
                
        except Evaluacion.DoesNotExist:
            logger.error(f"Evaluación {evaluaciones['evaluacion_id']} no encontrada")
            raise ValueError(f"Evaluación no existe")
        except Alumno.DoesNotExist:
            logger.error(f"Alumno {evaluaciones['alumno_id']} no encontrado")
            raise ValueError(f"Alumno no existe")
        except Exception as e:
            logger.error(f"Error guardando evaluaciones: {str(e)}", exc_info=True)
            raise
    
    def verificar_conexion_ia(self):
        """
        Verifica la conexión con Groq y/o Ollama según el modo configurado
        """
        resultado = {
            "modo": self.modo,
            "groq": {"disponible": False, "modelo": self.modelo_groq, "error": None},
            "ollama": {"disponible": False, "modelos": [], "error": None}
        }
        
        # Verificar Groq
        if self.modo in ['groq', 'auto']:
            try:
                from groq import Groq
                
                if self.groq_api_key and self.groq_api_key != 'gsk_pendiente':
                    client = Groq(api_key=self.groq_api_key)
                    # Intentar una llamada simple para verificar
                    client.chat.completions.create(
                        messages=[{"role": "user", "content": "test"}],
                        model=self.modelo_groq,
                        max_tokens=5
                    )
                    resultado["groq"]["disponible"] = True
                    logger.info("✓ Groq API disponible")
                else:
                    resultado["groq"]["error"] = "API Key no configurada"
                    
            except Exception as e:
                resultado["groq"]["error"] = str(e)
                logger.warning(f"Groq no disponible: {str(e)}")
        
        # Verificar Ollama
        if self.modo in ['ollama', 'auto']:
            try:
                response = requests.get(f"{self.url_ollama}/api/tags", timeout=5)
                response.raise_for_status()
                
                modelos_data = response.json()
                modelos = [m['name'] for m in modelos_data.get('models', [])]
                resultado["ollama"]["modelos"] = modelos
                resultado["ollama"]["disponible"] = self.modelo_ollama in modelos
                
                if not resultado["ollama"]["disponible"]:
                    resultado["ollama"]["error"] = f"Modelo '{self.modelo_ollama}' no encontrado"
                else:
                    logger.info(f"✓ Ollama disponible con {len(modelos)} modelos")
                    
            except Exception as e:
                resultado["ollama"]["error"] = str(e)
                logger.warning(f"Ollama no disponible: {str(e)}")
        
        # Determinar disponibilidad general
        if self.modo == 'groq':
            resultado["disponible"] = resultado["groq"]["disponible"]
        elif self.modo == 'ollama':
            resultado["disponible"] = resultado["ollama"]["disponible"]
        else:  # auto
            resultado["disponible"] = resultado["groq"]["disponible"] or resultado["ollama"]["disponible"]
        
        return resultado
    
    # Mantener compatibilidad con código anterior
    def verificar_conexion_ollama(self):
        """Método legacy, usa verificar_conexion_ia() en su lugar"""
        resultado_completo = self.verificar_conexion_ia()
        return {
            "disponible": resultado_completo["ollama"]["disponible"],
            "modelos": resultado_completo["ollama"]["modelos"],
            "error": resultado_completo["ollama"]["error"]
        }

