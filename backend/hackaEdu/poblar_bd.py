import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaEdu.settings')
django.setup()

from usuario.models import RolUsuario, Usuario
from profesores.models import NivelEducativo, Materia, Docente, NivelDesempeno, Curso, Tema, Sesion, CriterioEvaluacion
from alumnos.models import Alumno, Inscripcion
from evaluacion.models import Pregunta, PreguntaCriterio, Evaluacion, RespuestaAlumno
from datetime import datetime, timedelta

def poblar_bd():
    print("=== Poblando BD con datos de prueba ===\n")
    
    # 1. Roles
    rol_docente, _ = RolUsuario.objects.get_or_create(nombre='Docente')
    rol_alumno, _ = RolUsuario.objects.get_or_create(nombre='Alumno')
    print("✓ Roles creados")
    
    # 2. Nivel Educativo
    nivel_primaria, _ = NivelEducativo.objects.get_or_create(
        nombre='Primaria',
        defaults={'ciclo': 'III'}
    )
    print("✓ Nivel educativo creado")
    
    # 3. Materia
    materia_comunicacion, _ = Materia.objects.get_or_create(
        nombre='Comunicación',
        defaults={'area': 'Comunicación y Lenguaje'}
    )
    print("✓ Materia creada")
    
    # 4. Niveles de Desempeño
    niveles = [
        ('Excelente', 4.5, 5.0, '#4CAF50'),
        ('Bueno', 3.5, 4.49, '#2196F3'),
        ('Regular', 2.5, 3.49, '#FFC107'),
        ('Deficiente', 0, 2.49, '#F44336')
    ]
    for nombre, min_p, max_p, color in niveles:
        NivelDesempeno.objects.get_or_create(
            nombre=nombre,
            defaults={
                'puntaje_minimo': min_p,
                'puntaje_maximo': max_p,
                'color': color
            }
        )
    print("✓ Niveles de desempeño creados")
    
    # 5. Usuario Docente
    docente_user, created = Usuario.objects.get_or_create(
        email='profesor@hackaedu.com',
        defaults={
            'nombres': 'María',
            'apellidos': 'González',
            'rol': rol_docente,
            'activo': True
        }
    )
    if created:
        docente_user.set_password('hackaedu2025')
        docente_user.save()
    print("✓ Usuario docente creado")
    
    # 6. Docente
    docente, _ = Docente.objects.get_or_create(
        usuario=docente_user,
        defaults={
            'especialidad': 'Comunicación y Expresión Oral',
            'institucion': 'Colegio San Martín'
        }
    )
    print("✓ Docente creado")
    
    # 7. Usuario Alumno
    alumno_user, created = Usuario.objects.get_or_create(
        email='miguel@estudiante.com',
        defaults={
            'nombres': 'Miguel',
            'apellidos': 'Torres',
            'rol': rol_alumno,
            'fecha_nacimiento': '2014-05-15',
            'activo': True
        }
    )
    if created:
        alumno_user.set_password('hackaedu2025')
        alumno_user.save()
    print("✓ Usuario alumno creado")
    
    # 8. Alumno
    alumno, _ = Alumno.objects.get_or_create(
        usuario=alumno_user,
        defaults={
            'nivel': nivel_primaria,
            'grado_actual': '5to grado',
            'colegio': 'IE San Martín'
        }
    )
    print("✓ Alumno creado")
    
    # 9. Curso
    curso, _ = Curso.objects.get_or_create(
        codigo_curso='COM5A',
        defaults={
            'docente': docente,
            'nivel': nivel_primaria,
            'materia': materia_comunicacion,
            'nombre_curso': 'Comunicación 5to Grado',
            'objetivo': 'Desarrollar habilidades comunicativas orales y escritas',
            'descripcion': 'Curso de comunicación para 5to grado de primaria',
            'activo': True
        }
    )
    print("✓ Curso creado")
    
    # 10. Inscripción
    Inscripcion.objects.get_or_create(
        alumno=alumno,
        curso=curso,
        defaults={'codigo_acceso': 'COM5A', 'estado': 'activo'}
    )
    print("✓ Inscripción creada")
    
    # 11. Tema
    tema, _ = Tema.objects.get_or_create(
        curso=curso,
        orden=1,
        defaults={
            'nombre_tema': 'Comunicación y Expresión Oral',
            'descripcion': 'Desarrollo de expresión oral mediante lenguaje corporal',
            'semanas_estimadas': 2
        }
    )
    print("✓ Tema creado")
    
    # 12. Sesión
    sesion, _ = Sesion.objects.get_or_create(
        tema=tema,
        orden=1,
        defaults={
            'nombre_sesion': 'Mi Lenguaje Corporal',
            'objetivo_sesion': 'Desarrollar habilidades básicas de expresión oral',
            'horas_estimadas': 2
        }
    )
    print("✓ Sesión creada")
    
    # 13. Criterios de Evaluación
    criterios_data = [
        ('Reconocimiento de Gestos Básicos', 'Identifica gestos comunes en la comunicación', 4.0, 1),
        ('Expresión de Emociones con el Cuerpo', 'Relaciona expresiones corporales con emociones', 5.0, 2),
        ('Postura al Hablar', 'Comprende la importancia de la postura', 4.5, 3)
    ]
    
    criterios = []
    for nombre, desc, peso, orden in criterios_data:
        c, _ = CriterioEvaluacion.objects.get_or_create(
            sesion=sesion,
            orden=orden,
            defaults={
                'nombre_criterio': nombre,
                'descripcion': desc,
                'peso': peso
            }
        )
        criterios.append(c)
    print("✓ Criterios creados")
    
    # 14. Evaluación
    evaluacion, _ = Evaluacion.objects.get_or_create(
        sesion=sesion,
        docente=docente,
        defaults={
            'titulo_evaluacion': 'Evaluación - Lenguaje Corporal',
            'instrucciones': 'Responde las siguientes preguntas sobre lenguaje corporal',
            'fecha_aplicacion': datetime.now(),
            'fecha_limite': datetime.now() + timedelta(days=7),
            'tiempo_limite': 30,
            'intentos_permitidos': 1,
            'mostrar_resultados': True,
            'activo': True
        }
    )
    print("✓ Evaluación creada")
    
    # 15. Preguntas con vinculación a criterios
    preguntas_data = [
        ('Nombra 3 gestos que usamos al hablar y explica para qué sirven', 1, [0, 1]),
        ('¿Cómo mostramos con nuestro cuerpo cuando estamos contentos o tristes?', 2, [1]),
        ('¿Por qué es importante tener buena postura cuando hablamos?', 3, [2])
    ]
    
    preguntas = []
    for texto, orden, criterios_idx in preguntas_data:
        p, _ = Pregunta.objects.get_or_create(
            sesion=sesion,
            orden=orden,
            defaults={'texto_pregunta': texto}
        )
        
        for idx in criterios_idx:
            PreguntaCriterio.objects.get_or_create(
                pregunta=p,
                criterio=criterios[idx],
                defaults={'activo': True}
            )
        
        preguntas.append(p)
    print("✓ Preguntas creadas")
    
    # 16. Respuestas del Alumno
    respuestas_data = [
        'Los gestos que usamos son: mover las manos para explicar cosas, asentir con la cabeza cuando estamos de acuerdo y sonreír cuando estamos contentos. Sirven para que nos entiendan mejor.',
        'Cuando estamos contentos saltamos y reímos, y cuando estamos tristes bajamos la cabeza y no miramos a los ojos. También nuestros hombros se caen cuando estamos tristes.',
        'Es importante tener buena postura porque así las personas nos toman más en serio y podemos respirar mejor para hablar más claro.'
    ]
    
    for pregunta, respuesta in zip(preguntas, respuestas_data):
        RespuestaAlumno.objects.get_or_create(
            evaluacion=evaluacion,
            pregunta=pregunta,
            alumno=alumno,
            defaults={'texto_respuesta': respuesta}
        )
    print("✓ Respuestas creadas")
    
    print("\n" + "="*60)
    print(" DATOS CREADOS EXITOSAMENTE")
    print("="*60)
    print(f"\n IDs para testing:")
    print(f"   Evaluación ID: {evaluacion.id}")
    print(f"   Alumno ID: {alumno.id}")
    print(f"\n Login Admin Django:")
    print(f"   URL: http://localhost:8000/admin")
    print(f"   Email: profesor@hackaedu.com")
    print(f"   Password: hackaedu2025")
    print(f"\n Para probar la IA (Postman o cURL):")
    print(f"   POST http://localhost:8000/api/llama3/evaluar-respuestas/")
    print(f'   {{"evaluacion_id": {evaluacion.id}, "alumno_id": {alumno.id}}}')
    print("\n" + "="*60)

if __name__ == '__main__':
    try:
        poblar_bd()
    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback
        traceback.print_exc()
