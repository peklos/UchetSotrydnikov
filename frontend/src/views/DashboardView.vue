<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Главная панель</h1>
      <p class="page-subtitle">Обзор кадрового состава филармонии</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="color: #3fb950">&#9823;</div>
        <div class="stat-value">{{ stats.total_employees }}</div>
        <div class="stat-label">Сотрудников</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="color: #1565c0">&#9632;</div>
        <div class="stat-value">{{ stats.departments_count }}</div>
        <div class="stat-label">Подразделений</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="color: #e65100">&#9734;</div>
        <div class="stat-value">{{ stats.positions_count }}</div>
        <div class="stat-label">Должностей</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="color: #3fb950">&#8381;</div>
        <div class="stat-value">{{ formatSalary(stats.average_salary) }}</div>
        <div class="stat-label">Средняя зарплата</div>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value" style="color: #3fb950">{{ stats.total_employees - stats.on_vacation - stats.on_sick_leave - stats.on_business_trip }}</div>
        <div class="stat-label">На рабочем месте</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color: #1565c0">{{ stats.on_vacation }}</div>
        <div class="stat-label">В отпуске</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color: #e65100">{{ stats.on_sick_leave }}</div>
        <div class="stat-label">На больничном</div>
      </div>
      <div class="stat-card">
        <div class="stat-value" style="color: #6a1b9a">{{ stats.on_business_trip }}</div>
        <div class="stat-label">В командировке</div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
      <div class="card">
        <h3 style="margin-bottom: 16px; font-size: 16px; font-weight: 600; color: #e6edf3;">По подразделениям</h3>
        <div v-for="dept in byDepartment" :key="dept.name" class="dept-bar">
          <div class="dept-bar-header">
            <span>{{ dept.name }}</span>
            <span class="badge badge-green">{{ dept.employee_count }}</span>
          </div>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: deptPercent(dept.employee_count) + '%' }"></div>
          </div>
        </div>
        <div v-if="!byDepartment.length" class="empty-state">
          <p class="empty-state-text">Нет данных</p>
        </div>
      </div>

      <div class="card">
        <h3 style="margin-bottom: 16px; font-size: 16px; font-weight: 600; color: #e6edf3;">Последние события</h3>
        <div v-for="event in recentEvents" :key="event.id" class="event-item">
          <span :class="'badge badge-' + eventColor(event.event_type)">{{ event.event_type }}</span>
          <span class="event-name">{{ event.employee_name }}</span>
          <span class="event-date">{{ formatDate(event.event_date) }}</span>
        </div>
        <div v-if="!recentEvents.length" class="empty-state">
          <p class="empty-state-text">Нет событий</p>
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
      stats: {},
      byDepartment: [],
      recentEvents: []
    }
  },
  async mounted() {
    try {
      const [s, d, e] = await Promise.all([
        api.get('/reports/stats'),
        api.get('/reports/by-department'),
        api.get('/reports/recent-events')
      ])
      this.stats = s.data
      this.byDepartment = d.data
      this.recentEvents = e.data.slice(0, 10)
    } catch (err) {
      console.error(err)
    }
  },
  methods: {
    formatSalary(val) {
      if (!val) return '0'
      return Math.round(val).toLocaleString('ru-RU')
    },
    formatDate(d) {
      if (!d) return ''
      return new Date(d).toLocaleDateString('ru-RU')
    },
    deptPercent(count) {
      const max = Math.max(...this.byDepartment.map(d => d.employee_count), 1)
      return (count / max) * 100
    },
    eventColor(type) {
      const map = {
        'приём': 'green', 'увольнение': 'red', 'перевод': 'blue',
        'отпуск': 'orange', 'больничный': 'red', 'командировка': 'purple',
        'повышение': 'green', 'выговор': 'red', 'премия': 'green'
      }
      return map[type] || 'gray'
    }
  }
}
</script>

<style scoped>
.dept-bar {
  margin-bottom: 12px;
}

.dept-bar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  font-size: 13px;
}

.progress-bar {
  height: 6px;
  background: #21262d;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #238636;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.event-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #21262d;
  font-size: 13px;
}

.event-name {
  flex: 1;
  font-weight: 500;
}

.event-date {
  color: #7d8590;
  font-size: 12px;
}
</style>
