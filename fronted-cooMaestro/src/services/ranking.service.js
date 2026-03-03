/**
 * Ranking Service — Global leaderboard API calls
 *
 * Endpoints used:
 *   GET /usuarios/dashboard/global-ranking/?limit=50
 *     → { userRank, userPoints, userTopPercentage, totalUsers, topThree, leaderboard }
 */

import api from '../lib/axios'

export const rankingService = {
  /**
   * Fetch the full global leaderboard.
   *
   * @param {number} limit  Max rows for the leaderboard section (default 50, max 200)
   * @returns {Promise}
   */
  getGlobalRanking(limit = 50) {
    return api.get('/usuarios/dashboard/global-ranking/', { params: { limit } })
  },
}
