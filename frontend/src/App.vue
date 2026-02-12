<template>
  <div class="app">
    <nav class="sidebar" v-if="isAuthenticated">
      <div class="sidebar-header">
        <div class="logo">
          <span class="logo-icon">&#9835;</span>
          <div class="logo-text">
            <span class="logo-title">Филармония</span>
            <span class="logo-subtitle">Учёт сотрудников</span>
          </div>
        </div>
      </div>

      <div class="nav-links">
        <router-link to="/dashboard" class="nav-item">
          <span class="nav-icon">&#9633;</span>
          <span>Главная</span>
        </router-link>
        <router-link to="/employees" class="nav-item">
          <span class="nav-icon">&#9823;</span>
          <span>Сотрудники</span>
        </router-link>
        <router-link to="/departments" class="nav-item">
          <span class="nav-icon">&#9632;</span>
          <span>Подразделения</span>
        </router-link>
        <router-link to="/positions" class="nav-item">
          <span class="nav-icon">&#9734;</span>
          <span>Должности</span>
        </router-link>
        <router-link to="/events" class="nav-item">
          <span class="nav-icon">&#9998;</span>
          <span>Кадровые события</span>
        </router-link>
        <router-link to="/reports" class="nav-item">
          <span class="nav-icon">&#9776;</span>
          <span>Отчёты</span>
        </router-link>
        <router-link to="/guide" class="nav-item">
          <span class="nav-icon">&#9432;</span>
          <span>Памятка</span>
        </router-link>
        <router-link to="/admin" class="nav-item" v-if="isAdmin">
          <span class="nav-icon">&#9881;</span>
          <span>Админ-панель</span>
        </router-link>
      </div>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">{{ userInitials }}</div>
          <div class="user-details">
            <span class="user-name">{{ userName }}</span>
            <span class="user-role">{{ userRole }}</span>
          </div>
        </div>
        <button class="logout-btn" @click="logout">Выход</button>
      </div>
    </nav>

    <main :class="{ 'main-content': isAuthenticated, 'main-full': !isAuthenticated }">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token')
    },
    userName() {
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        return user.full_name || user.username || ''
      } catch { return '' }
    },
    userRole() {
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        return user.role_name || ''
      } catch { return '' }
    },
    userInitials() {
      const name = this.userName
      if (!name) return '?'
      return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
    },
    isAdmin() {
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        return user.role_id === 1
      } catch { return false }
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.$router.push('/login')
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #f0f2f5;
  color: #2c3e50;
  min-height: 100vh;
}

.app {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: #ffffff;
  border-right: 1px solid #e0e4e8;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  box-shadow: 2px 0 8px rgba(0,0,0,0.04);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e0e4e8;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 28px;
  color: #2e7d32;
  background: #e8f5e9;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.logo-title {
  font-weight: 700;
  font-size: 16px;
  color: #1a1a2e;
  display: block;
}

.logo-subtitle {
  font-size: 12px;
  color: #7c8db0;
  display: block;
}

.nav-links {
  flex: 1;
  padding: 12px 10px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 16px;
  border-radius: 8px;
  color: #4a5568;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  margin-bottom: 2px;
}

.nav-item:hover {
  background: #f0f7f0;
  color: #2e7d32;
}

.nav-item.router-link-active {
  background: #e8f5e9;
  color: #2e7d32;
  font-weight: 600;
}

.nav-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #e0e4e8;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: #2e7d32;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: #2c3e50;
  display: block;
}

.user-role {
  font-size: 11px;
  color: #7c8db0;
  display: block;
}

.logout-btn {
  width: 100%;
  padding: 8px;
  border: 1px solid #e0e4e8;
  border-radius: 6px;
  background: white;
  color: #e53e3e;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #fff5f5;
  border-color: #e53e3e;
}

/* Main content */
.main-content {
  flex: 1;
  margin-left: 260px;
  padding: 24px;
  min-height: 100vh;
}

.main-full {
  flex: 1;
  min-height: 100vh;
}

/* Common styles */
.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 14px;
  color: #7c8db0;
}

.card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e0e4e8;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-primary {
  background: #2e7d32;
  color: white;
}

.btn-primary:hover {
  background: #1b5e20;
}

.btn-secondary {
  background: #f0f2f5;
  color: #4a5568;
  border: 1px solid #e0e4e8;
}

.btn-secondary:hover {
  background: #e0e4e8;
}

.btn-danger {
  background: #e53e3e;
  color: white;
}

.btn-danger:hover {
  background: #c53030;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

/* Form styles */
.form-group {
  margin-bottom: 14px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #4a5568;
  margin-bottom: 4px;
}

.form-input {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  color: #2c3e50;
  background: #fafbfc;
  transition: border-color 0.2s;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #2e7d32;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
  background: white;
}

select.form-input {
  appearance: auto;
}

textarea.form-input {
  resize: vertical;
  min-height: 80px;
}

/* Table styles */
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.data-table th {
  text-align: left;
  padding: 10px 12px;
  background: #f7f8fa;
  color: #4a5568;
  font-weight: 600;
  border-bottom: 2px solid #e0e4e8;
  white-space: nowrap;
}

.data-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #f0f2f5;
  color: #2c3e50;
}

.data-table tr:hover {
  background: #f7faf7;
}

.data-table tr {
  cursor: pointer;
  transition: background 0.15s;
}

/* Badges */
.badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  display: inline-block;
}

.badge-green {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge-red {
  background: #ffebee;
  color: #c62828;
}

.badge-blue {
  background: #e3f2fd;
  color: #1565c0;
}

.badge-orange {
  background: #fff3e0;
  color: #e65100;
}

.badge-purple {
  background: #f3e5f5;
  color: #6a1b9a;
}

.badge-gray {
  background: #f0f2f5;
  color: #4a5568;
}

/* Stats cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #e0e4e8;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
}

.stat-label {
  font-size: 13px;
  color: #7c8db0;
  margin-top: 4px;
}

.stat-icon {
  font-size: 20px;
  margin-bottom: 8px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 24px;
  width: 90%;
  max-width: 600px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 20px;
}

.modal-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 20px;
}

/* Search bar */
.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 200px;
  padding: 9px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  font-family: inherit;
}

.search-input:focus {
  outline: none;
  border-color: #2e7d32;
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
}

/* Filter select */
.filter-select {
  padding: 9px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 13px;
  background: white;
  color: #4a5568;
  font-family: inherit;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 2px solid #e0e4e8;
  margin-bottom: 20px;
}

.tab {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  color: #7c8db0;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
  background: none;
  border-top: none;
  border-left: none;
  border-right: none;
  font-family: inherit;
}

.tab:hover {
  color: #2e7d32;
}

.tab.active {
  color: #2e7d32;
  border-bottom-color: #2e7d32;
  font-weight: 600;
}

/* Grid layouts */
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.grid-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 14px;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 60px;
  }
  .sidebar .logo-text,
  .sidebar .nav-item span:last-child,
  .sidebar .user-details,
  .sidebar .logout-btn {
    display: none;
  }
  .main-content {
    margin-left: 60px;
  }
  .grid-2, .grid-3 {
    grid-template-columns: 1fr;
  }
  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #7c8db0;
}

.empty-state-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.empty-state-text {
  font-size: 15px;
}

/* Toolbar */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.toolbar-left {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f0f2f5;
}

::-webkit-scrollbar-thumb {
  background: #c4c9d4;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a0a8b8;
}
</style>
