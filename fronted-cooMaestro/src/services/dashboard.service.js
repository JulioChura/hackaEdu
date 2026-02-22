/**
 * Dashboard Service - Llamadas API al backend del dashboard
 * 
 * Arquitectura: Frontend hace UNA sola llamada para obtener todos los datos
 * 
 * Endpoint principal:
 * - GET /usuarios/dashboard/full/  → Todos los datos del dashboard
 */

import api from "../lib/axios";

export const dashboardService = {
  /**
   * Obtiene TODOS los datos del dashboard en una sola llamada
   * 
   * @returns {Promise} Objeto con:
   *   - studentData: { userId, fullName, userLevelTitle, avatarUrl, isPro }
   *   - progressData: { currentLevel, levelTitle, currentPoints, nextLevelPoints, nextLevel }
   *   - streakData: { currentStreak, completedDaysThisWeek }
   *   - rankingData: { userRank, userTopPercentage, topPlayers }
   *   - achievementsData: Array de { achievementId, title, description, iconName }
   *   - activeCourses: Array de cursos activos
   */
  getFullDashboard() {
    return api.get('/usuarios/dashboard/full/');
  }
};
