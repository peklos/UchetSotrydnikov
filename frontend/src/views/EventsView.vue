<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Кадровые события</h1>
      <p class="page-subtitle">Приказы, отпуска, больничные, командировки</p>
    </div>

    <div class="toolbar">
      <div class="toolbar-left">
        <select v-model="filterType" @change="load" class="filter-select">
          <option value="">Все типы</option>
          <option value="приём">Приём</option>
          <option value="увольнение">Увольнение</option>
          <option value="перевод">Перевод</option>
          <option value="отпуск">Отпуск</option>
          <option value="больничный">Больничный</option>
          <option value="командировка">Командировка</option>
          <option value="повышение">Повышение</option>
          <option value="выговор">Выговор</option>
          <option value="премия">Премия</option>
        </select>
      </div>
      <button class="btn btn-primary" @click="showModal = true">+ Создать событие</button>
    </div>

    <div class="card" style="padding: 0; overflow: hidden;">
      <table class="data-table">
        <thead>
          <tr>
            <th>Дата</th>
            <th>Тип</th>
            <th>Сотрудник</th>
            <th>Описание</th>
            <th>Документ</th>
            <th>Дата оконч.</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ev in events" :key="ev.id">
            <td>{{ formatDate(ev.event_date) }}</td>
            <td><span :class="'badge badge-' + eventColor(ev.event_type)">{{ ev.event_type }}</span></td>
            <td style="font-weight:500;">{{ ev.employee_name }}</td>
            <td style="max-width: 250px;">{{ ev.description || '—' }}</td>
            <td>{{ ev.document_number || '—' }}</td>
            <td>{{ ev.end_date ? formatDate(ev.end_date) : '—' }}</td>
            <td><button class="btn btn-danger btn-sm" @click="deleteEvent(ev.id)">Уд.</button></td>
          </tr>
        </tbody>
      </table>
      <div v-if="!events.length" class="empty-state"><p class="empty-state-text">События не найдены</p></div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal" style="max-width: 520px;">
        <h2 class="modal-title">Новое кадровое событие</h2>
        <div class="form-group">
          <label class="form-label">Сотрудник *</label>
          <select v-model="form.employee_id" class="form-input">
            <option :value="null">Выберите сотрудника</option>
            <option v-for="e in employees" :key="e.id" :value="e.id">{{ e.last_name }} {{ e.first_name }} {{ e.middle_name || '' }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label">Тип события *</label>
          <select v-model="form.event_type" class="form-input">
            <option value="приём">Приём</option>
            <option value="увольнение">Увольнение</option>
            <option value="перевод">Перевод</option>
            <option value="отпуск">Отпуск</option>
            <option value="больничный">Больничный</option>
            <option value="командировка">Командировка</option>
            <option value="повышение">Повышение</option>
            <option value="выговор">Выговор</option>
            <option value="премия">Премия</option>
          </select>
        </div>
        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Дата события *</label>
            <input v-model="form.event_date" type="date" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Дата окончания</label>
            <input v-model="form.end_date" type="date" class="form-input" />
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">Номер документа</label>
          <input v-model="form.document_number" class="form-input" />
        </div>
        <div class="form-group">
          <label class="form-label">Описание</label>
          <textarea v-model="form.description" class="form-input"></textarea>
        </div>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="showModal = false">Отмена</button>
          <button class="btn btn-primary" @click="save">Создать</button>
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
      events: [],
      employees: [],
      filterType: '',
      showModal: false,
      form: { employee_id: null, event_type: 'приём', event_date: new Date().toISOString().slice(0,10), end_date: '', description: '', document_number: '' }
    }
  },
  async mounted() {
    const { data } = await api.get('/employees')
    this.employees = data
    this.load()
  },
  methods: {
    async load() {
      const params = {}
      if (this.filterType) params.event_type = this.filterType
      const { data } = await api.get('/events', { params })
      this.events = data
    },
    async save() {
      if (!this.form.employee_id) { alert('Выберите сотрудника'); return }
      try {
        await api.post('/events', this.form)
        this.showModal = false
        this.form = { employee_id: null, event_type: 'приём', event_date: new Date().toISOString().slice(0,10), end_date: '', description: '', document_number: '' }
        this.load()
      } catch (err) {
        alert(err.response?.data?.detail || 'Ошибка')
      }
    },
    async deleteEvent(id) {
      if (!confirm('Удалить событие?')) return
      await api.delete(`/events/${id}`)
      this.load()
    },
    formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('ru-RU')
    },
    eventColor(t) {
      return { 'приём': 'green', 'увольнение': 'red', 'перевод': 'blue', 'отпуск': 'orange', 'больничный': 'red', 'командировка': 'purple', 'повышение': 'green', 'выговор': 'red', 'премия': 'green' }[t] || 'gray'
    }
  }
}
</script>
