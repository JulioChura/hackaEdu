/**
 * Achievements Service — Logros del usuario
 */

import api from '../lib/axios'

export const achievementsService = {
  /**
   * Obtiene todos los logros con estado unlocked/locked del usuario autenticado.
   *
   * @returns {Promise} { achievements: [...], unlockedCount, totalCount }
   */
  getAll() {
    return api.get('/logros/')
  }
}
