<template>
  <div v-if="employee">
    <div class="page-header" style="display: flex; justify-content: space-between; align-items: flex-start;">
      <div>
        <h1 class="page-title">{{ employee.full_name }}</h1>
        <p class="page-subtitle">{{ employee.position_name || 'Должность не указана' }} | {{ employee.department_name || 'Подразделение не указано' }}</p>
      </div>
      <div>
        <span :class="'badge badge-' + statusColor(employee.status)" style="font-size: 13px; padding: 6px 14px;">{{ employee.status }}</span>
        <button class="btn btn-secondary" style="margin-left: 8px;" @click="$router.push('/employees')">Назад</button>
      </div>
    </div>

    <div class="tabs">
      <button :class="['tab', { active: activeTab === 'info' }]" @click="activeTab = 'info'">Личные данные</button>
      <button :class="['tab', { active: activeTab === 'contacts' }]" @click="activeTab = 'contacts'">Контакты</button>
      <button :class="['tab', { active: activeTab === 'education' }]" @click="activeTab = 'education'">Образование</button>
      <button :class="['tab', { active: activeTab === 'events' }]" @click="activeTab = 'events'">Кадровые события</button>
    </div>

    <!-- Info tab -->
    <div v-if="activeTab === 'info'" class="card">
      <div class="grid-2">
        <div class="info-row"><span class="info-label">Фамилия</span><span class="info-value">{{ employee.last_name }}</span></div>
        <div class="info-row"><span class="info-label">Имя</span><span class="info-value">{{ employee.first_name }}</span></div>
        <div class="info-row"><span class="info-label">Отчество</span><span class="info-value">{{ employee.middle_name || '—' }}</span></div>
        <div class="info-row"><span class="info-label">Дата рождения</span><span class="info-value">{{ formatDate(employee.birth_date) || '—' }}</span></div>
        <div class="info-row"><span class="info-label">Пол</span><span class="info-value">{{ employee.gender === 'М' ? 'Мужской' : employee.gender === 'Ж' ? 'Женский' : '—' }}</span></div>
        <div class="info-row"><span class="info-label">Тип занятости</span><span class="info-value">{{ employee.employment_type || '—' }}</span></div>
        <div class="info-row"><span class="info-label">Дата приёма</span><span class="info-value">{{ formatDate(employee.hire_date) }}</span></div>
        <div class="info-row"><span class="info-label">Оклад</span><span class="info-value">{{ employee.salary ? employee.salary.toLocaleString('ru-RU') + ' руб.' : '—' }}</span></div>
        <div class="info-row"><span class="info-label">ИНН</span><span class="info-value">{{ employee.inn || '—' }}</span></div>
        <div class="info-row"><span class="info-label">СНИЛС</span><span class="info-value">{{ employee.snils || '—' }}</span></div>
        <div class="info-row"><span class="info-label">Паспорт</span><span class="info-value">{{ employee.passport_series && employee.passport_number ? employee.passport_series + ' ' + employee.passport_number : '—' }}</span></div>
        <div class="info-row"><span class="info-label">Адрес</span><span class="info-value">{{ employee.address || '—' }}</span></div>
        <div class="info-row"><span class="info-label">Телефон</span><span class="info-value">{{ employee.phone || '—' }}</span></div>
        <div class="info-row"><span class="info-label">Email</span><span class="info-value">{{ employee.email || '—' }}</span></div>
      </div>
    </div>

    <!-- Contacts tab -->
    <div v-if="activeTab === 'contacts'">
      <div class="card">
        <div class="toolbar">
          <h3 style="font-size: 16px; font-weight: 600;">Контактные данные</h3>
          <button class="btn btn-primary btn-sm" @click="showContactModal = true">+ Добавить</button>
        </div>
        <table class="data-table" v-if="employee.contacts && employee.contacts.length">
          <thead>
            <tr><th>Тип</th><th>Значение</th><th>Основной</th><th></th></tr>
          </thead>
          <tbody>
            <tr v-for="c in employee.contacts" :key="c.id">
              <td>{{ c.contact_type }}</td>
              <td>{{ c.contact_value }}</td>
              <td>{{ c.is_primary ? 'Да' : 'Нет' }}</td>
              <td><button class="btn btn-danger btn-sm" @click="deleteContact(c.id)">Уд.</button></td>
            </tr>
          </tbody>
        </table>
        <div v-else class="empty-state"><p class="empty-state-text">Контакты не добавлены</p></div>
      </div>

      <div v-if="showContactModal" class="modal-overlay" @click.self="showContactModal = false">
        <div class="modal" style="max-width: 400px;">
          <h2 class="modal-title">Добавить контакт</h2>
          <div class="form-group">
            <label class="form-label">Тип</label>
            <select v-model="contactForm.contact_type" class="form-input">
              <option value="телефон">Телефон</option>
              <option value="email">Email</option>
              <option value="telegram">Telegram</option>
              <option value="другое">Другое</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Значение</label>
            <input v-model="contactForm.contact_value" class="form-input" />
          </div>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="showContactModal = false">Отмена</button>
            <button class="btn btn-primary" @click="addContact">Добавить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Education tab -->
    <div v-if="activeTab === 'education'">
      <div class="card">
        <div class="toolbar">
          <h3 style="font-size: 16px; font-weight: 600;">Образование</h3>
          <button class="btn btn-primary btn-sm" @click="showEduModal = true">+ Добавить</button>
        </div>
        <table class="data-table" v-if="employee.education && employee.education.length">
          <thead>
            <tr><th>Учебное заведение</th><th>Специальность</th><th>Степень</th><th>Годы</th><th></th></tr>
          </thead>
          <tbody>
            <tr v-for="e in employee.education" :key="e.id">
              <td>{{ e.institution }}</td>
              <td>{{ e.speciality || '—' }}</td>
              <td>{{ e.degree || '—' }}</td>
              <td>{{ e.year_start }}–{{ e.year_end || '...' }}</td>
              <td><button class="btn btn-danger btn-sm" @click="deleteEdu(e.id)">Уд.</button></td>
            </tr>
          </tbody>
        </table>
        <div v-else class="empty-state"><p class="empty-state-text">Записи об образовании отсутствуют</p></div>
      </div>

      <div v-if="showEduModal" class="modal-overlay" @click.self="showEduModal = false">
        <div class="modal">
          <h2 class="modal-title">Добавить образование</h2>
          <div class="form-group">
            <label class="form-label">Учебное заведение *</label>
            <input v-model="eduForm.institution" class="form-input" />
          </div>
          <div class="grid-2">
            <div class="form-group">
              <label class="form-label">Специальность</label>
              <input v-model="eduForm.speciality" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Степень</label>
              <select v-model="eduForm.degree" class="form-input">
                <option value="">—</option>
                <option value="среднее">Среднее</option>
                <option value="среднее специальное">Среднее специальное</option>
                <option value="бакалавр">Бакалавр</option>
                <option value="магистр">Магистр</option>
                <option value="специалист">Специалист</option>
                <option value="аспирант">Аспирант</option>
                <option value="кандидат наук">Кандидат наук</option>
                <option value="доктор наук">Доктор наук</option>
              </select>
            </div>
          </div>
          <div class="grid-2">
            <div class="form-group">
              <label class="form-label">Год начала</label>
              <input v-model.number="eduForm.year_start" type="number" class="form-input" />
            </div>
            <div class="form-group">
              <label class="form-label">Год окончания</label>
              <input v-model.number="eduForm.year_end" type="number" class="form-input" />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Номер диплома</label>
            <input v-model="eduForm.diploma_number" class="form-input" />
          </div>
          <div class="modal-actions">
            <button class="btn btn-secondary" @click="showEduModal = false">Отмена</button>
            <button class="btn btn-primary" @click="addEdu">Добавить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Events tab -->
    <div v-if="activeTab === 'events'" class="card">
      <h3 style="margin-bottom: 16px; font-size: 16px; font-weight: 600;">История кадровых событий</h3>
      <table class="data-table" v-if="employee.events && employee.events.length">
        <thead>
          <tr><th>Дата</th><th>Тип</th><th>Описание</th><th>Документ</th></tr>
        </thead>
        <tbody>
          <tr v-for="ev in employee.events" :key="ev.id">
            <td>{{ formatDate(ev.event_date) }}</td>
            <td><span :class="'badge badge-' + eventColor(ev.event_type)">{{ ev.event_type }}</span></td>
            <td>{{ ev.description || '—' }}</td>
            <td>{{ ev.document_number || '—' }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state"><p class="empty-state-text">Кадровые события отсутствуют</p></div>
    </div>
  </div>
</template>

<script>
import api from '../api.js'

export default {
  data() {
    return {
      employee: null,
      activeTab: 'info',
      showContactModal: false,
      showEduModal: false,
      contactForm: { contact_type: 'телефон', contact_value: '', is_primary: 0 },
      eduForm: { institution: '', speciality: '', degree: '', year_start: null, year_end: null, diploma_number: '' }
    }
  },
  async mounted() {
    await this.load()
  },
  methods: {
    async load() {
      const { data } = await api.get(`/employees/${this.$route.params.id}`)
      this.employee = data
    },
    formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('ru-RU')
    },
    statusColor(s) {
      return { 'работает': 'green', 'уволен': 'red', 'в отпуске': 'blue', 'больничный': 'orange', 'командировка': 'purple' }[s] || 'gray'
    },
    eventColor(t) {
      return { 'приём': 'green', 'увольнение': 'red', 'перевод': 'blue', 'отпуск': 'orange', 'больничный': 'red', 'командировка': 'purple', 'повышение': 'green', 'выговор': 'red', 'премия': 'green' }[t] || 'gray'
    },
    async addContact() {
      await api.post(`/employees/${this.employee.id}/contacts`, this.contactForm)
      this.showContactModal = false
      this.contactForm = { contact_type: 'телефон', contact_value: '', is_primary: 0 }
      this.load()
    },
    async deleteContact(id) {
      await api.delete(`/employees/${this.employee.id}/contacts/${id}`)
      this.load()
    },
    async addEdu() {
      await api.post(`/employees/${this.employee.id}/education`, this.eduForm)
      this.showEduModal = false
      this.eduForm = { institution: '', speciality: '', degree: '', year_start: null, year_end: null, diploma_number: '' }
      this.load()
    },
    async deleteEdu(id) {
      await api.delete(`/employees/${this.employee.id}/education/${id}`)
      this.load()
    }
  }
}
</script>

<style scoped>
.info-row {
  padding: 10px 0;
  border-bottom: 1px solid #f0f2f5;
}

.info-label {
  display: block;
  font-size: 12px;
  color: #7c8db0;
  margin-bottom: 2px;
}

.info-value {
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
}
</style>
