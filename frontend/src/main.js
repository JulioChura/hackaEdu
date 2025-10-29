import { verificarIA, probarPrompt, ejecutarEvaluacion } from './api.js';

const $ = sel => document.querySelector(sel);

// IA status
$('#check-ia').addEventListener('click', async () => {
  $('#ia-output').textContent = 'Verificando...';
  try {
    const r = await verificarIA();
    $('#ia-output').textContent = JSON.stringify(r, null, 2);
  } catch (e) {
    $('#ia-output').textContent = 'Error: ' + e.message;
  }
});

// Prompt generator
$('#gen-prompt').addEventListener('click', async () => {
  const evalId = Number($('#eval-id').value);
  const alumnoId = Number($('#alumno-id').value);
  $('#prompt-output').textContent = 'Generando...';
  try {
    const r = await probarPrompt(evalId, alumnoId);
    $('#prompt-output').textContent = r.prompt || JSON.stringify(r, null, 2);
  } catch (e) {
    $('#prompt-output').textContent = 'Error: ' + e.message;
  }
});

// Run evaluation
$('#run-eval-btn').addEventListener('click', async () => {
  const evalId = Number($('#eval-id-2').value);
  const alumnoId = Number($('#alumno-id-2').value);
  $('#eval-output').textContent = 'Ejecutando evaluación... Esto puede tardar.';
  try {
    const r = await ejecutarEvaluacion(evalId, alumnoId);
    $('#eval-output').textContent = JSON.stringify(r, null, 2);
  } catch (e) {
    $('#eval-output').textContent = 'Error: ' + e.message;
  }
});
