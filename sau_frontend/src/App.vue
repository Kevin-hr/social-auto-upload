<template>
  <div id="app" class="posthog-app" :class="{ 'theme-dark': isDark }">
    <!-- 全局网格背景 -->
    <div class="grid-background"></div>

    <!-- 光晕效果 -->
    <div class="glow-orb glow-orb-1"></div>
    <div class="glow-orb glow-orb-2"></div>

    <div class="app-layout">
      <!-- 复古边栏 -->
      <aside class="retro-sidebar" :class="{ collapsed: isCollapse }">
        <div class="sidebar-header" @click="$router.push('/')">
          <img src="@/assets/hedgehog.png" alt="Logo" class="sidebar-logo" />
          <h2 v-show="!isCollapse" class="brand-name">SocialAuto</h2>
        </div>

        <nav class="sidebar-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item-retro"
            :class="{ active: activeMenu === item.path }"
          >
            <el-icon class="nav-icon"><component :is="item.icon" /></el-icon>
            <span v-show="!isCollapse" class="nav-text">{{ item.label }}</span>
            <span v-if="!isCollapse && item.badge" class="nav-badge-retro">{{ item.badge }}</span>
          </router-link>
        </nav>

        <div class="sidebar-footer">
          <!-- 主题切换按钮 -->
          <button class="theme-toggle-btn" @click="toggleTheme" :title="isDark ? '切换到浅色模式' : '切换到深色模式'">
            <span v-if="isDark" class="theme-icon">&#9728;</span>
            <span v-else class="theme-icon">&#9790;</span>
          </button>

          <div class="user-card-retro retro-window" v-show="!isCollapse">
            <div class="user-avatar-retro">Admin</div>
            <div class="user-info">
              <div class="username">Hedgehog Pro</div>
              <div class="status-tag">Online</div>
            </div>
          </div>
          
          <!-- 个人微信二维码 -->
          <div class="wechat-qr-retro retro-window" v-show="!isCollapse">
             <div class="qr-title">扫码加微信</div>
             <div class="qr-container">
               <img src="@/assets/wechat-qr.png" alt="WeChat QR" class="wechat-img" />
             </div>
             <div class="qr-desc">获取更多支持</div>
          </div>
          <button class="collapse-btn-retro" @click="isCollapse = !isCollapse">
            <el-icon><Expand v-if="isCollapse" /><Fold v-else /></el-icon>
          </button>
        </div>
      </aside>

      <!-- 主内容区 -->
      <main class="main-content-retro">
        <!-- 顶栏 -->
        <header class="retro-header">
          <div class="header-breadcrumb retro-window">
            {{ currentPageTitle }}
          </div>

          <div class="header-actions">
            <div class="system-status-retro retro-window">
              <span class="status-dot pulse"></span>
              {{ currentTime }}
            </div>
            <button class="action-btn-retro block-btn">
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
const isDark = ref(false)
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
  { path: '/', label: '仪表盘', icon: HomeFilled },
  { path: '/account-management', label: '账号管理', icon: User, badge: 3 },
  { path: '/material-management', label: '素材库', icon: Picture },
  { path: '/publish-center', label: '发布中心', icon: Upload, badge: 5 },
  { path: '/about', label: '系统关于', icon: Monitor },
]

// ===== 计算属性 =====
const activeMenu = computed(() => route.path)

const currentPageTitle = computed(() => {
  const item = menuItems.find(m => m.path === route.path)
  return item?.label || '指挥中心'
})

// ===== 生命周期 =====
onMounted(() => {
  // 恢复主题设置
  const savedTheme = localStorage.getItem('theme') || 'light'
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

.posthog-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s ease;
}

.app-layout {
  display: flex;
  min-height: 100vh;
}

// ===== 复古边栏 =====
.retro-sidebar {
  width: 260px;
  background: $bg-sidebar;
  border-right: $border-main;
  display: flex;
  flex-direction: column;
  transition: width $transition-normal;
  z-index: 100;
  position: relative;

  &.collapsed {
    width: 64px;
    .brand-name { display: none; }
    .sidebar-footer { flex-direction: column; }
  }
}

.sidebar-header {
  padding: $spacing-lg;
  display: flex;
  align-items: center;
  gap: $spacing-md;
  cursor: pointer;
  border-bottom: $border-light;

  .sidebar-logo {
    width: 40px;
    image-rendering: pixelated;
  }

  .brand-name {
    font-family: $font-display;
    font-size: 20px;
    font-weight: 900;
    margin: 0;
  }
}

.sidebar-nav {
  flex: 1;
  padding: $spacing-md;
}

.nav-item-retro {
  display: flex;
  align-items: center;
  padding: $spacing-sm $spacing-md;
  margin-bottom: $spacing-sm;
  color: $text-primary;
  text-decoration: none;
  font-weight: bold;
  border: 1px solid transparent;
  transition: all $transition-fast;

  .nav-icon {
    font-size: 20px;
    margin-right: $spacing-md;
  }

  &:hover {
    background: rgba(0, 0, 0, 0.05);
    border: $border-light;
    transform: translateX(2px);
  }

  &.active {
    background: $primary-color;
    border: $border-main;
    box-shadow: $shadow-block-sm;
    transform: translateX(4px);
  }
}

.nav-badge-retro {
  margin-left: auto;
  background: #000;
  color: #fff;
  font-size: 10px;
  padding: 2px 6px;
  font-family: $font-mono;
}

.sidebar-footer {
  padding: $spacing-md;
  border-top: $border-light;
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.theme-toggle-btn {
  width: 100%;
  padding: $spacing-sm;
  background: transparent;
  border: $border-light;
  cursor: pointer;
  font-size: 18px;
  transition: all $transition-fast;

  &:hover {
    background: $primary-color;
    border: $border-main;
  }

  .theme-icon {
    display: block;
    text-align: center;
  }
}

.user-card-retro {
  padding: $spacing-sm;
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-bottom: $spacing-sm;

  .user-avatar-retro {
    width: 32px;
    height: 32px;
    background: #000;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: bold;
  }

  .username {
    font-size: 12px;
    font-weight: bold;
  }

  .status-tag {
    font-size: 10px;
    color: $success-color;
  }
}

.wechat-qr-retro {
  padding: $spacing-sm;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  margin-bottom: $spacing-sm;
  background: white !important; /* QR码需要白底 */
  
  .qr-title {
    font-size: 10px;
    font-weight: bold;
    color: #000;
  }

  .qr-container {
    width: 120px;
    height: 120px;
    display: flex;
    justify-content: center;
    align-items: center;
    
    .wechat-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      image-rendering: auto; /* 保持图片清晰 */
    }
  }

  .qr-desc {
    font-size: 10px;
    color: #666;
  }
}

.collapse-btn-retro {
  width: 100%;
  padding: $spacing-xs;
  background: transparent;
  border: $border-light;
  cursor: pointer;

  &:hover {
    background: $primary-color;
    border: $border-main;
  }
}

// ===== 主内容区 =====
.main-content-retro {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: $spacing-lg;
  min-width: 0;
}

.retro-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-xl;
  height: auto;
  padding: 0;
}

.header-breadcrumb {
  padding: $spacing-sm $spacing-xl;
  font-family: $font-display;
  font-weight: 900;
  font-size: 18px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.system-status-retro {
  padding: $spacing-sm $spacing-md;
  font-family: $font-mono;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: $spacing-sm;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: $success-color;
  border: 1px solid #000;

  &.pulse {
    animation: pulse 2s infinite;
  }
}

.view-container {
  flex: 1;
  position: relative;
}

// ===== 动画 =====
@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.4; }
  100% { opacity: 1; }
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.2s ease;
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
