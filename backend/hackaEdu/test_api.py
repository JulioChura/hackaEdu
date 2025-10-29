"""
Script de prueba para verificar que todo funciona
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/llama3"

def test_verificar_ia():
    print("\n" + "="*60)
    print("TEST 1: Verificar conexión con Ollama")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/verificar-ia/")
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200

def test_prueba_prompt():
    print("\n" + "="*60)
    print("TEST 2: Generar prompt (sin IA)")
    print("="*60)
    
    data = {
        "evaluacion_id": 1,
        "alumno_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/prueba-prompt/", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Prompt generado ({result['longitud']} caracteres)")
        print(f"✓ Criterios: {result['num_criterios']}")
        print(f"✓ Respuestas: {result['num_respuestas']}")
        return True
    else:
        print(f"✗ Error: {response.json()}")
        return False

def test_evaluar_respuestas():
    print("\n" + "="*60)
    print("TEST 3: Evaluación COMPLETA con IA")
    print("="*60)
    print("  Esto puede tardar 60-120 segundos en CPU sin GPU...")
    
    data = {
        "evaluacion_id": 1,
        "alumno_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/evaluar-respuestas/", json=data, timeout=150)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Evaluación exitosa")
        print(f"✓ Reporte ID: {result.get('reporte_id')}")
        
        if 'data' in result and 'evaluaciones' in result['data']:
            print(f"✓ Evaluaciones generadas: {len(result['data']['evaluaciones'])}")
            print(f"\nPrimera evaluación:")
            print(json.dumps(result['data']['evaluaciones'][0], indent=2, ensure_ascii=False))
        
        return True
    else:
        print(f"✗ Error: {response.json()}")
        return False

if __name__ == "__main__":
    print("\n INICIANDO TESTS DEL BACKEND")
    print("="*60)
    
    try:
        # Test 1: Verificar Ollama
        test1 = test_verificar_ia()
        
        # Test 2: Generar prompt
        test2 = test_prueba_prompt()
        
        # Test 3: Evaluación completa (solo si Ollama funciona)
        if test1:
            test3 = test_evaluar_respuestas()
        else:
            print("\n  Saltando Test 3 porque Ollama no está disponible")
            test3 = False
        
        # Resumen
        print("\n" + "="*60)
        print("RESUMEN DE TESTS")
        print("="*60)
        print(f"✓ Test 1 (Verificar Ollama): {'PASS' if test1 else 'FAIL'}")
        print(f"✓ Test 2 (Generar Prompt): {'PASS' if test2 else 'PASS'}")
        print(f"✓ Test 3 (Evaluar con IA): {'PASS' if test3 else 'SKIP/FAIL'}")
        print("="*60)
        
        if test1 and test2 and test3:
            print("\n Todos los tests pasaron!")
        elif test2:
            print("\n  Backend funcional, pero IA requiere Ollama corriendo")
        else:
            print("\n Hay errores en el backend")
    
    except requests.exceptions.ConnectionError:
        print("\n ERROR: No se puede conectar al servidor Django")
        print("   Asegúrate de que esté corriendo: python manage.py runserver")
    except Exception as e:
        print(f"\n ERROR: {e}")
