import api from "../lib/axios";

/**
 * Servicio para manejar categorías de contenido
 */
export const categoriesService = {
  /**
   * Obtiene todas las categorías disponibles
   * @returns {Promise} - Promise con array de categorías
   */
  getAll() {
    return api.get('/contenido/categorias/')
  },

  /**
   * Obtiene una categoría específica por código
   * @param {string} codigo - Código de la categoría
   * @returns {Promise} - Promise con los datos de la categoría
   */
  getByCode(codigo) {
    return api.get(`/contenido/categorias/${codigo}/`)
  }
}
