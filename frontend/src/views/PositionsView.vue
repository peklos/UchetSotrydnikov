<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Должности</h1>
      <p class="page-subtitle">Штатное расписание филармонии</p>
    </div>

    <div class="toolbar">
      <select v-model="filterDept" @change="load" class="filter-select">
        <option value="">Все подразделения</option>
        <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
      </select>
      <button class="btn btn-primary" @click="openAdd">+ Добавить должность</button>
    </div>

    <div class="card" style="padding: 0; overflow: hidden;">
      <table class="data-table">
        <thead>
          <tr>
            <th>Должность</th>
            <th>Подразделение</th>
            <th>Мин. оклад</th>
            <th>Макс. оклад</th>
            <th>Описание</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pos in positions" :key="pos.id">
            <td style="font-weight: 600;">{{ pos.name }}</td>
            <td>{{ pos.department_name || '—' }}</td>
            <td>{{ pos.salary_min ? pos.salary_min.toLocaleString('ru-RU') : '—' }}</td>
            <td>{{ pos.salary_max ? pos.salary_max.toLocaleString('ru-RU') : '—' }}</td>
            <td style="max-width: 200px; overflow: hidden; text-overflow: ellipsis;">{{ pos.description || '—' }}</td>
            <td>
              <button class="btn btn-secondary btn-sm" @click="openEdit(pos)">Изм.</button>
              <button class="btn btn-danger btn-sm" style="margin-left:4px" @click="deletePos(pos.id)">Уд.</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="!positions.length" class="empty-state"><p class="empty-state-text">Должности не найдены</p></div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal" style="max-width: 480px;">
        <h2 class="modal-title">{{ editing ? 'Редактирование' : 'Новая должность' }}</h2>
        <div class="form-group">
          <label class="form-label">Название *</label>
          <input v-model="form.name" class="form-input" required />
        </div>
        <div class="form-group">
          <label class="form-label">Подразделение</label>
          <select v-model="form.department_id" class="form-input">
            <option :value="null">—</option>
            <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
          </select>
        </div>
        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Мин. оклад</label>
            <input v-model.number="form.salary_min" type="number" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Макс. оклад</label>
            <input v-model.number="form.salary_max" type="number" class="form-input" />
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Описание</label>
          <textarea v-model="form.description" class="form-input"></textarea>
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
      positions: [],
      departments: [],
      filterDept: '',
      showModal: false,
      editing: null,
      form: { name: '', department_id: null, salary_min: null, salary_max: null, description: '' }
    }
  },
  async mounted() {
    const { data } = await api.get('/departments')
    this.departments = data
    this.load()
  },
  methods: {
    async load() {
      const params = {}
      if (this.filterDept) params.department_id = this.filterDept
      const { data } = await api.get('/positions', { params })
      this.positions = data
    },
    openAdd() {
      this.editing = null
      this.form = { name: '', department_id: null, salary_min: null, salary_max: null, description: '' }
      this.showModal = true
    },
    openEdit(pos) {
      this.editing = pos.id
      this.form = { name: pos.name, department_id: pos.department_id, salary_min: pos.salary_min, salary_max: pos.salary_max, description: pos.description || '' }
      this.showModal = true
    },
    async save() {
      try {
        if (this.editing) {
          await api.put(`/positions/${this.editing}`, this.form)
        } else {
          await api.post('/positions', this.form)
        }
        this.showModal = false
        this.load()
      } catch (err) {
        alert(err.response?.data?.detail || 'Ошибка')
      }
    },
    async deletePos(id) {
      if (!confirm('Удалить должность?')) return
      await api.delete(`/positions/${id}`)
      this.load()
    }
  }
}
</script>
