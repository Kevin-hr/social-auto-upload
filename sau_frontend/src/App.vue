<template>
  <div id="app" :class="theme">
    <!-- 背景效果 -->
    <div class="grid-background"></div>
    <div class="glow-orb glow-orb-1"></div>
    <div class="glow-orb glow-orb-2"></div>

    <div class="app-container">
      <!-- 侧边栏 -->
      <aside class="sidebar" :class="{ collapsed: isCollapse }">
        <div class="sidebar-header">
          <div class="logo">
            <div class="logo-icon">
              <svg viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 2L4 8v16l12 6 12-6V8L16 2z" stroke="url(#logo-grad)" stroke-width="2" fill="none"/>
                <circle cx="16" cy="16" r="4" fill="url(#logo-grad)"/>
                <path d="M16 26V32M26 20l-6-4M6 20l6-4" stroke="url(#logo-grad)" stroke-width="2" stroke-linecap="round"/>
                <defs>
                  <linearGradient id="logo-grad" x1="4" y1="4" x2="28" y2="28">
                    <stop stop-color="#0071e3"/>
                    <stop offset="1" stop-color="#5e5ce6"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <span v-show="!isCollapse" class="logo-text">
              <span class="logo-title">指挥中心</span>
              <span class="logo-subtitle">Social Auto</span>
            </span>
          </div>
        </div>

        <nav class="sidebar-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: activeMenu === item.path }"
          >
            <component :is="item.icon" class="nav-icon" />
            <span v-show="!isCollapse" class="nav-text">{{ item.label }}</span>
            <span v-if="!isCollapse && item.badge" class="nav-badge">{{ item.badge }}</span>
          </router-link>
        </nav>

        <div class="sidebar-footer">
          <div class="system-status">
            <div class="status-indicator online"></div>
            <span v-show="!isCollapse" class="status-text">系统在线</span>
          </div>
          <div class="footer-actions">
            <button class="theme-toggle-btn" @click="toggleTheme" :title="theme === 'light' ? '切换到深色模式' : '切换到浅色模式'">
              <span v-if="theme === 'light'" class="theme-icon">🌙</span>
              <span v-else class="theme-icon">☀️</span>
            </button>
            <button class="collapse-btn" @click="toggleSidebar">
              <component :is="isCollapse ? 'Expand' : 'Fold'" />
            </button>
          </div>
        </div>
      </aside>

      <!-- 主内容区 -->
      <main class="main-content">
        <!-- 顶部栏 -->
        <header class="top-bar">
          <div class="breadcrumb">
            <span class="breadcrumb-item">{{ currentPageTitle }}</span>
          </div>
          <div class="top-bar-actions">
            <div class="time-display">
              <span class="time-value">{{ currentTime }}</span>
              <span class="time-label">服务器时间</span>
            </div>
            <button class="action-btn" title="刷新数据">
              <component :is="Refresh" />
            </button>
            <button class="action-btn" title="通知">
              <component :is="Bell" />
              <span class="notification-dot"></span>
            </button>
            <div class="user-profile">
              <div class="user-avatar">
                <span>OP</span>
              </div>
              <span class="user-name">管理员</span>
            </div>
          </div>
        </header>

        <!-- 页面内容 -->
        <div class="page-content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  HomeFilled, User, Picture, Upload, Monitor, DataAnalysis,
  Fold, Expand, Refresh, Bell
} from '@element-plus/icons-vue'

const route = useRoute()

// 菜单项配置
const menuItems = [
  { path: '/', label: '仪表盘', icon: HomeFilled },
  { path: '/account-management', label: '账号管理', icon: User, badge: 3 },
  { path: '/material-management', label: '素材库', icon: Picture },
  { path: '/publish-center', label: '发布中心', icon: Upload, badge: 5 },
  { path: '/website', label: '监控面板', icon: Monitor },
  { path: '/data', label: '数据分析', icon: DataAnalysis },
]

// 当前激活菜单
const activeMenu = computed(() => route.path)

// 当前页面标题
const currentPageTitle = computed(() => {
  const item = menuItems.find(m => m.path === route.path)
  return item?.label || '仪表盘'
})

// 侧边栏折叠状态
const isCollapse = ref(false)

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

// ===== 主题切换功能 =====
const theme = ref('light')

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  localStorage.setItem('theme', theme.value)
  document.documentElement.setAttribute('data-theme', theme.value)
}

// 当前时间
const currentTime = ref('')
let timeInterval = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

onMounted(() => {
  // 恢复主题设置
  const savedTheme = localStorage.getItem('theme') || 'light'
  theme.value = savedTheme
  document.documentElement.setAttribute('data-theme', savedTheme)

  updateTime()
  timeInterval = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timeInterval) clearInterval(timeInterval)
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

// ===== 侧边栏样式 =====
.sidebar {
  width: 260px;
  background: $bg-light;
  border-right: 1px solid $border-light;
  display: flex;
  flex-direction: column;
  transition: width $transition-normal ease, background 0.3s ease;
  position: relative;
  z-index: 10;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 1px;
    height: 100%;
    background: linear-gradient(180deg, transparent 0%, rgba(0, 113, 227, 0.2) 50%, transparent 100%);
    opacity: 0;
    transition: opacity $transition-normal;
  }

  &:hover::before {
    opacity: 1;
  }

  &.collapsed {
    width: 80px;

    .logo {
      padding: 0;
      justify-content: center;
    }

    .nav-item {
      justify-content: center;
      padding: $spacing-md;

      .nav-icon {
        margin-right: 0;
      }
    }
  }
}

#app.dark .sidebar {
  background: linear-gradient(180deg, rgba(17, 17, 24, 0.95) 0%, rgba(10, 10, 15, 0.98) 100%);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.sidebar-header {
  padding: $spacing-lg;
  border-bottom: 1px solid $border-light;
}

#app.dark .sidebar-header {
  border-bottom-color: rgba(255, 255, 255, 0.08);
}

.logo {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.logo-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;

  svg {
    width: 100%;
    height: 100%;
  }
}

.logo-text {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.logo-title {
  font-family: $font-display;
  font-size: 16px;
  font-weight: $font-weight-bold;
  color: $text-primary;
  letter-spacing: 0.05em;
}

.logo-subtitle {
  font-size: 10px;
  color: $text-tertiary;
  text-transform: uppercase;
  letter-spacing: 0.15em;
}

#app.dark .logo-subtitle {
  color: rgba(255, 255, 255, 0.4);
}

// ===== 导航菜单 =====
.sidebar-nav {
  flex: 1;
  padding: $spacing-md;
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: $spacing-md $spacing-lg;
  border-radius: $radius-md;
  color: $text-secondary;
  text-decoration: none;
  transition: all $transition-fast;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 0;
    background: $primary-gradient;
    border-radius: 0 3px 3px 0;
    transition: height $transition-fast;
  }

  &:hover {
    color: $text-primary;
    background: rgba(0, 0, 0, 0.03);

    &::before {
      height: 20px;
    }
  }

  &.active {
    color: $text-primary;
    background: linear-gradient(90deg, rgba(0, 113, 227, 0.08) 0%, transparent 100%);

    &::before {
      height: 24px;
    }

    .nav-icon {
      color: $primary-start;
    }
  }
}

#app.dark .nav-item {
  &:hover {
    background: rgba(255, 255, 255, 0.06);
  }

  &.active {
    background: linear-gradient(90deg, rgba(99, 102, 241, 0.15) 0%, transparent 100%);

    .nav-icon {
      color: $primary-start;
      filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.5));
    }
  }
}

.nav-icon {
  width: 20px;
  height: 20px;
  margin-right: $spacing-md;
  transition: all $transition-fast;
}

.nav-text {
  font-size: 14px;
  font-weight: $font-weight-medium;
  white-space: nowrap;
}

.nav-badge {
  margin-left: auto;
  padding: 2px 8px;
  background: linear-gradient(135deg, $primary-start, $primary-end);
  border-radius: $radius-full;
  font-size: 10px;
  font-weight: $font-weight-bold;
  color: white;
}

// ===== 侧边栏底部 =====
.sidebar-footer {
  padding: $spacing-md $spacing-lg;
  border-top: 1px solid $border-light;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

#app.dark .sidebar-footer {
  border-top-color: rgba(255, 255, 255, 0.08);
}

.system-status {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: $text-tertiary;

  &.online {
    background: $success-color;
    box-shadow: 0 0 8px rgba(52, 199, 89, 0.4);
    animation: pulse 2s ease-in-out infinite;
  }
}

.status-text {
  font-size: 12px;
  color: $text-tertiary;
}

#app.dark .status-text {
  color: rgba(255, 255, 255, 0.4);
}

.footer-actions {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.theme-toggle-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: $radius-sm;
  background: rgba(0, 0, 0, 0.03);
  border: 1px solid $border-light;
  color: $text-secondary;
  transition: all $transition-fast;

  &:hover {
    background: rgba(0, 0, 0, 0.06);
    color: $text-primary;
  }
}

#app.dark .theme-toggle-btn {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.08);

  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
}

.theme-icon {
  font-size: 14px;
}

.collapse-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: $radius-sm;
  color: $text-tertiary;
  transition: all $transition-fast;

  &:hover {
    color: $text-primary;
    background: rgba(0, 0, 0, 0.05);
  }
}

#app.dark .collapse-btn {
  &:hover {
    background: rgba(255, 255, 255, 0.06);
  }
}

// ===== 主内容区 =====
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  position: relative;
}

.top-bar {
  height: 64px;
  padding: 0 $spacing-xl;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: $bg-light;
  border-bottom: 1px solid $border-light;
  position: sticky;
  top: 0;
  z-index: 5;
  transition: background 0.3s ease, border-color 0.3s ease;
}

#app.dark .top-bar {
  background: rgba(17, 17, 24, 0.8);
  border-bottom-color: rgba(255, 255, 255, 0.08);
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.breadcrumb-item {
  font-size: 16px;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.top-bar-actions {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
}

.time-display {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  padding: $spacing-xs $spacing-md;
  background: rgba(0, 0, 0, 0.02);
  border-radius: $radius-md;
  border: 1px solid $border-light;
}

#app.dark .time-display {
  background: rgba(255, 255, 255, 0.03);
  border-color: rgba(255, 255, 255, 0.08);
}

.time-value {
  font-family: $font-mono;
  font-size: 14px;
  font-weight: $font-weight-medium;
  color: $primary-start;
}

.time-label {
  font-size: 10px;
  color: $text-tertiary;
}

#app.dark .time-label {
  color: rgba(255, 255, 255, 0.4);
}

.action-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: $radius-md;
  color: $text-secondary;
  transition: all $transition-fast;
  position: relative;

  &:hover {
    color: $text-primary;
    background: rgba(0, 0, 0, 0.03);
  }
}

#app.dark .action-btn {
  &:hover {
    background: rgba(255, 255, 255, 0.06);
  }
}

.notification-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: $danger-color;
  border-radius: 50%;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-xs $spacing-md;
  background: rgba(0, 0, 0, 0.02);
  border-radius: $radius-md;
  border: 1px solid $border-light;
  cursor: pointer;
  transition: all $transition-fast;

  &:hover {
    background: rgba(0, 0, 0, 0.04);
    border-color: rgba(0, 0, 0, 0.12);
  }
}

#app.dark .user-profile {
  background: rgba(255, 255, 255, 0.03);
  border-color: rgba(255, 255, 255, 0.08);

  &:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.15);
  }
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: $radius-sm;
  background: linear-gradient(135deg, $primary-start, $primary-end);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: $font-weight-bold;
  color: white;
}

.user-name {
  font-size: 14px;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.page-content {
  flex: 1;
  padding: $spacing-xl;
  overflow-y: auto;
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    transform: translateX(-100%);

    &.collapsed {
      transform: translateX(-100%);
    }
  }

  .top-bar-actions .user-name {
    display: none;
  }
}
</style>

<!-- 全局主题样式 -->
<style lang="scss">
@use '@/styles/variables.scss' as *;

#app {
  min-height: 100vh;
  background: $bg-lightest;
  transition: background-color 0.3s ease;
}

#app.dark {
  background: $bg-darkest;
}
</style>
