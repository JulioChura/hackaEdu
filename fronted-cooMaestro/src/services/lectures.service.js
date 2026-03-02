import api from "../lib/axios";

/**
 * Servicio para manejar lecturas y sesiones de evaluación
 */
export const LecturesService = {
  /**
   * Obtiene lecturas creadas por el usuario autenticado
   * @returns {Promise}
   */
  getMine() {
    return api.get('/contenido/lecturas/mias/')
  },

  /**
   * Obtiene una lectura por id
   * @param {string|number} id
   * @returns {Promise}
   */
  getById(id) {
    return api.get(`/contenido/lecturas/${id}/`)
  },

  /**
   * Inicia (o reanuda) una sesión para una lectura
   * @param {string|number} lecturaId
   * @returns {Promise}
   */
  startSession(lecturaId) {
    return api.post('/evaluacion/sesiones/iniciar/', { lectura_id: lecturaId })
  },

  /**
   * Finaliza sesión enviando respuestas
   * @param {string|number} sesionId
   * @param {Array} respuestas
   * @param {number} tiempoRestanteSegundos
   * @returns {Promise}
   */
  finalizeSession(sesionId, respuestas, tiempoRestanteSegundos = 0) {
    return api.post(`/evaluacion/sesiones/${sesionId}/finalizar/`, {
      respuestas,
      tiempo_restante_segundos: tiempoRestanteSegundos,
    })
  },
}
