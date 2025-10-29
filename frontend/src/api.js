const API_BASE = 'http://localhost:8000/api/llama3';

async function verificarIA() {
  const res = await fetch(`${API_BASE}/verificar-ia/`);
  return res.json();
}

async function probarPrompt(evaluacion_id, alumno_id) {
  const res = await fetch(`${API_BASE}/prueba-prompt/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ evaluacion_id, alumno_id })
  });
  return res.json();
}

async function ejecutarEvaluacion(evaluacion_id, alumno_id) {
  const res = await fetch(`${API_BASE}/evaluar-respuestas/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ evaluacion_id, alumno_id })
  });
  return res.json();
}

export { verificarIA, probarPrompt, ejecutarEvaluacion };
