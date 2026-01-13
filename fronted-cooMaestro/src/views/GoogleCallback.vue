<template>
  <div class="callback-container">
    <div class="loading">
      <div class="spinner"></div>
      <h2>{{ message }}</h2>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const message = ref('Completando autenticación con Google...');
const error = ref('');

onMounted(async () => {
  try {
    // Llamar al backend para convertir la sesión en JWT tokens
    const response = await axios.get('http://localhost:8000/api/auth/convert-token/', {
      withCredentials: true // Importante: enviar cookies de sesión
    });
    
    // Guardar tokens JWT
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    
    // Guardar info del usuario
    localStorage.setItem('user', JSON.stringify(response.data.user));
    
    message.value = '¡Éxito! Redirigiendo...';
    
    // Redirigir al dashboard
    setTimeout(() => {
      router.push('/dashboard');
    }, 1000);
    
  } catch (err) {
    console.error('Error al obtener tokens:', err);
    error.value = 'Error al completar autenticación. Intenta nuevamente.';
    
    // Redirigir al login después de 3 segundos
    setTimeout(() => {
      router.push('/login');
    }, 3000);
  }
});
</script>

<style scoped>
.callback-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.loading {
  background: white;
  border-radius: 12px;
  padding: 48px;
  text-align: center;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 24px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

h2 {
  color: #333;
  margin: 0 0 16px;
  font-size: 24px;
}

p {
  color: #666;
  margin: 0;
}

.error {
  color: #c33;
  margin-top: 16px;
}
</style>
