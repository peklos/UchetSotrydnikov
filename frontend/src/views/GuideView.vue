<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Памятка пользователя</h1>
      <p class="page-subtitle">Руководство по работе с системой «Учёт сотрудников»</p>
    </div>

    <div class="guide-sections">
      <div class="card guide-section" v-for="(section, i) in sections" :key="i">
        <div class="guide-header" @click="section.open = !section.open">
          <h3>{{ section.title }}</h3>
          <span class="guide-toggle">{{ section.open ? '−' : '+' }}</span>
        </div>
        <div v-if="section.open" class="guide-body" v-html="section.content"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sections: [
        {
          title: '1. Начало работы',
          open: true,
          content: `
            <p>Для начала работы с системой необходимо авторизоваться. Введите логин и пароль на странице входа и нажмите кнопку «Войти».</p>
            <p>Если у вас нет учётной записи — нажмите «Зарегистрироваться» и заполните форму регистрации (ФИО, логин, пароль).</p>
            <p><strong>Тестовые учётные записи:</strong></p>
            <ul>
              <li><strong>admin / admin123</strong> — Администратор (полный доступ)</li>
              <li><strong>kadry / kadry123</strong> — Менеджер по кадрам</li>
              <li><strong>user / user123</strong> — Обычный сотрудник</li>
            </ul>
          `
        },
        {
          title: '2. Главная панель (Dashboard)',
          open: false,
          content: `
            <p>На главной панели отображается сводная информация о кадровом составе филармонии:</p>
            <ul>
              <li>Общее количество сотрудников</li>
              <li>Количество подразделений и должностей</li>
              <li>Средняя заработная плата</li>
              <li>Распределение сотрудников по статусам</li>
              <li>Диаграмма по подразделениям</li>
              <li>Последние кадровые события</li>
            </ul>
          `
        },
        {
          title: '3. Работа с сотрудниками',
          open: false,
          content: `
            <p>Раздел «Сотрудники» позволяет управлять кадровым составом:</p>
            <ul>
              <li><strong>Просмотр списка</strong> — таблица со всеми сотрудниками с возможностью поиска и фильтрации по подразделению, статусу</li>
              <li><strong>Добавление</strong> — нажмите кнопку «+ Добавить сотрудника», заполните форму (ФИО, подразделение, должность, дата приёма, оклад, контактные данные, паспортные данные)</li>
              <li><strong>Редактирование</strong> — нажмите кнопку «Изм.» в строке сотрудника</li>
              <li><strong>Удаление</strong> — нажмите кнопку «Уд.» в строке сотрудника</li>
              <li><strong>Карточка сотрудника</strong> — нажмите на строку для перехода к подробной информации</li>
            </ul>
            <p>В карточке сотрудника доступны вкладки:</p>
            <ul>
              <li><strong>Личные данные</strong> — паспорт, ИНН, СНИЛС, адрес</li>
              <li><strong>Контакты</strong> — телефоны, email, Telegram</li>
              <li><strong>Образование</strong> — учебные заведения, степени, дипломы</li>
              <li><strong>Кадровые события</strong> — история приёмов, переводов, отпусков</li>
            </ul>
          `
        },
        {
          title: '4. Подразделения',
          open: false,
          content: `
            <p>Раздел «Подразделения» отражает организационную структуру филармонии.</p>
            <ul>
              <li>Карточки подразделений с указанием руководителя, телефона и количества сотрудников</li>
              <li>При нажатии на карточку — список сотрудников подразделения</li>
              <li>Возможность добавления, редактирования и удаления подразделений</li>
            </ul>
          `
        },
        {
          title: '5. Должности',
          open: false,
          content: `
            <p>Раздел «Должности» содержит штатное расписание:</p>
            <ul>
              <li>Таблица должностей с указанием подразделения и диапазона окладов</li>
              <li>Фильтрация по подразделению</li>
              <li>Добавление, редактирование и удаление должностей</li>
            </ul>
          `
        },
        {
          title: '6. Кадровые события',
          open: false,
          content: `
            <p>Раздел «Кадровые события» — журнал всех кадровых операций:</p>
            <ul>
              <li><strong>Типы событий:</strong> приём, увольнение, перевод, отпуск, больничный, командировка, повышение, выговор, премия</li>
              <li>Фильтрация по типу события</li>
              <li>Создание нового события с привязкой к сотруднику, указанием даты и номера документа</li>
              <li>При создании событий «отпуск», «больничный», «командировка» автоматически обновляется статус сотрудника</li>
            </ul>
          `
        },
        {
          title: '7. Отчёты',
          open: false,
          content: `
            <p>Раздел «Отчёты» предоставляет аналитику:</p>
            <ul>
              <li><strong>Обзор</strong> — статистика по подразделениям, статусам, типам занятости и полу</li>
              <li><strong>Штатное расписание</strong> — полная таблица должностей с указанием занятых позиций и сотрудников</li>
              <li><strong>График отпусков</strong> — все зарегистрированные отпуска сотрудников</li>
            </ul>
          `
        },
        {
          title: '8. Админ-панель',
          open: false,
          content: `
            <p>Раздел доступен только для пользователей с ролью «Администратор».</p>
            <ul>
              <li>Управление пользователями системы (создание, блокировка, удаление)</li>
              <li>Изменение ролей пользователей</li>
              <li>Сброс паролей</li>
              <li>Статистика по системе</li>
            </ul>
            <p><strong>Роли пользователей:</strong></p>
            <ul>
              <li><strong>Администратор</strong> — полный доступ ко всем разделам</li>
              <li><strong>Менеджер по кадрам</strong> — управление сотрудниками и событиями</li>
              <li><strong>Руководитель подразделения</strong> — просмотр данных подразделения</li>
              <li><strong>Сотрудник</strong> — просмотр собственного профиля</li>
            </ul>
          `
        },
        {
          title: '9. О системе',
          open: false,
          content: `
            <p><strong>Информационная система «Учёт сотрудников»</strong></p>
            <p>Разработана для ГАУК «Брянская областная филармония» с целью автоматизации кадрового учёта и управления персоналом.</p>
            <p><strong>Технологический стек:</strong></p>
            <ul>
              <li>Frontend: Vue.js 3, Vue Router, Axios</li>
              <li>Backend: Python, FastAPI</li>
              <li>База данных: SQLite</li>
            </ul>
            <p><strong>Основные возможности:</strong></p>
            <ul>
              <li>Авторизация и разграничение прав доступа</li>
              <li>Ведение базы данных сотрудников</li>
              <li>Формирование штатного расписания</li>
              <li>Учёт отпусков, больничных, командировок</li>
              <li>Поиск и фильтрация сотрудников</li>
              <li>Формирование отчётной документации</li>
            </ul>
          `
        }
      ]
    }
  }
}
</script>

<style scoped>
.guide-sections {
  max-width: 800px;
}

.guide-section {
  padding: 0;
  overflow: hidden;
}

.guide-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  transition: background 0.15s;
}

.guide-header {
  -webkit-user-select: none;
  user-select: none;
}

.guide-header:hover {
  background: #1c2128;
}

.guide-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: #e6edf3;
}

.guide-toggle {
  font-size: 20px;
  color: #58a6ff;
  font-weight: 600;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: #1c2a3a;
}

.guide-body {
  padding: 0 20px 20px;
  font-size: 14px;
  line-height: 1.7;
  color: #8b949e;
}

.guide-body p {
  margin-bottom: 10px;
}

.guide-body ul {
  margin-left: 20px;
  margin-bottom: 10px;
}

.guide-body li {
  margin-bottom: 4px;
}

.guide-body strong {
  color: #e6edf3;
}
</style>
