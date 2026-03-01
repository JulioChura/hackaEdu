import api from "../lib/axios";

/**
 * Servicio para interactuar con el LLM (generación de lecturas con IA)
 */
export const llmService = {
  /**
   * Genera una lectura con preguntas usando IA
   * @param {Object} data - Datos para generar la lectura
   * @param {string} data.tema - Tema de la lectura
   * @param {string} data.nivel - Nivel CEFR (A1, A2, B1, B2, C1, C2)
   * @param {string} data.categoria - Código de la categoría
   * @param {string} data.modalidad - Código de la modalidad (ej: "IA_GENERADA")
   * @param {number} data.cantidad_preguntas - Cantidad de preguntas a generar (1-10)
   * @param {Array<string>} data.tags - Tags opcionales para personalizar
   * @returns {Promise} - Promise con la lectura y preguntas generadas
   */
  createReadingWithQuestions(data) {
    return api.post('/api/llm/create-reading-with-questions/', data)
  }
}
