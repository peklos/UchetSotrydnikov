<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <div class="auth-logo">&#9835;</div>
        <h1>Регистрация</h1>
        <p>Создание учётной записи</p>
      </div>

      <form @submit.prevent="register" class="auth-form">
        <div class="form-group">
          <label class="form-label">ФИО</label>
          <input v-model="full_name" type="text" class="form-input" placeholder="Иванов Иван Иванович" required />
        </div>
        <div class="form-group">
          <label class="form-label">Логин</label>
          <input v-model="username" type="text" class="form-input" placeholder="Придумайте логин" required />
        </div>
        <div class="form-group">
          <label class="form-label">Пароль</label>
          <input v-model="password" type="password" class="form-input" placeholder="Придумайте пароль" required />
        </div>
        <div class="form-group">
          <label class="form-label">Подтверждение пароля</label>
          <input v-model="password2" type="password" class="form-input" placeholder="Повторите пароль" required />
        </div>
        <p v-if="error" class="auth-error">{{ error }}</p>
        <p v-if="success" class="auth-success">{{ success }}</p>
        <button type="submit" class="btn btn-primary auth-btn" :disabled="loading">
          {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
        </button>
      </form>

      <div class="auth-footer">
        <span>Уже есть учётная запись?</span>
        <router-link to="/login">Войти</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api.js'

export default {
  data() {
    return { username: '', password: '', password2: '', full_name: '', error: '', success: '', loading: false }
  },
  methods: {
    async register() {
      this.error = ''
      this.success = ''
      if (this.password !== this.password2) {
        this.error = 'Пароли не совпадают'
        return
      }
      if (!this.full_name.trim()) {
        this.error = 'Введите ФИО'
        return
      }
      this.loading = true
      try {
        await api.post('/auth/register', {
          username: this.username,
          password: this.password,
          full_name: this.full_name
        })
        this.success = 'Регистрация прошла успешно! Перенаправление...'
        setTimeout(() => this.$router.push('/login'), 1500)
      } catch (err) {
        this.error = err.response?.data?.detail || 'Ошибка регистрации'
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
  background: linear-gradient(135deg, #e8f5e9 0%, #f0f2f5 50%, #e8f5e9 100%);
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
}

.auth-header {
  text-align: center;
  margin-bottom: 28px;
}

.auth-logo {
  font-size: 40px;
  color: #2e7d32;
  background: #e8f5e9;
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
  color: #1a1a2e;
  margin-bottom: 4px;
}

.auth-header p {
  font-size: 13px;
  color: #7c8db0;
}

.auth-btn {
  width: 100%;
  padding: 12px;
  font-size: 15px;
  margin-top: 8px;
}

.auth-error {
  color: #e53e3e;
  font-size: 13px;
  margin-bottom: 8px;
  text-align: center;
}

.auth-success {
  color: #2e7d32;
  font-size: 13px;
  margin-bottom: 8px;
  text-align: center;
}

.auth-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 13px;
  color: #7c8db0;
}

.auth-footer a {
  color: #2e7d32;
  text-decoration: none;
  font-weight: 600;
  margin-left: 4px;
}
</style>
