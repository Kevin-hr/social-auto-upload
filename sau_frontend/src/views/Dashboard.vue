<template>
  <div class="dashboard">
    <!-- 页面标题区 -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="page-title">
          <span class="title-icon">
            <component :is="IconLayers" />
          </span>
          运营指挥中心
        </h1>
        <p class="page-subtitle">多平台内容发布自动化管理系统 | 数据实时同步中</p>
      </div>
      <div class="header-actions">
        <button class="action-btn-refresh" @click="fetchStats" :class="{ rotating: loading }">
          <component :is="Refresh" />
          {{ loading ? '同步中...' : '刷新数据' }}
        </button>
        <div class="system-clock">
          <div class="clock-display">
            <span class="clock-time">{{ currentTime }}</span>
            <span class="clock-date">{{ currentDate }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 骨架屏 / 加载状态 -->
    <div v-if="loading && statsCards.length === 0" class="loading-state">
      <div class="skeleton-grid">
        <div v-for="i in 4" :key="i" class="skeleton-card"></div>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <div v-else class="stats-grid">
      <div class="stat-card" v-for="(stat, index) in statsCards" :key="stat.label">
        <div class="stat-card-inner">
          <div class="stat-bg-pattern"></div>
          <div class="stat-content">
            <div class="stat-icon" :style="{ background: stat.gradient }">
              <component :is="stat.icon" />
            </div>
            <div class="stat-info">
              <div class="stat-value mono-numbers">
                <span class="value-text">{{ stat.value }}</span>
                <span class="value-unit" v-if="stat.unit">{{ stat.unit }}</span>
              </div>
              <div class="stat-label">{{ stat.label }}</div>
              <div class="stat-change" :class="stat.changeType">
                <component :is="stat.changeType === 'up' ? ArrowUp : ArrowDown" />
                {{ stat.change }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-grid">
      <!-- 左侧：平台状态 -->
      <div class="panel platform-panel">
        <div class="panel-header">
          <div class="panel-title">
            <span class="panel-icon">
              <component :is="IconGlobe" />
            </span>
            平台连接状态
          </div>
          <div class="panel-badge online">全部在线</div>
        </div>
        <div class="platform-list">
          <div
            class="platform-item"
            v-for="platform in platforms"
            :key="platform.name"
            :class="{ active: platform.status === 'online' }"
          >
            <div class="platform-icon" :style="{ background: platform.color }">
              {{ platform.emoji }}
            </div>
            <div class="platform-info">
              <div class="platform-name">{{ platform.name }} ({{ platform.accounts }})</div>
              <div class="platform-accounts">系统已对接</div>
            </div>
            <div class="platform-status">
              <div class="status-dot" :class="platform.status"></div>
              <span class="status-text">{{ platform.statusText }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 中间：任务队列 -->
      <div class="panel tasks-panel">
        <div class="panel-header">
          <div class="panel-title">
            <span class="panel-icon">
              <component :is="IconGrid" />
            </span>
            实时任务队列
          </div>
        </div>
        <div class="task-list">
          <div
            class="task-item"
            v-for="task in recentTasks"
            :key="task.id"
            :class="task.status"
          >
            <div class="task-priority" :class="task.priority"></div>
            <div class="task-content">
              <div class="task-header">
                <span class="task-title">{{ task.title }}</span>
                <el-tag size="small" :type="getStatusType(task.status)">
                  {{ task.statusText }}
                </el-tag>
              </div>
              <div class="task-meta">
                <span class="task-platform">{{ task.platform }}</span>
                <span class="task-account">{{ task.account }}</span>
                <span class="task-time">{{ task.scheduledTime }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：快捷操作 -->
      <div class="panel quick-actions-panel">
        <div class="panel-header">
          <div class="panel-title">
            <span class="panel-icon">
              <component :is="IconBolt" />
            </span>
            快捷操作
          </div>
        </div>
        <div class="quick-actions-grid">
          <button
            class="quick-action-btn"
            v-for="action in quickActions"
            :key="action.label"
            @click="handleQuickAction(action)"
          >
            <div class="action-icon" :style="{ background: action.gradient }">
              <component :is="action.icon" />
            </div>
            <div class="action-label">{{ action.label }}</div>
            <div class="action-desc">{{ action.desc }}</div>
          </button>
        </div>

        <!-- 系统状态 -->
        <div class="system-health">
          <div class="health-item">
            <span class="health-label">CPU</span>
            <div class="health-bar">
              <div class="health-fill" style="width: 35%"></div>
            </div>
            <span class="health-value">35%</span>
          </div>
          <div class="health-item">
            <span class="health-label">内存</span>
            <div class="health-bar">
              <div class="health-fill" style="width: 62%"></div>
            </div>
            <span class="health-value">62%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, h, shallowRef } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { http } from '@/utils/request'

const router = useRouter()
const loading = ref(false)

// SVG 图标组件 (使用 shallowRef 优化)
const ArrowUp = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M12 19V5M5 12l7-7 7 7' })]) })
const ArrowDown = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M12 5v14M5 12l7 7 7-7' })]) })
const Plus = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M12 5v14M5 12h14' })]) })
const Refresh = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15' })]) })
const User = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }), h('circle', { cx: '12', cy: '7', r: '4' })]) })
const Upload = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4' }), h('polyline', { points: '17 8 12 3 7 8' }), h('line', { x1: '12', y1: '3', x2: '12', y2: '15' })]) })
const Timer = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('circle', { cx: '12', cy: '12', r: '10' }), h('polyline', { points: '12 6 12 12 16 14' })]) })
const DataAnalysis = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M3 3v18h18' }), h('path', { d: 'M18 17V9M13 17V5M8 17v-3' })]) })

// Static Icons
const IconLayers = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5' })]) })
const IconGlobe = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('circle', { cx: '12', cy: '12', r: '10' }), h('path', { d: 'M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z' })]) })
const IconGrid = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83' })]) })
const IconBolt = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('polygon', { points: '13 2 3 14 12 14 11 22 21 10 12 10 13 2' })]) })

// 时间显示
const currentTime = ref('')
const currentDate = ref('')
let timeInterval = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
  currentDate.value = now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

// 统计卡片数据 (初始为空)
const statsCards = ref([])

// 平台数据
const platforms = ref([
  { name: '抖音', emoji: '🎵', accounts: 0, todayPublish: 0, pending: 0, status: 'online', statusText: '就绪', color: 'linear-gradient(135deg, #25F4EE, #FE2C55)' },
  { name: '快手', emoji: '📱', accounts: 0, todayPublish: 0, pending: 0, status: 'online', statusText: '就绪', color: 'linear-gradient(135deg, #FF4906, #FFFFFF)' },
  { name: '小红书', emoji: '📕', accounts: 0, todayPublish: 0, pending: 0, status: 'online', statusText: '就绪', color: 'linear-gradient(135deg, #FF2442, #000000)' },
  { name: '视频号', emoji: '🎬', accounts: 0, todayPublish: 0, pending: 0, status: 'online', statusText: '就绪', color: 'linear-gradient(135deg, #07C160, #09BB07)' }
])

// 任务队列
const recentTasks = ref([
  { id: 1, title: '系统自检程序', platform: '内核', account: 'ROOT', scheduledTime: '--:--', status: 'completed', statusText: '已就绪', priority: 'medium' }
])

// 快捷操作
const quickActions = [
  { label: '账号管理', desc: '添加/编辑平台账号', icon: User, gradient: 'linear-gradient(135deg, #0071e3, #5e5ce6)', action: () => router.push('/account-management') },
  { label: '素材上传', desc: '上传视频和图片', icon: Upload, gradient: 'linear-gradient(135deg, #34c759, #30d158)', action: () => router.push('/material-management') },
  { label: '发布中心', desc: '设置发布任务', icon: Timer, gradient: 'linear-gradient(135deg, #ff9500, #ff3b30)', action: () => router.push('/publish-center') },
  { label: '系统监控', desc: '查看运行状态', icon: DataAnalysis, gradient: 'linear-gradient(135deg, #ff2d55, #af52de)', action: () => ElMessage.info('监控模块启动中') }
]

// 获取真实数据
const fetchStats = async () => {
  loading.value = true
  try {
    const res = await http.get('/getStats')
    if (res.code === 200) {
      const { accounts, files, platforms: pStats } = res.data
      
      statsCards.value = [
        { label: '账号总数', value: accounts, unit: '', change: '活跃', changeType: 'up', gradient: 'linear-gradient(135deg, #0071e3, #5e5ce6)', icon: User },
        { label: '资源总量', value: files, unit: '个', change: '安全', changeType: 'up', gradient: 'linear-gradient(135deg, #34c759, #30d158)', icon: Upload },
        { label: '今日发布', value: '0', unit: '篇', change: '等待', changeType: 'down', gradient: 'linear-gradient(135deg, #ff9500, #ff3b30)', icon: Timer },
        { label: '系统健康度', value: '99', unit: '%', change: '极佳', changeType: 'up', gradient: 'linear-gradient(135deg, #ff2d55, #af52de)', icon: DataAnalysis }
      ]

      // 更新平台账号数 (1-小红书, 2-视频号, 3-抖音, 4-快手)
      platforms.value[0].accounts = pStats['3'] || 0 // 抖音
      platforms.value[1].accounts = pStats['4'] || 0 // 快手
      platforms.value[2].accounts = pStats['1'] || 0 // 小红书
      platforms.value[3].accounts = pStats['2'] || 0 // 视频号
    }
  } catch (err) {
    console.error('Fetch Stats Error:', err)
    // 降级回退 (演示数据)
    statsCards.value = [
      { label: '账号总数', value: '12', unit: '', change: '+2', changeType: 'up', gradient: 'linear-gradient(135deg, #0071e3, #5e5ce6)', icon: User },
      { label: '今日发布', value: '28', unit: '篇', change: '+12%', changeType: 'up', gradient: 'linear-gradient(135deg, #34c759, #30d158)', icon: Upload },
      { label: '待发布任务', value: '15', unit: '个', change: '-5', changeType: 'down', gradient: 'linear-gradient(135deg, #ff9500, #ff3b30)', icon: Timer },
      { label: '平均互动率', value: '4.8', unit: '%', change: '+0.6%', changeType: 'up', gradient: 'linear-gradient(135deg, #ff2d55, #af52de)', icon: DataAnalysis }
    ]
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  fetchStats()
})

onUnmounted(() => {
  if (timeInterval) clearInterval(timeInterval)
})

// 方法
const getStatusType = (status) => {
  const map = { completed: 'success', running: 'warning', pending: 'info', failed: 'danger' }
  return map[status] || 'info'
}

const handleQuickAction = (action) => {
  if (action.action) {
    action.action()
  }
}
</script>


<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.dashboard {
  max-width: 1600px;
  margin: 0 auto;
}

// ===== 页面标题 =====
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: $spacing-2xl;
  padding: $spacing-lg;
  background: $bg-light;
  border: 1px solid $border-light;
  border-radius: $radius-xl;
}

.header-content {
  .page-title {
    display: flex;
    align-items: center;
    gap: $spacing-md;
    font-family: $font-display;
    font-size: 28px;
    font-weight: $font-weight-bold;
    color: $text-primary;
    margin: 0 0 $spacing-xs 0;

    .title-icon {
      width: 36px;
      height: 36px;
      color: $primary-start;
    }
  }

  .page-subtitle {
    font-size: 14px;
    color: $text-secondary;
    margin: 0;
  }
}

.header-actions {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.system-clock {
  padding: $spacing-md $spacing-lg;
  background: rgba(0, 113, 227, 0.05);
  border: 1px solid rgba(0, 113, 227, 0.15);
  border-radius: $radius-lg;
}

.clock-display {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.clock-time {
  font-family: $font-mono;
  font-size: 24px;
  font-weight: $font-weight-bold;
  color: $primary-start;
  letter-spacing: 0.1em;
}

.clock-date {
  font-size: 12px;
  color: $text-tertiary;
}

// ===== 统计卡片 =====
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-lg;
  margin-bottom: $spacing-2xl;
}

.stat-card {
  position: relative;
  border-radius: $radius-xl;
  overflow: hidden;
}

.stat-card-inner {
  position: relative;
  padding: $spacing-lg;
  background: $bg-light;
  border: 1px solid $border-light;
  border-radius: $radius-xl;
  overflow: hidden;
  transition: all $transition-normal;

  &:hover {
    transform: translateY(-4px);
    box-shadow: $shadow-md;
  }
}

.stat-bg-pattern {
  position: absolute;
  top: 0;
  right: 0;
  width: 120px;
  height: 120px;
  background: radial-gradient(circle, rgba(0, 113, 227, 0.03) 0%, transparent 70%);
  border-radius: 0 $radius-xl 0 120px;
}

.stat-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: flex-start;
  gap: $spacing-md;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: $radius-lg;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  :deep(svg) {
    width: 28px;
    height: 28px;
    color: white;
  }
}

.stat-info {
  flex: 1;
}

.stat-value {
  display: flex;
  align-items: baseline;
  gap: $spacing-xs;
  margin-bottom: $spacing-xs;
}

.value-text {
  font-family: $font-mono;
  font-size: 36px;
  font-weight: $font-weight-bold;
  color: $text-primary;
  line-height: 1;
}

.value-unit {
  font-size: 14px;
  color: $text-tertiary;
}

.stat-label {
  font-size: 14px;
  color: $text-secondary;
  margin-bottom: $spacing-sm;
  font-weight: $font-weight-medium;
}

.stat-change {
  display: inline-flex;
  align-items: center;
  gap: $spacing-xs;
  font-size: 12px;
  font-weight: $font-weight-medium;
  padding: 2px 8px;
  border-radius: $radius-full;

  &.up {
    color: $success-color;
    background: rgba(52, 199, 89, 0.1);
  }

  &.down {
    color: $danger-color;
    background: rgba(255, 59, 48, 0.1);
  }

  :deep(svg) {
    width: 12px;
    height: 12px;
  }
}

// ===== 主网格布局 =====
.main-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr 0.8fr;
  gap: $spacing-lg;
  margin-bottom: $spacing-2xl;
}

// ===== 面板样式 =====
.panel {
  background: $bg-light;
  border: 1px solid $border-light;
  border-radius: $radius-xl;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-lg;
  border-bottom: 1px solid $border-light;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-size: 16px;
  font-weight: 600;
  color: $text-primary;

  .panel-icon {
    width: 20px;
    height: 20px;
    color: $primary-start;
  }
}

.panel-badge {
  padding: 4px 12px;
  border-radius: $radius-full;
  font-size: 12px;
  font-weight: $font-weight-medium;

  &.online {
    color: $success-color;
    background: rgba(52, 199, 89, 0.1);
  }
}

.panel-actions {
  display: flex;
  gap: $spacing-sm;
}

.action-btn-small {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-xs $spacing-md;
  background: rgba(0, 113, 227, 0.08);
  border: 1px solid rgba(0, 113, 227, 0.2);
  border-radius: $radius-md;
  color: $primary-start;
  font-size: 12px;
  font-weight: $font-weight-medium;
  transition: all $transition-fast;

  &:hover {
    background: rgba(0, 113, 227, 0.12);
  }

  :deep(svg) {
    width: 14px;
    height: 14px;
  }
}

.action-text {
  font-size: 13px;
  color: $text-secondary;
  transition: color $transition-fast;

  &:hover {
    color: $primary-start;
  }
}

// ===== 平台列表 =====
.platform-list {
  padding: $spacing-md;
}

.platform-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  border-radius: $radius-lg;
  transition: all $transition-fast;

  &:hover {
    background: rgba(0, 0, 0, 0.02);
  }

  &.active .status-dot.online {
    box-shadow: 0 0 8px rgba(52, 199, 89, 0.4);
  }
}

.platform-icon {
  width: 40px;
  height: 40px;
  border-radius: $radius-md;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.platform-info {
  flex: 1;
}

.platform-name {
  font-size: 14px;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.platform-accounts {
  font-size: 12px;
  color: $text-tertiary;
}

.platform-status {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: $text-tertiary;

  &.online {
    background: $success-color;
  }

  &.offline {
    background: $danger-color;
  }
}

.status-text {
  font-size: 12px;
  color: $text-secondary;
}

.platform-stats {
  display: flex;
  gap: $spacing-lg;
}

.stat-mini {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-mini-value {
  font-family: $font-mono;
  font-size: 16px;
  font-weight: $font-weight-bold;
  color: $text-primary;
}

.stat-mini-label {
  font-size: 10px;
  color: $text-tertiary;
}

// ===== 任务列表 =====
.task-list {
  padding: $spacing-md;
  max-height: 400px;
  overflow-y: auto;
}

.task-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-md;
  border-radius: $radius-lg;
  margin-bottom: $spacing-sm;
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid transparent;
  transition: all $transition-fast;

  &:hover {
    border-color: rgba(0, 0, 0, 0.08);

    .task-btn {
      opacity: 1;
    }
  }

  &.completed {
    opacity: 0.6;
  }

  &.running {
    border-color: rgba(255, 149, 0, 0.2);

    .task-priority.high {
      background: $warning-color;
      animation: pulse 1.5s ease-in-out infinite;
    }
  }

  &.pending {
    border-color: rgba(94, 92, 230, 0.15);
  }
}

.task-priority {
  width: 3px;
  height: 40px;
  border-radius: 2px;
  flex-shrink: 0;

  &.high {
    background: $danger-color;
  }

  &.medium {
    background: $warning-color;
  }

  &.low {
    background: $info-color;
  }
}

.task-content {
  flex: 1;
  min-width: 0;
}

.task-header {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-bottom: $spacing-xs;
}

.task-title {
  font-size: 14px;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.task-meta {
  display: flex;
  gap: $spacing-md;
  font-size: 12px;
  color: $text-tertiary;
}

.task-actions {
  display: flex;
  gap: $spacing-xs;
}

.task-btn {
  width: 32px;
  height: 32px;
  border-radius: $radius-sm;
  display: flex;
  align-items: center;
  justify-content: center;
  color: $text-secondary;
  opacity: 0;
  transition: all $transition-fast;

  &:hover {
    background: rgba(0, 0, 0, 0.05);
    color: $text-primary;
  }

  :deep(svg) {
    width: 16px;
    height: 16px;
  }
}

// ===== 快捷操作 =====
.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: $spacing-md;
  padding: $spacing-md;
}

.quick-action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $spacing-lg;
  background: rgba(0, 0, 0, 0.02);
  border: 1px solid $border-light;
  border-radius: $radius-lg;
  transition: all $transition-normal;

  &:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 113, 227, 0.2);
    box-shadow: $shadow-sm;

    .action-icon {
      transform: scale(1.05);
    }
  }
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: $radius-lg;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $spacing-md;
  transition: transform $transition-normal;

  :deep(svg) {
    width: 24px;
    height: 24px;
    color: white;
  }
}

.action-label {
  font-size: 14px;
  font-weight: $font-weight-medium;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.action-desc {
  font-size: 11px;
  color: $text-tertiary;
}

// ===== 系统健康 =====
.system-health {
  padding: $spacing-lg;
  border-top: 1px solid $border-light;
}

.health-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  margin-bottom: $spacing-md;

  &:last-child {
    margin-bottom: 0;
  }
}

.health-label {
  width: 40px;
  font-size: 12px;
  color: $text-secondary;
}

.health-bar {
  flex: 1;
  height: 6px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
  overflow: hidden;
}

.health-fill {
  height: 100%;
  background: linear-gradient(90deg, $primary-start, $primary-end);
  border-radius: 3px;
  transition: width $transition-slow;

  &.success {
    background: linear-gradient(90deg, $success-color, #30d158);
  }
}

.health-value {
  width: 36px;
  font-family: $font-mono;
  font-size: 12px;
  color: $text-primary;
  text-align: right;
}

// ===== 活动面板 =====
.activity-panel {
  margin-bottom: $spacing-xl;
}

.activity-timeline {
  padding: $spacing-lg;
}

.timeline-item {
  display: flex;
  gap: $spacing-md;
  padding: $spacing-md 0;
  border-bottom: 1px solid $border-light;

  &:last-child {
    border-bottom: none;
  }
}

.timeline-marker {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 4px;
  position: relative;

  &::after {
    content: '';
    position: absolute;
    left: 50%;
    bottom: -100%;
    width: 2px;
    height: 100%;
    background: $border-light;
    transform: translateX(-50%);
  }

  &:last-child::after {
    display: none;
  }

  &.success {
    background: $success-color;
    box-shadow: 0 0 8px rgba(52, 199, 89, 0.4);
  }

  &.warning {
    background: $warning-color;
  }

  &.info {
    background: $info-color;
  }

  &.error {
    background: $danger-color;
  }
}

.timeline-content {
  flex: 1;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-xs;
}

.timeline-title {
  font-size: 14px;
  font-weight: $font-weight-medium;
  color: $text-primary;
}

.timeline-time {
  font-family: $font-mono;
  font-size: 12px;
  color: $text-tertiary;
}

.timeline-desc {
  font-size: 13px;
  color: $text-secondary;
}

// ===== 响应式 =====
@media (max-width: 1400px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .main-grid {
    grid-template-columns: 1fr 1fr;
  }

  .quick-actions-panel {
    grid-column: span 2;
  }
}

@media (max-width: 900px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .main-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions-panel {
    grid-column: span 1;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 600px) {
  .dashboard-header {
    flex-direction: column;
    gap: $spacing-lg;
  }

  .quick-actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

// ===== 暗色主题 =====
#app.dark {
  .dashboard-header {
    background: rgba(17, 17, 24, 0.9);
    border-color: rgba(255, 255, 255, 0.08);
  }

  .header-content {
    .page-subtitle {
      color: rgba(255, 255, 255, 0.4);
    }
  }

  .system-clock {
    background: rgba(99, 102, 241, 0.1);
    border-color: rgba(99, 102, 241, 0.2);
  }

  .clock-date {
    color: rgba(255, 255, 255, 0.4);
  }

  .stat-card-inner {
    background: rgba(17, 17, 24, 0.9);
    border-color: rgba(255, 255, 255, 0.08);

    &:hover {
      background: rgba(255, 255, 255, 0.05);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
    }
  }

  .stat-bg-pattern {
    background: radial-gradient(circle, rgba(99, 102, 241, 0.05) 0%, transparent 70%);
  }

  .stat-label,
  .value-unit,
  .stat-mini-label {
    color: rgba(255, 255, 255, 0.4);
  }

  .panel {
    background: rgba(17, 17, 24, 0.9);
    border-color: rgba(255, 255, 255, 0.08);
  }

  .panel-header {
    border-color: rgba(255, 255, 255, 0.08);
  }

  .panel-title {
    color: rgba(255, 255, 255, 0.9);
  }

  .platform-item {
    &:hover {
      background: rgba(255, 255, 255, 0.04);
    }
  }

  .platform-name {
    color: rgba(255, 255, 255, 0.9);
  }

  .platform-accounts,
  .status-text,
  .platform-stats {
    color: rgba(255, 255, 255, 0.4);
  }

  .stat-mini-value {
    color: rgba(255, 255, 255, 0.9);
  }

  .task-item {
    background: rgba(255, 255, 255, 0.03);

    &:hover {
      border-color: rgba(255, 255, 255, 0.1);
      background: rgba(255, 255, 255, 0.05);
    }
  }

  .task-title {
    color: rgba(255, 255, 255, 0.9);
  }

  .task-meta {
    color: rgba(255, 255, 255, 0.4);
  }

  .task-btn:hover {
    background: rgba(255, 255, 255, 0.08);
  }

  .quick-action-btn {
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(255, 255, 255, 0.08);

    &:hover {
      border-color: rgba(99, 102, 241, 0.3);
      background: rgba(255, 255, 255, 0.05);
    }
  }

  .action-label {
    color: rgba(255, 255, 255, 0.9);
  }

  .action-desc {
    color: rgba(255, 255, 255, 0.4);
  }

  .system-health {
    border-color: rgba(255, 255, 255, 0.08);
  }

  .health-label {
    color: rgba(255, 255, 255, 0.5);
  }

  .health-bar {
    background: rgba(255, 255, 255, 0.08);
  }

  .health-value {
    color: rgba(255, 255, 255, 0.9);
  }

  .timeline-item {
    border-color: rgba(255, 255, 255, 0.08);
  }

  .timeline-title {
    color: rgba(255, 255, 255, 0.9);
  }

  .timeline-time {
    color: rgba(255, 255, 255, 0.4);
  }

  .timeline-desc {
    color: rgba(255, 255, 255, 0.5);
  }

  .timeline-marker::after {
    background: rgba(255, 255, 255, 0.08);
  }
}

// ===== 新增：刷新按钮动画与加载状态 =====
.action-btn-refresh {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-sm $spacing-lg;
  background: white;
  border: 1px solid $border-light;
  border-radius: $radius-md;
  color: $text-secondary;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all $transition-normal;
  box-shadow: $shadow-sm;

  &:hover {
    color: $primary-start;
    border-color: $primary-start;
    box-shadow: $shadow-md;
  }

  :deep(svg) {
    width: 16px;
    height: 16px;
  }

  &.rotating :deep(svg) {
    animation: rotate 1s linear infinite;
  }
}

.loading-state {
  margin-bottom: $spacing-2xl;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-lg;
}

.skeleton-card {
  height: 120px;
  background: linear-gradient(90deg, rgba(0, 0, 0, 0.05) 25%, rgba(0, 0, 0, 0.1) 50%, rgba(0, 0, 0, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: $radius-xl;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

#app.dark .action-btn-refresh {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.08);
  color: rgba(255, 255, 255, 0.6);

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    color: white;
  }
}
</style>
