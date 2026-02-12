<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Отчёты</h1>
      <p class="page-subtitle">Кадровая аналитика и отчётность</p>
    </div>

    <div class="tabs">
      <button :class="['tab', { active: activeTab === 'overview' }]" @click="activeTab = 'overview'">Обзор</button>
      <button :class="['tab', { active: activeTab === 'staffing' }]" @click="activeTab = 'staffing'">Штатное расписание</button>
      <button :class="['tab', { active: activeTab === 'vacations' }]" @click="activeTab = 'vacations'">График отпусков</button>
    </div>

    <!-- Overview tab -->
    <div v-if="activeTab === 'overview'">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{ stats.total_employees }}</div>
          <div class="stat-label">Всего сотрудников</div>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color: #c62828;">{{ stats.fired_employees }}</div>
          <div class="stat-label">Уволено</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ formatSalary(stats.average_salary) }}</div>
          <div class="stat-label">Средняя зарплата</div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
        <div class="card">
          <h3 style="margin-bottom: 16px; font-size: 16px; font-weight: 600;">По подразделениям</h3>
          <table class="data-table">
            <thead><tr><th>Подразделение</th><th>Сотрудников</th><th>Ср. оклад</th></tr></thead>
            <tbody>
              <tr v-for="d in byDepartment" :key="d.name">
                <td>{{ d.name }}</td>
                <td><span class="badge badge-green">{{ d.employee_count }}</span></td>
                <td>{{ formatSalary(d.avg_salary) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="card">
          <h3 style="margin-bottom: 16px; font-size: 16px; font-weight: 600;">По статусу</h3>
          <div v-for="s in byStatus" :key="s.status" class="report-bar">
            <div class="report-bar-header">
              <span :class="'badge badge-' + statusColor(s.status)">{{ s.status }}</span>
              <span style="font-weight: 600;">{{ s.count }}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: percent(s.count, totalEmployees) + '%', background: statusBg(s.status) }"></div>
            </div>
          </div>

          <h3 style="margin: 24px 0 16px; font-size: 16px; font-weight: 600;">По типу занятости</h3>
          <div v-for="t in byType" :key="t.employment_type" class="report-bar">
            <div class="report-bar-header">
              <span>{{ t.employment_type }}</span>
              <span style="font-weight: 600;">{{ t.count }}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: percent(t.count, totalActive) + '%' }"></div>
            </div>
          </div>

          <h3 style="margin: 24px 0 16px; font-size: 16px; font-weight: 600;">По полу</h3>
          <div v-for="g in byGender" :key="g.gender" class="report-bar">
            <div class="report-bar-header">
              <span>{{ g.gender === 'М' ? 'Мужской' : 'Женский' }}</span>
              <span style="font-weight: 600;">{{ g.count }}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: percent(g.count, totalActive) + '%', background: g.gender === 'М' ? '#1565c0' : '#e91e63' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Staffing tab -->
    <div v-if="activeTab === 'staffing'" class="card" style="padding: 0; overflow: hidden;">
      <table class="data-table">
        <thead>
          <tr>
            <th>Подразделение</th>
            <th>Должность</th>
            <th>Мин. оклад</th>
            <th>Макс. оклад</th>
            <th>Занято</th>
            <th>Сотрудники</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, i) in staffing" :key="i">
            <td>{{ row.department_name || '—' }}</td>
            <td style="font-weight: 500;">{{ row.position_name }}</td>
            <td>{{ row.salary_min ? row.salary_min.toLocaleString('ru-RU') : '—' }}</td>
            <td>{{ row.salary_max ? row.salary_max.toLocaleString('ru-RU') : '—' }}</td>
            <td><span class="badge badge-green">{{ row.filled }}</span></td>
            <td style="max-width: 250px;">{{ row.employees || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Vacations tab -->
    <div v-if="activeTab === 'vacations'" class="card" style="padding: 0; overflow: hidden;">
      <table class="data-table">
        <thead>
          <tr>
            <th>Сотрудник</th>
            <th>Подразделение</th>
            <th>Должность</th>
            <th>Начало</th>
            <th>Окончание</th>
            <th>Описание</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(v, i) in vacations" :key="i">
            <td style="font-weight: 500;">{{ v.employee_name }}</td>
            <td>{{ v.department_name || '—' }}</td>
            <td>{{ v.position_name || '—' }}</td>
            <td>{{ formatDate(v.event_date) }}</td>
            <td>{{ v.end_date ? formatDate(v.end_date) : '—' }}</td>
            <td>{{ v.description || '—' }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="!vacations.length" class="empty-state"><p class="empty-state-text">Нет данных об отпусках</p></div>
    </div>
  </div>
</template>

<script>
import api from '../api.js'

export default {
  data() {
    return {
      activeTab: 'overview',
      stats: {},
      byDepartment: [],
      byStatus: [],
      byType: [],
      byGender: [],
      staffing: [],
      vacations: []
    }
  },
  computed: {
    totalEmployees() {
      return this.byStatus.reduce((s, r) => s + r.count, 0) || 1
    },
    totalActive() {
      return this.byType.reduce((s, r) => s + r.count, 0) || 1
    }
  },
  async mounted() {
    const [s, d, st, t, g, sf, v] = await Promise.all([
      api.get('/reports/stats'),
      api.get('/reports/by-department'),
      api.get('/reports/by-status'),
      api.get('/reports/by-employment-type'),
      api.get('/reports/by-gender'),
      api.get('/reports/staffing'),
      api.get('/reports/vacation-schedule')
    ])
    this.stats = s.data
    this.byDepartment = d.data
    this.byStatus = st.data
    this.byType = t.data
    this.byGender = g.data
    this.staffing = sf.data
    this.vacations = v.data
  },
  methods: {
    formatSalary(v) { return v ? Math.round(v).toLocaleString('ru-RU') : '0' },
    formatDate(d) { return d ? new Date(d).toLocaleDateString('ru-RU') : '' },
    percent(v, total) { return Math.round((v / total) * 100) },
    statusColor(s) { return { 'работает': 'green', 'уволен': 'red', 'в отпуске': 'blue', 'больничный': 'orange', 'командировка': 'purple' }[s] || 'gray' },
    statusBg(s) { return { 'работает': '#2e7d32', 'уволен': '#c62828', 'в отпуске': '#1565c0', 'больничный': '#e65100', 'командировка': '#6a1b9a' }[s] || '#999' }
  }
}
</script>

<style scoped>
.report-bar {
  margin-bottom: 14px;
}

.report-bar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  font-size: 13px;
}

.progress-bar {
  height: 6px;
  background: #f0f2f5;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #2e7d32;
  border-radius: 3px;
  transition: width 0.5s ease;
}
</style>
