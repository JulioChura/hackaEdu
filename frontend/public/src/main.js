import { verificarIA, probarPrompt, ejecutarEvaluacion } from './api.js';

const $ = sel => document.querySelector(sel);

// IA status
$('#check-ia').addEventListener('click', async () => {
  const btn = $('#check-ia');
  btn.disabled = true; btn.textContent = 'Verificando...';
  try {
    const r = await verificarIA();
    $('#ia-output').textContent = JSON.stringify(r, null, 2);
  } catch (e) {
    $('#ia-output').textContent = 'Error: ' + e.message;
  }
  btn.disabled = false; btn.textContent = 'Verificar IA';
});

// Prompt generator
$('#gen-prompt').addEventListener('click', async () => {
  const btn = $('#gen-prompt');
  const evalId = Number($('#eval-id').value);
  const alumnoId = Number($('#alumno-id').value);
  btn.disabled = true; btn.textContent = 'Generando...';
  $('#prompt-output').textContent = 'Generando...';
  try {
    const r = await probarPrompt(evalId, alumnoId);
    $('#prompt-output').textContent = r.prompt || JSON.stringify(r, null, 2);
  } catch (e) {
    $('#prompt-output').textContent = 'Error: ' + e.message;
  }
  btn.disabled = false; btn.textContent = 'Generar prompt';
});

// Run evaluation
$('#run-eval-btn').addEventListener('click', async () => {
  const btn = $('#run-eval-btn');
  const evalId = Number($('#eval-id-2').value);
  const alumnoId = Number($('#alumno-id-2').value);
  btn.disabled = true; btn.textContent = 'Ejecutando...';
  $('#eval-output').textContent = 'Ejecutando evaluación... Esto puede tardar.';
  try {
    const r = await ejecutarEvaluacion(evalId, alumnoId);
    $('#eval-output').textContent = JSON.stringify(r, null, 2);
  } catch (e) {
    $('#eval-output').textContent = 'Error: ' + e.message;
  }
  btn.disabled = false; btn.textContent = 'Ejecutar';
});
