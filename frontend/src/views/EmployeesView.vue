<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Сотрудники</h1>
      <p class="page-subtitle">Управление кадровым составом филармонии</p>
    </div>

    <div class="toolbar">
      <div class="toolbar-left">
        <input v-model="search" @input="loadEmployees" type="text" class="search-input" placeholder="Поиск по ФИО, телефону, email..." />
        <select v-model="filterDept" @change="loadEmployees" class="filter-select">
          <option value="">Все подразделения</option>
          <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
        </select>
        <select v-model="filterStatus" @change="loadEmployees" class="filter-select">
          <option value="">Все статусы</option>
          <option value="работает">Работает</option>
          <option value="в отпуске">В отпуске</option>
          <option value="больничный">Больничный</option>
          <option value="уволен">Уволен</option>
          <option value="командировка">Командировка</option>
        </select>
      </div>
      <button v-if="canEdit" class="btn btn-primary" @click="openAdd">+ Добавить сотрудника</button>
    </div>

    <div class="card" style="padding: 0; overflow: hidden;">
      <table class="data-table">
        <thead>
          <tr>
            <th>ФИО</th>
            <th>Подразделение</th>
            <th>Должность</th>
            <th>Телефон</th>
            <th>Статус</th>
            <th>Дата приёма</th>
            <th v-if="canEdit">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="emp in employees" :key="emp.id" @click="$router.push('/employees/' + emp.id)">
            <td style="font-weight: 600;">{{ emp.last_name }} {{ emp.first_name }} {{ emp.middle_name || '' }}</td>
            <td>{{ emp.department_name || '—' }}</td>
            <td>{{ emp.position_name || '—' }}</td>
            <td>{{ emp.phone || '—' }}</td>
            <td><span :class="'badge badge-' + statusColor(emp.status)">{{ emp.status }}</span></td>
            <td>{{ formatDate(emp.hire_date) }}</td>
            <td v-if="canEdit" @click.stop>
              <button class="btn btn-secondary btn-sm" @click="openEdit(emp)">Изм.</button>
              <button class="btn btn-danger btn-sm" style="margin-left:4px" @click="deleteEmployee(emp.id)">Уд.</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="!employees.length" class="empty-state">
        <p class="empty-state-text">Сотрудники не найдены</p>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h2 class="modal-title">{{ editing ? 'Редактирование сотрудника' : 'Добавление сотрудника' }}</h2>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Фамилия *</label>
            <input v-model="form.last_name" class="form-input" required />
          </div>
          <div class="form-group">
            <label class="form-label">Имя *</label>
            <input v-model="form.first_name" class="form-input" required />
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Отчество</label>
            <input v-model="form.middle_name" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Дата рождения</label>
            <input v-model="form.birth_date" type="date" class="form-input" />
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Пол</label>
            <select v-model="form.gender" class="form-input">
              <option value="">—</option>
              <option value="М">Мужской</option>
              <option value="Ж">Женский</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Тип занятости</label>
            <select v-model="form.employment_type" class="form-input">
              <option value="штатный">Штатный</option>
              <option value="совместитель">Совместитель</option>
              <option value="срочный договор">Срочный договор</option>
              <option value="ГПД">ГПД</option>
            </select>
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Подразделение</label>
            <select v-model="form.department_id" class="form-input">
              <option :value="null">—</option>
              <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Должность</label>
            <select v-model="form.position_id" class="form-input">
              <option :value="null">—</option>
              <option v-for="p in positions" :key="p.id" :value="p.id">{{ p.name }}</option>
            </select>
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Дата приёма *</label>
            <input v-model="form.hire_date" type="date" class="form-input" required />
          </div>
          <div class="form-group">
            <label class="form-label">Оклад</label>
            <input v-model.number="form.salary" type="number" class="form-input" />
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Телефон</label>
            <input v-model="form.phone" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-input" />
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">ИНН</label>
            <input v-model="form.inn" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">СНИЛС</label>
            <input v-model="form.snils" class="form-input" />
          </div>
        </div>

        <div class="grid-2">
          <div class="form-group">
            <label class="form-label">Серия паспорта</label>
            <input v-model="form.passport_series" class="form-input" />
          </div>
          <div class="form-group">
            <label class="form-label">Номер паспорта</label>
            <input v-model="form.passport_number" class="form-input" />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Адрес</label>
          <input v-model="form.address" class="form-input" />
        </div>

        <div class="form-group" v-if="editing">
          <label class="form-label">Статус</label>
          <select v-model="form.status" class="form-input">
            <option value="работает">Работает</option>
            <option value="в отпуске">В отпуске</option>
            <option value="больничный">Больничный</option>
            <option value="уволен">Уволен</option>
            <option value="командировка">Командировка</option>
          </select>
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

const emptyForm = () => ({
  last_name: '', first_name: '', middle_name: '', birth_date: '', gender: '',
  inn: '', snils: '', passport_series: '', passport_number: '', address: '',
  phone: '', email: '', department_id: null, position_id: null,
  hire_date: new Date().toISOString().slice(0, 10), salary: null,
  employment_type: 'штатный', status: 'работает', photo_url: ''
})

export default {
  data() {
    return {
      employees: [],
      departments: [],
      positions: [],
      search: '',
      filterDept: '',
      filterStatus: '',
      showModal: false,
      editing: null,
      form: emptyForm()
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
  async mounted() {
    const [d, p] = await Promise.all([
      api.get('/departments'),
      api.get('/positions')
    ])
    this.departments = d.data
    this.positions = p.data
    this.loadEmployees()
  },
  methods: {
    async loadEmployees() {
      const params = {}
      if (this.search) params.search = this.search
      if (this.filterDept) params.department_id = this.filterDept
      if (this.filterStatus) params.status = this.filterStatus
      const { data } = await api.get('/employees', { params })
      this.employees = data
    },
    openAdd() {
      this.editing = null
      this.form = emptyForm()
      this.showModal = true
    },
    openEdit(emp) {
      this.editing = emp.id
      this.form = { ...emp }
      this.showModal = true
    },
    async save() {
      try {
        if (this.editing) {
          await api.put(`/employees/${this.editing}`, this.form)
        } else {
          await api.post('/employees', this.form)
        }
        this.showModal = false
        this.loadEmployees()
      } catch (err) {
        alert(err.response?.data?.detail || 'Ошибка сохранения')
      }
    },
    async deleteEmployee(id) {
      if (!confirm('Удалить сотрудника?')) return
      await api.delete(`/employees/${id}`)
      this.loadEmployees()
    },
    formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('ru-RU')
    },
    statusColor(status) {
      const map = { 'работает': 'green', 'уволен': 'red', 'в отпуске': 'blue', 'больничный': 'orange', 'командировка': 'purple' }
      return map[status] || 'gray'
    }
  }
}
</script>
