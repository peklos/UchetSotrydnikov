<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Админ-панель</h1>
      <p class="page-subtitle">Управление пользователями системы</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ adminStats.users_count }}</div>
        <div class="stat-label">Пользователей</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color: #3fb950">{{ adminStats.active_users }}</div>
        <div class="stat-label">Активных</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ adminStats.employees_count }}</div>
        <div class="stat-label">Сотрудников в БД</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ adminStats.events_count }}</div>
        <div class="stat-label">Кадровых событий</div>
      </div>
    </div>

    <div class="card" style="padding: 0; overflow: hidden;">
      <div style="padding: 16px 20px; border-bottom: 1px solid #21262d;">
        <h3 style="font-size: 16px; font-weight: 600; color: #e6edf3;">Пользователи системы</h3>
      </div>
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Логин</th>
            <th>ФИО</th>
            <th>Роль</th>
            <th>Статус</th>
            <th>Дата создания</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.id }}</td>
            <td style="font-weight: 600;">{{ u.username }}</td>
            <td>{{ u.full_name }}</td>
            <td>
              <select :value="u.role_id" @change="updateRole(u.id, $event.target.value)" class="filter-select" style="padding: 4px 8px; font-size: 12px;">
                <option v-for="r in roles" :key="r.id" :value="r.id">{{ r.name }}</option>
              </select>
            </td>
            <td>
              <span :class="'badge ' + (u.is_active ? 'badge-green' : 'badge-red')">
                {{ u.is_active ? 'Активен' : 'Заблокирован' }}
              </span>
            </td>
            <td>{{ formatDate(u.created_at) }}</td>
            <td>
              <button class="btn btn-secondary btn-sm" @click="toggleActive(u)">
                {{ u.is_active ? 'Блок.' : 'Разблок.' }}
              </button>
              <button class="btn btn-secondary btn-sm" style="margin-left:4px" @click="resetPassword(u.id)">Сброс пароля</button>
              <button class="btn btn-danger btn-sm" style="margin-left:4px" @click="deleteUser(u.id)">Уд.</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import api from '../api.js'

export default {
  data() {
    return {
      users: [],
      roles: [],
      adminStats: {}
    }
  },
  async mounted() {
    await this.load()
  },
  methods: {
    async load() {
      const [u, r, s] = await Promise.all([
        api.get('/admin/users'),
        api.get('/admin/roles'),
        api.get('/admin/stats')
      ])
      this.users = u.data
      this.roles = r.data
      this.adminStats = s.data
    },
    async updateRole(userId, roleId) {
      await api.put(`/admin/users/${userId}`, { role_id: parseInt(roleId) })
      this.load()
    },
    async toggleActive(user) {
      await api.put(`/admin/users/${user.id}`, { is_active: user.is_active ? 0 : 1 })
      this.load()
    },
    async resetPassword(userId) {
      if (!confirm('Сбросить пароль на password123?')) return
      await api.post(`/admin/users/${userId}/reset-password`)
      alert('Пароль сброшен на password123')
    },
    async deleteUser(userId) {
      if (!confirm('Удалить пользователя?')) return
      await api.delete(`/admin/users/${userId}`)
      this.load()
    },
    formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('ru-RU')
    }
  }
}
</script>
