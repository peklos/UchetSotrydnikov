<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Подразделения</h1>
      <p class="page-subtitle">Структура филармонии</p>
    </div>

    <div class="toolbar">
      <div></div>
      <button v-if="canEdit" class="btn btn-primary" @click="openAdd">+ Добавить подразделение</button>
    </div>

    <div class="dept-grid">
      <div v-for="dept in departments" :key="dept.id" class="card dept-card" @click="selectDept(dept)">
        <div class="dept-card-header">
          <h3>{{ dept.name }}</h3>
          <div v-if="canEdit" class="dept-actions" @click.stop>
            <button class="btn btn-secondary btn-sm" @click="openEdit(dept)">Изм.</button>
            <button class="btn btn-danger btn-sm" @click="deleteDept(dept.id)">Уд.</button>
          </div>
        </div>
        <p class="dept-desc">{{ dept.description || '' }}</p>
        <div class="dept-meta">
          <span v-if="dept.head_name">Руководитель: {{ dept.head_name }}</span>
          <span v-if="dept.phone">{{ dept.phone }}</span>
        </div>
        <div class="dept-count">
          <span class="badge badge-green">{{ dept.employee_count }} сотр.</span>
        </div>
      </div>
    </div>

    <!-- Department detail -->
    <div v-if="selected" class="card" style="margin-top: 16px;">
      <h3 style="margin-bottom: 12px; font-size: 16px; font-weight: 600; color: #e6edf3;">Сотрудники: {{ selected.name }}</h3>
      <table class="data-table" v-if="selectedEmployees.length">
        <thead>
          <tr><th>ФИО</th><th>Должность</th><th>Статус</th></tr>
        </thead>
        <tbody>
          <tr v-for="e in selectedEmployees" :key="e.id" @click="$router.push('/employees/' + e.id)">
            <td style="font-weight:500;">{{ e.last_name }} {{ e.first_name }} {{ e.middle_name || '' }}</td>
            <td>{{ e.position_name || '—' }}</td>
            <td><span :class="'badge badge-' + statusColor(e.status)">{{ e.status }}</span></td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state"><p class="empty-state-text">Нет сотрудников</p></div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal" style="max-width: 480px;">
        <h2 class="modal-title">{{ editing ? 'Редактирование' : 'Новое подразделение' }}</h2>
        <div class="form-group">
          <label class="form-label">Название *</label>
          <input v-model="form.name" class="form-input" required />
        </div>
        <div class="form-group">
          <label class="form-label">Описание</label>
          <textarea v-model="form.description" class="form-input"></textarea>
        </div>
        <div class="form-group">
          <label class="form-label">Руководитель</label>
          <input v-model="form.head_name" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Телефон</label>
          <input v-model="form.phone" class="form-input" />
        </div>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="showModal = false">Отмена</button>
          <button class="btn btn-primary" @click="save">{{ editing ? 'Сохранить' : 'Добавить' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api.js'

export default {
  data() {
    return {
      departments: [],
      selected: null,
      selectedEmployees: [],
      showModal: false,
      editing: null,
      form: { name: '', description: '', head_name: '', phone: '' }
    }
  },
  computed: {
    canEdit() {
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        return user.role_id === 1 || user.role_id === 2
      } catch { return false }
    }
  },
  async mounted() { await this.load() },
  methods: {
    async load() {
      const { data } = await api.get('/departments')
      this.departments = data
    },
    async selectDept(dept) {
      this.selected = dept
      const { data } = await api.get(`/departments/${dept.id}`)
      this.selectedEmployees = data.employees || []
    },
    openAdd() {
      this.editing = null
      this.form = { name: '', description: '', head_name: '', phone: '' }
      this.showModal = true
    },
    openEdit(dept) {
      this.editing = dept.id
      this.form = { name: dept.name, description: dept.description || '', head_name: dept.head_name || '', phone: dept.phone || '' }
      this.showModal = true
    },
    async save() {
      try {
        if (this.editing) {
          await api.put(`/departments/${this.editing}`, this.form)
        } else {
          await api.post('/departments', this.form)
        }
        this.showModal = false
        this.load()
      } catch (err) {
        alert(err.response?.data?.detail || 'Ошибка')
      }
    },
    async deleteDept(id) {
      if (!confirm('Удалить подразделение?')) return
      await api.delete(`/departments/${id}`)
      this.selected = null
      this.load()
    },
    statusColor(s) {
      return { 'работает': 'green', 'уволен': 'red', 'в отпуске': 'blue', 'больничный': 'orange', 'командировка': 'purple' }[s] || 'gray'
    }
  }
}
</script>

<style scoped>
.dept-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.dept-card {
  cursor: pointer;
  transition: box-shadow 0.2s, border-color 0.2s;
}

.dept-card:hover {
  border-color: #58a6ff;
  box-shadow: 0 4px 12px rgba(88,166,255,0.08);
}

.dept-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.dept-card-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: #e6edf3;
}

.dept-actions {
  display: flex;
  gap: 4px;
}

.dept-desc {
  font-size: 13px;
  color: #7d8590;
  margin-bottom: 8px;
}

.dept-meta {
  font-size: 12px;
  color: #7d8590;
  margin-bottom: 8px;
}

.dept-meta span {
  display: block;
}

.dept-count {
  margin-top: 4px;
}
</style>
