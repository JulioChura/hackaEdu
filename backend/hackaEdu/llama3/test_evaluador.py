"""
Script de prueba para el módulo de evaluación con IA
Proyecto: ReConéctate IA - Hackathon 2025

Este script te permite probar el evaluador sin tener toda la BD configurada.
Usa datos de ejemplo del PDF del proyecto (caso "Mi Lenguaje Corporal").
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from prompts import construir_prompt
from evaluador import EvaluadorIA
import json


def datos_ejemplo_lenguaje_corporal():
    """
    Datos de ejemplo del caso real del PDF:
    Sesión: "Mi Lenguaje Corporal" - 5to grado primaria
    Alumno: Miguel Torres
    """
    return {
        'sesion': {
            'nombre': 'Mi Lenguaje Corporal',
            'tema': 'Comunicación y Expresión Oral',
            'objetivo': 'Desarrollar habilidades básicas de expresión oral mediante el reconocimiento y uso del lenguaje corporal',
            'nivel_educativo': '5to grado primaria'
        },
        'criterios': [
            {
                'criterio_id': 1,
                'nombre_criterio': 'Reconocimiento de Gestos Básicos',
                'descripcion': 'Identifica gestos comunes en la comunicación y explica su función',
                'peso': 4.0
            },
            {
                'criterio_id': 2,
                'nombre_criterio': 'Expresión de Emociones con el Cuerpo',
                'descripcion': 'Relaciona expresiones corporales con emociones básicas',
                'peso': 5.0
            },
            {
                'criterio_id': 3,
                'nombre_criterio': 'Postura al Hablar',
                'descripcion': 'Comprende la importancia de la postura en la comunicación efectiva',
                'peso': 4.5
            }
        ],
        'respuestas': [
            {
                'respuesta_id': 1,
                'pregunta': 'Nombra 3 gestos que usamos al hablar y explica para qué sirven',
                'texto_respuesta': 'Los gestos que usamos son: mover las manos para explicar cosas, asentir con la cabeza cuando estamos de acuerdo y sonreír cuando estamos contentos. Sirven para que nos entiendan mejor.',
                'criterios_vinculados': [1, 2]  # Esta pregunta evalúa criterios 1 y 2
            },
            {
                'respuesta_id': 2,
                'pregunta': '¿Cómo mostramos con nuestro cuerpo cuando estamos contentos o tristes?',
                'texto_respuesta': 'Cuando estamos contentos saltamos y reímos, y cuando estamos tristes bajamos la cabeza y no miramos a los ojos. También nuestros hombros se caen cuando estamos tristes.',
                'criterios_vinculados': [2]  # Solo criterio 2
            },
            {
                'respuesta_id': 3,
                'pregunta': '¿Por qué es importante tener buena postura cuando hablamos con otras personas?',
                'texto_respuesta': 'Es importante tener buena postura porque así las personas nos toman más en serio y podemos respirar mejor para hablar más claro.',
                'criterios_vinculados': [3]  # Solo criterio 3
            }
        ],
        'alumno': {
            'alumno_id': 123,
            'nombre': 'Miguel Torres',
            'grado': '5to grado'
        },
        'evaluacion_id': 456
    }


def probar_construccion_prompt():
    """
    Prueba 1: Verificar que el prompt se construye correctamente
    """
    print("=" * 80)
    print("PRUEBA 1: Construcción de Prompt")
    print("=" * 80)
    
    datos = datos_ejemplo_lenguaje_corporal()
    prompt = construir_prompt(datos)
    
    print(f"\n✅ Prompt generado exitosamente")
    print(f"📏 Longitud: {len(prompt)} caracteres")
    print(f"📊 Criterios incluidos: {len(datos['criterios'])}")
    print(f"📝 Respuestas incluidas: {len(datos['respuestas'])}")
    
    print("\n" + "-" * 80)
    print("CONTENIDO DEL PROMPT:")
    print("-" * 80)
    print(prompt[:1000] + "\n...\n" + prompt[-500:])
    print("-" * 80)
    
    return prompt


def probar_conexion_ollama():
    """
    Prueba 2: Verificar que Ollama está disponible
    """
    print("\n" + "=" * 80)
    print("PRUEBA 2: Verificación de Ollama")
    print("=" * 80)
    
    evaluador = EvaluadorIA()
    resultado = evaluador.verificar_conexion_ollama()
    
    if resultado['disponible']:
        print(f"\n✅ Ollama está disponible")
        print(f"🤖 Modelos instalados: {', '.join(resultado['modelos'])}")
        print(f"✓ Modelo '{evaluador.modelo}' encontrado")
    else:
        print(f"\n❌ Ollama NO está disponible")
        print(f"⚠️  Error: {resultado['error']}")
        print(f"📋 Modelos instalados: {resultado['modelos']}")
        print("\n💡 SOLUCIÓN:")
        print("   1. Instala Ollama: https://ollama.com/download")
        print(f"   2. Descarga el modelo: ollama pull {evaluador.modelo}")
        print("   3. Verifica que esté corriendo: ollama list")
    
    return resultado['disponible']


def probar_evaluacion_completa():
    """
    Prueba 3: Evaluación completa con IA (requiere Ollama funcionando)
    """
    print("\n" + "=" * 80)
    print("PRUEBA 3: Evaluación Completa con IA")
    print("=" * 80)
    
    datos = datos_ejemplo_lenguaje_corporal()
    evaluador = EvaluadorIA()
    
    # Construir prompt
    prompt = evaluador._construir_prompt(datos)
    print(f"\n📝 Prompt construido ({len(prompt)} caracteres)")
    
    # Llamar a IA
    print("🤖 Llamando a Ollama... (esto puede tardar 10-30 segundos)")
    try:
        respuesta_ia = evaluador._llamar_ia(prompt, timeout=60)
        print(f"✅ Respuesta recibida ({len(respuesta_ia)} caracteres)")
        
        # Parsear respuesta
        print("🔍 Parseando JSON...")
        evaluaciones = evaluador._parsear_respuesta(respuesta_ia)
        print(f"✅ JSON parseado exitosamente")
        
        # Validar
        print("✓ Validando estructura...")
        evaluador._validar_evaluaciones(evaluaciones, datos)
        print(f"✅ Validación exitosa")
        
        # Mostrar resultados
        print("\n" + "-" * 80)
        print("RESULTADOS DE LA EVALUACIÓN:")
        print("-" * 80)
        print(json.dumps(evaluaciones, indent=2, ensure_ascii=False))
        print("-" * 80)
        
        # Estadísticas
        num_evaluaciones = len(evaluaciones.get('evaluaciones', []))
        puntaje_promedio = sum(
            e['puntaje_obtenido'] for e in evaluaciones['evaluaciones']
        ) / num_evaluaciones if num_evaluaciones > 0 else 0
        
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   - Evaluaciones generadas: {num_evaluaciones}")
        print(f"   - Puntaje promedio: {puntaje_promedio:.2f} / 5.0")
        print(f"   - Fortalezas identificadas: {len(evaluaciones.get('fortalezas', []))}")
        print(f"   - Áreas de mejora: {len(evaluaciones.get('areas_mejora', []))}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error en evaluación: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def menu_principal():
    """
    Menú interactivo para ejecutar las pruebas
    """
    print("\n" + "=" * 80)
    print("🧪 PRUEBAS DEL MÓDULO DE EVALUACIÓN CON IA")
    print("Proyecto: ReConéctate IA - Hackathon 2025")
    print("=" * 80)
    
    print("\nSelecciona una opción:")
    print("  1. Probar construcción de prompt")
    print("  2. Verificar conexión con Ollama")
    print("  3. Evaluación completa con IA (requiere Ollama)")
    print("  4. Ejecutar todas las pruebas")
    print("  0. Salir")
    
    opcion = input("\nOpción: ").strip()
    
    if opcion == "1":
        probar_construccion_prompt()
    elif opcion == "2":
        probar_conexion_ollama()
    elif opcion == "3":
        if probar_conexion_ollama():
            probar_evaluacion_completa()
        else:
            print("\n⚠️  No se puede ejecutar sin Ollama. Configúralo primero.")
    elif opcion == "4":
        probar_construccion_prompt()
        if probar_conexion_ollama():
            probar_evaluacion_completa()
    elif opcion == "0":
        print("\n👋 ¡Hasta luego!")
        return
    else:
        print("\n❌ Opción inválida")
    
    # Volver al menú
    input("\n\nPresiona Enter para continuar...")
    menu_principal()


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
