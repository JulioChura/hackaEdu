import api from "../lib/axios";
export const authService = {
  login(data) {
    return api.post('/auth/token/', data)
  },

  register(data) {
    return api.post('/auth/register/', data)
  },

  profile() {
    return api.get('/auth/users/profile/')
  },

  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
}
