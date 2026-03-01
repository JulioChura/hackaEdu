import api from "../lib/axios";

/**
 * Servicio para manejar modalidades de contenido
 */
export const modalidadesService = {
  /**
   * Obtiene todas las modalidades disponibles
   * @returns {Promise} - Promise con array de modalidades
   */
  getAll() {
    return api.get('/contenido/modalidades/')
  },

  /**
   * Obtiene una modalidad específica por código
   * @param {string} codigo - Código de la modalidad
   * @returns {Promise} - Promise con los datos de la modalidad
   */
  getByCode(codigo) {
    return api.get(`/contenido/modalidades/${codigo}/`)
  }
}
