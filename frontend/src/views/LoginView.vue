<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <div class="auth-logo">&#9835;</div>
        <h1>Учёт сотрудников</h1>
        <p>ГАУК «Брянская областная филармония»</p>
      </div>

      <form @submit.prevent="login" class="auth-form">
        <div class="form-group">
          <label class="form-label">Логин</label>
          <input v-model="username" type="text" class="form-input" placeholder="Введите логин" required />
        </div>
        <div class="form-group">
          <label class="form-label">Пароль</label>
          <input v-model="password" type="password" class="form-input" placeholder="Введите пароль" required />
        </div>
        <p v-if="error" class="auth-error">{{ error }}</p>
        <button type="submit" class="btn btn-primary auth-btn" :disabled="loading">
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>

      <div class="auth-footer">
        <span>Нет учётной записи?</span>
        <router-link to="/register">Зарегистрироваться</router-link>
      </div>

      <div class="auth-hint">
        <p><strong>Тестовые учётные записи:</strong></p>
        <p>admin / admin123 (Администратор)</p>
        <p>kadry / kadry123 (Менеджер по кадрам)</p>
        <p>user / user123 (Сотрудник)</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api.js'

export default {
  data() {
    return { username: '', password: '', error: '', loading: false }
  },
  methods: {
    async login() {
      this.error = ''
      this.loading = true
      try {
        const { data } = await api.post('/auth/login', {
          username: this.username,
          password: this.password
        })
        localStorage.setItem('token', data.token)
        localStorage.setItem('user', JSON.stringify(data.user))
        this.$router.push('/dashboard')
        setTimeout(() => location.reload(), 100)
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка авторизации'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0d1117 0%, #0f1117 50%, #0d1117 100%);
  padding: 20px;
}

.auth-card {
  background: #161b22;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  border: 1px solid #21262d;
}

.auth-header {
  text-align: center;
  margin-bottom: 28px;
}

.auth-logo {
  font-size: 40px;
  color: #3fb950;
  background: #12261e;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  margin: 0 auto 16px;
}

.auth-header h1 {
  font-size: 22px;
  font-weight: 700;
  color: #e6edf3;
  margin-bottom: 4px;
}

.auth-header p {
  font-size: 13px;
  color: #7d8590;
}

.auth-btn {
  width: 100%;
  padding: 12px;
  font-size: 15px;
  margin-top: 8px;
}

.auth-error {
  color: #f85149;
  font-size: 13px;
  margin-bottom: 8px;
  text-align: center;
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 13px;
  color: #7d8590;
}

.auth-footer a {
  color: #58a6ff;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
}

.auth-hint {
  margin-top: 20px;
  padding: 12px;
  background: #1c2128;
  border-radius: 8px;
  font-size: 12px;
  color: #7d8590;
  text-align: center;
}

.auth-hint p {
  margin-bottom: 2px;
}
</style>
