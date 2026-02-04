<template>
  <div id="app" class="app-container" :class="{ 'sidebar-collapsed': isCollapse }">
    <!-- 全局背景效果 -->
    <div class="grid-background"></div>
    <div class="glow-orb glow-orb-1"></div>
    <div class="glow-orb glow-orb-2"></div>
    <div class="glow-orb glow-orb-3"></div>

    <div class="app-layout">
      <!-- 侧边栏 -->
      <aside class="sidebar" :class="{ collapsed: isCollapse }">
        <div class="sidebar-header" @click="$router.push('/')">
          <div class="logo-container">
            <img src="@/assets/hedgehog.png" alt="Logo" class="logo-img" />
          </div>
          <span v-show="!isCollapse" class="brand-name">SAU</span>
        </div>

        <nav class="sidebar-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: activeMenu === item.path }"
          >
            <el-icon class="nav-icon">
              <component :is="item.icon" />
            </el-icon>
            <span v-show="!isCollapse" class="nav-text">{{ item.label }}</span>
            <span v-if="!isCollapse && item.badge" class="nav-badge">{{ item.badge }}</span>
          </router-link>
        </nav>

        <div class="sidebar-footer">
          <!-- 主题切换 -->
          <button class="theme-toggle" @click="toggleTheme" :title="isDark ? '浅色模式' : '深色模式'">
            <span v-if="isDark" class="theme-icon">☀️</span>
            <span v-else class="theme-icon">◐</span>
          </button>

          <!-- 用户卡片 -->
          <div v-show="!isCollapse" class="user-card">
            <div class="user-avatar">A</div>
            <div class="user-info">
              <div class="user-name">Admin</div>
              <div class="user-status">
                <span class="status-dot online"></span>
                Online
              </div>
            </div>
          </div>

          <!-- 折叠按钮 -->
          <button class="collapse-btn" @click="isCollapse = !isCollapse">
            <el-icon>
              <Expand v-if="isCollapse" />
              <Fold v-else />
            </el-icon>
          </button>
        </div>
      </aside>

      <!-- 主内容区 -->
      <main class="main-content">
        <!-- 顶栏 -->
        <header class="topbar">
          <div class="breadcrumb">
            <span class="crumb-page">{{ currentPageTitle }}</span>
          </div>

          <div class="topbar-actions">
            <div class="system-status">
              <span class="status-indicator"></span>
              <span class="status-text">{{ currentTime }}</span>
            </div>
            <button class="action-btn">
              <el-icon><Bell /></el-icon>
            </button>
          </div>
        </header>

        <!-- 页面视图 -->
        <div class="view-container">
          <router-view v-slot="{ Component }">
            <transition name="fade-slide" mode="out-in">
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
  HomeFilled, User, Picture, Upload, Monitor,
  Fold, Expand, Bell
} from '@element-plus/icons-vue'

const route = useRoute()

// ===== 侧边栏状态 =====
const isCollapse = ref(false)

// ===== 主题系统 =====
const isDark = ref(true) // 默认深色
const toggleTheme = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  document.documentElement.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
}

// ===== 时间系统 =====
const currentTime = ref('')
let timeTimer = null
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// ===== 菜单配置 =====
const menuItems = [
  { path: '/', label: '仪表盘', icon: HomeFilled, badge: null },
  { path: '/account-management', label: '账号管理', icon: User, badge: 3 },
  { path: '/material-management', label: '素材库', icon: Picture, badge: null },
  { path: '/publish-center', label: '发布中心', icon: Upload, badge: 5 },
  { path: '/about', label: '系统关于', icon: Monitor, badge: null },
]

// ===== 计算属性 =====
const activeMenu = computed(() => route.path)

const currentPageTitle = computed(() => {
  const item = menuItems.find(m => m.path === route.path)
  return item?.label || 'DASHBOARD'
})

// ===== 生命周期 =====
onMounted(() => {
  // 恢复主题设置
  const savedTheme = localStorage.getItem('theme') || 'dark'
  isDark.value = savedTheme === 'dark'
  document.documentElement.setAttribute('data-theme', savedTheme)

  // 启动时钟
  updateTime()
  timeTimer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timeTimer) clearInterval(timeTimer)
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: $bg-darkest;
}

.app-layout {
  display: flex;
  min-height: 100vh;
}

// ===== 侧边栏 =====
.sidebar {
  width: 240px;
  background: rgba($bg-dark, 0.8);
  backdrop-filter: blur(20px);
  border-right: $border-main;
  display: flex;
  flex-direction: column;
  transition: width $transition-normal;
  z-index: 100;
  position: relative;

  &.collapsed {
    width: 72px;

    .brand-name,
    .nav-text,
    .nav-badge,
    .user-card {
      opacity: 0;
      visibility: hidden;
    }

    .sidebar-footer {
      flex-direction: column;
      gap: $spacing-sm;
    }
  }
}

.sidebar-header {
  padding: $spacing-lg;
  display: flex;
  align-items: center;
  gap: $spacing-md;
  cursor: pointer;
  border-bottom: $border-light;

  .logo-container {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: $primary-color;
    border-radius: $radius-md;
  }

  .logo-img {
    width: 28px;
    height: 28px;
  }

  .brand-name {
    font-family: $font-display;
    font-size: 24px;
    font-weight: 700;
    color: $primary-color;
    letter-spacing: 0.05em;
    transition: opacity $transition-fast;
  }
}

.sidebar-nav {
  flex: 1;
  padding: $spacing-md;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-sm $spacing-md;
  margin-bottom: $spacing-xs;
  color: $text-secondary;
  text-decoration: none;
  font-family: $font-mono;
  font-size: 13px;
  border: 1px solid transparent;
  border-radius: $radius-md;
  transition: all $transition-fast;

  .nav-icon {
    font-size: 18px;
    flex-shrink: 0;
  }

  &:hover {
    color: $text-primary;
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(255, 255, 255, 0.1);
  }

  &.active {
    color: $bg-darkest;
    background: $primary-color;
    border-color: $primary-color;
    font-weight: 600;
  }
}

.nav-badge {
  margin-left: auto;
  background: $bg-dark;
  color: $primary-color;
  font-size: 11px;
  padding: 2px 8px;
  border-radius: $radius-full;
  font-family: $font-mono;
}

.sidebar-footer {
  padding: $spacing-md;
  border-top: $border-light;
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.theme-toggle {
  width: 100%;
  padding: $spacing-sm;
  background: transparent;
  border: $border-light;
  border-radius: $radius-md;
  cursor: pointer;
  font-size: 16px;
  transition: all $transition-fast;

  &:hover {
    background: rgba($primary-color, 0.1);
    border-color: $primary-color;
    color: $primary-color;
  }
}

.user-card {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm;
  background: rgba(255, 255, 255, 0.03);
  border: $border-light;
  border-radius: $radius-md;
  margin-bottom: $spacing-sm;
  transition: opacity $transition-fast;

  .user-avatar {
    width: 32px;
    height: 32px;
    background: $primary-color;
    color: $bg-darkest;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: $font-mono;
    font-weight: 700;
    font-size: 14px;
    border-radius: $radius-sm;
  }

  .user-name {
    font-family: $font-mono;
    font-size: 12px;
    font-weight: 600;
    color: $text-primary;
  }

  .user-status {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 10px;
    color: $text-tertiary;
    font-family: $font-mono;

    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: $text-tertiary;

      &.online {
        background: $success-color;
        box-shadow: 0 0 8px rgba($success-color, 0.5);
      }
    }
  }
}

.collapse-btn {
  width: 100%;
  padding: $spacing-sm;
  background: transparent;
  border: $border-light;
  border-radius: $radius-md;
  cursor: pointer;
  color: $text-secondary;
  font-size: 16px;
  transition: all $transition-fast;

  &:hover {
    background: rgba($primary-color, 0.1);
    border-color: $primary-color;
    color: $primary-color;
  }
}

// ===== 主内容区 =====
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: $spacing-lg;
  min-width: 0;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-xl;
  padding: $spacing-md $spacing-lg;
  background: rgba($bg-dark, 0.5);
  border: $border-light;
  border-radius: $radius-lg;
  backdrop-filter: blur(10px);
}

.breadcrumb {
  .crumb-page {
    font-family: $font-mono;
    font-size: 18px;
    font-weight: 700;
    color: $text-primary;
    letter-spacing: 0.1em;
  }
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.system-status {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-xs $spacing-md;
  background: rgba(255, 255, 255, 0.03);
  border: $border-light;
  border-radius: $radius-md;
  font-family: $font-mono;
  font-size: 12px;

  .status-indicator {
    width: 8px;
    height: 8px;
    background: $success-color;
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
  }

  .status-text {
    color: $text-secondary;
  }
}

.action-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: $border-light;
  border-radius: $radius-md;
  color: $text-secondary;
  cursor: pointer;
  transition: all $transition-fast;

  &:hover {
    background: rgba($primary-color, 0.1);
    border-color: $primary-color;
    color: $primary-color;
  }
}

.view-container {
  flex: 1;
  position: relative;
}

// ===== 动画 =====
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 0 0 rgba($success-color, 0.4);
  }
  50% {
    opacity: 0.8;
    box-shadow: 0 0 0 4px rgba($success-color, 0);
  }
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all $transition-normal ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
