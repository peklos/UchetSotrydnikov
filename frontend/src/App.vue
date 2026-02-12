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
          <span class="nav-icon">&#127968;</span>
          <span>Главная</span>
        </router-link>
        <router-link to="/employees" class="nav-item">
          <span class="nav-icon">&#9823;</span>
          <span>Сотрудники</span>
        </router-link>
        <router-link to="/departments" class="nav-item">
          <span class="nav-icon">&#127970;</span>
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
          <span class="nav-icon">&#128202;</span>
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
      window.location.href = '/login'
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
  background: #0f1117;
  color: #c9d1d9;
  min-height: 100vh;
}

.app {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: #161b22;
  border-right: 1px solid #21262d;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #21262d;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 28px;
  color: #58a6ff;
  background: #1c2a3a;
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
  color: #e6edf3;
  display: block;
}

.logo-subtitle {
  font-size: 12px;
  color: #7d8590;
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
  color: #8b949e;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  margin-bottom: 2px;
}

.nav-item:hover {
  background: #1c2433;
  color: #58a6ff;
}

.nav-item.router-link-active {
  background: #1c2a3a;
  color: #58a6ff;
  font-weight: 600;
}

.nav-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #21262d;
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
  background: #238636;
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
  color: #e6edf3;
  display: block;
}

.user-role {
  font-size: 11px;
  color: #7d8590;
  display: block;
}

.logout-btn {
  width: 100%;
  padding: 8px;
  border: 1px solid #30363d;
  border-radius: 6px;
  background: #161b22;
  color: #f85149;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #2d1215;
  border-color: #f85149;
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
  color: #e6edf3;
  margin-bottom: 4px;
}

.page-subtitle {
  font-size: 14px;
  color: #7d8590;
}

.card {
  background: #161b22;
  border-radius: 12px;
  border: 1px solid #21262d;
  padding: 20px;
  margin-bottom: 16px;
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
  background: #238636;
  color: white;
}

.btn-primary:hover {
  background: #2ea043;
}

.btn-secondary {
  background: #21262d;
  color: #c9d1d9;
  border: 1px solid #30363d;
}

.btn-secondary:hover {
  background: #30363d;
}

.btn-danger {
  background: #da3633;
  color: white;
}

.btn-danger:hover {
  background: #f85149;
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
  color: #8b949e;
  margin-bottom: 4px;
}

.form-input {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid #30363d;
  border-radius: 8px;
  font-size: 14px;
  color: #e6edf3;
  background: #0d1117;
  transition: border-color 0.2s;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #58a6ff;
  box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
  background: #0d1117;
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
  background: #1c2128;
  color: #8b949e;
  font-weight: 600;
  border-bottom: 2px solid #21262d;
  white-space: nowrap;
}

.data-table td {
  padding: 10px 12px;
  border-bottom: 1px solid #21262d;
  color: #c9d1d9;
}

.data-table tr:hover {
  background: #1c2128;
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
  background: #12261e;
  color: #3fb950;
}

.badge-red {
  background: #2d1215;
  color: #f85149;
}

.badge-blue {
  background: #121d2f;
  color: #58a6ff;
}

.badge-orange {
  background: #2a1e0f;
  color: #d29922;
}

.badge-purple {
  background: #211c33;
  color: #bc8cff;
}

.badge-gray {
  background: #21262d;
  color: #8b949e;
}

/* Stats cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: #161b22;
  border-radius: 12px;
  border: 1px solid #21262d;
  padding: 20px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #e6edf3;
}

.stat-label {
  font-size: 13px;
  color: #7d8590;
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
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #161b22;
  border-radius: 16px;
  border: 1px solid #30363d;
  padding: 24px;
  width: 90%;
  max-width: 600px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: #e6edf3;
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
  border: 1px solid #30363d;
  border-radius: 8px;
  font-size: 14px;
  background: #0d1117;
  color: #e6edf3;
  font-family: inherit;
}

.search-input:focus {
  outline: none;
  border-color: #58a6ff;
  box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
}

/* Filter select */
.filter-select {
  padding: 9px 12px;
  border: 1px solid #30363d;
  border-radius: 8px;
  font-size: 13px;
  background: #0d1117;
  color: #c9d1d9;
  font-family: inherit;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0;
  border-bottom: 2px solid #21262d;
  margin-bottom: 20px;
}

.tab {
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  color: #7d8590;
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
  color: #58a6ff;
}

.tab.active {
  color: #58a6ff;
  border-bottom-color: #58a6ff;
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
  color: #7d8590;
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
  background: #0d1117;
}

::-webkit-scrollbar-thumb {
  background: #30363d;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #484f58;
}
</style>
