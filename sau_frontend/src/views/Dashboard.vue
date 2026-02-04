<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div
        v-for="(stat, index) in statsCards"
        :key="stat.label"
        class="stat-card"
        :style="{ '--delay': `${index * 0.1}s` }"
      >
        <div class="stat-card-inner brutal-card">
          <div class="stat-bg-glow" :style="{ background: stat.gradient }"></div>
          <div class="stat-content">
            <div class="stat-icon" :style="{ background: stat.gradient }">
              <el-icon><component :is="stat.icon" /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">
                <span class="value-text mono-numbers">{{ stat.value }}</span>
                <span v-if="stat.unit" class="value-unit">{{ stat.unit }}</span>
              </div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
          <div class="stat-footer">
            <span class="stat-change" :class="stat.changeType">
              <el-icon v-if="stat.changeType === 'up'"><Top /></el-icon>
              <el-icon v-else><Bottom /></el-icon>
              {{ stat.change }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主网格 -->
    <div class="main-grid">
      <!-- 平台状态 -->
      <div class="panel platforms-panel brutal-card">
        <div class="panel-header">
          <h3 class="panel-title">
            <span class="panel-icon">◈</span>
            PLATFORMS
          </h3>
          <el-tag type="success" size="small">ONLINE</el-tag>
        </div>
        <div class="platform-list">
          <div
            v-for="platform in platforms"
            :key="platform.name"
            class="platform-item"
          >
            <div class="platform-icon" :style="{ background: platform.color }">
              {{ platform.emoji }}
            </div>
            <div class="platform-info">
              <div class="platform-name">{{ platform.name }}</div>
              <div class="platform-accounts mono-numbers">{{ platform.accounts }} ACCOUNTS</div>
            </div>
            <div class="platform-stats">
              <div class="stat-mini">
                <div class="stat-mini-value mono-numbers">{{ platform.todayPublish }}</div>
                <div class="stat-mini-label">TODAY</div>
              </div>
              <div class="stat-mini">
                <div class="stat-mini-value mono-numbers">{{ platform.pending }}</div>
                <div class="stat-mini-label">PENDING</div>
              </div>
            </div>
            <div class="platform-status">
              <span class="status-dot" :class="platform.status"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 任务队列 -->
      <div class="panel tasks-panel brutal-card">
        <div class="panel-header">
          <h3 class="panel-title">
            <span class="panel-icon">▶</span>
            TASK QUEUE
          </h3>
          <span class="task-count mono-numbers">{{ recentTasks.length }}</span>
        </div>
        <div class="task-list">
          <div
            v-for="task in recentTasks"
            :key="task.id"
            class="task-item"
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
                <span>{{ task.platform }}</span>
                <span>{{ task.account }}</span>
                <span class="mono-numbers">{{ task.scheduledTime }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 快捷操作 -->
      <div class="panel quick-actions-panel brutal-card">
        <div class="panel-header">
          <h3 class="panel-title">
            <span class="panel-icon">◇</span>
            QUICK ACTIONS
          </h3>
        </div>
        <div class="quick-actions-grid">
          <button
            v-for="action in quickActions"
            :key="action.label"
            class="quick-action-btn"
            @click="handleQuickAction(action)"
          >
            <div class="action-icon" :style="{ background: action.gradient }">
              <el-icon><component :is="action.icon" /></el-icon>
            </div>
            <div class="action-label">{{ action.label }}</div>
            <div class="action-desc">{{ action.desc }}</div>
          </button>
        </div>
      </div>
    </div>

    <!-- 系统监控 -->
    <div class="system-monitor brutal-card">
      <div class="monitor-header">
        <h3 class="monitor-title">
          <span class="monitor-icon">◉</span>
          SYSTEM MONITOR
        </h3>
        <div class="monitor-time mono-numbers">{{ currentTime }}</div>
      </div>
      <div class="monitor-grid">
        <div class="monitor-item">
          <div class="monitor-label">CPU</div>
          <div class="monitor-bar">
            <div class="monitor-fill" style="width: 35%"></div>
          </div>
          <div class="monitor-value mono-numbers">35%</div>
        </div>
        <div class="monitor-item">
          <div class="monitor-label">MEM</div>
          <div class="monitor-bar">
            <div class="monitor-fill" style="width: 62%"></div>
          </div>
          <div class="monitor-value mono-numbers">62%</div>
        </div>
        <div class="monitor-item">
          <div class="monitor-label">DISK</div>
          <div class="monitor-bar">
            <div class="monitor-fill" style="width: 78%"></div>
          </div>
          <div class="monitor-value mono-numbers">78%</div>
        </div>
        <div class="monitor-item">
          <div class="monitor-label">NET</div>
          <div class="monitor-bar">
            <div class="monitor-fill" style="width: 45%"></div>
          </div>
          <div class="monitor-value mono-numbers">45%</div>
        </div>
      </div>
      <div class="monitor-terminal">
        <div class="terminal-line">
          <span class="terminal-prompt">></span>
          <span class="terminal-text">SYSTEM_HEALTH: OPTIMAL</span>
        </div>
        <div class="terminal-line">
          <span class="terminal-prompt">></span>
          <span class="terminal-text">ALL_NODES: ONLINE</span>
        </div>
        <div class="terminal-line">
          <span class="terminal-prompt">></span>
          <span class="terminal-text">LAST_SYNC: {{ currentDate }}</span>
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
import {
  Top, Bottom
} from '@element-plus/icons-vue'

const router = useRouter()

// SVG Icons
const User = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }), h('circle', { cx: '12', cy: '7', r: '4' })]) })
const Upload = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4' }), h('polyline', { points: '17 8 12 3 7 8' }), h('line', { x1: '12', y1: '3', x2: '12', y2: '15' })]) })
const Timer = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('circle', { cx: '12', cy: '12', r: '10' }), h('polyline', { points: '12 6 12 12 16 14' })]) })
const DataAnalysis = shallowRef({ render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [h('path', { d: 'M3 3v18h18' }), h('path', { d: 'M18 17V9M13 17V5M8 17v-3' })]) })

// 时间显示
const currentTime = ref('')
const currentDate = ref('')
let timeInterval = null

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('zh-CN', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
  currentDate.value = now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

// 统计卡片
const statsCards = ref([
  { label: '账号总数', value: '12', unit: '', change: '+2', changeType: 'up', gradient: 'linear-gradient(135deg, #0071e3, #5e5ce6)', icon: User },
  { label: '资源总量', value: '128', unit: '个', change: '+15', changeType: 'up', gradient: 'linear-gradient(135deg, #34c759, #30d158)', icon: Upload },
  { label: '今日发布', value: '28', unit: '篇', change: '+12%', changeType: 'up', gradient: 'linear-gradient(135deg, #ff9500, #ff3b30)', icon: Timer },
  { label: '系统健康', value: '99', unit: '%', change: 'OPTIMAL', changeType: 'up', gradient: 'linear-gradient(135deg, #ccff00, #00ccff)', icon: DataAnalysis }
])

// 平台数据
const platforms = ref([
  { name: '抖音', emoji: '🎵', accounts: 2, todayPublish: 5, pending: 3, status: 'online', color: 'linear-gradient(135deg, #25F4EE, #FE2C55)' },
  { name: '快手', emoji: '📱', accounts: 1, todayPublish: 3, pending: 2, status: 'online', color: 'linear-gradient(135deg, #FF4906, #FFFFFF)' },
  { name: '小红书', emoji: '📕', accounts: 3, todayPublish: 8, pending: 5, status: 'online', color: 'linear-gradient(135deg, #FF2442, #000000)' },
  { name: '视频号', emoji: '🎬', accounts: 2, todayPublish: 4, pending: 1, status: 'online', color: 'linear-gradient(135deg, #07C160, #09BB07)' }
])

// 任务队列
const recentTasks = ref([
  { id: 1, title: '视频发布任务 #001', platform: '抖音', account: 'account_01', scheduledTime: '14:30', status: 'completed', statusText: '已完成', priority: 'high' },
  { id: 2, title: '批量上传任务', platform: '小红书', account: 'account_02', scheduledTime: '15:00', status: 'running', statusText: '进行中', priority: 'medium' },
  { id: 3, title: '定时发布任务', platform: '视频号', account: 'account_03', scheduledTime: '16:00', status: 'pending', statusText: '等待中', priority: 'low' },
  { id: 4, title: '封面生成任务', platform: '快手', account: 'account_01', scheduledTime: '17:30', status: 'pending', statusText: '等待中', priority: 'medium' }
])

// 快捷操作
const quickActions = [
  { label: '账号管理', desc: '添加/编辑平台账号', icon: User, gradient: 'linear-gradient(135deg, #0071e3, #5e5ce6)', action: () => router.push('/account-management') },
  { label: '素材上传', desc: '上传视频和图片', icon: Upload, gradient: 'linear-gradient(135deg, #34c759, #30d158)', action: () => router.push('/material-management') },
  { label: '发布中心', desc: '设置发布任务', icon: Timer, gradient: 'linear-gradient(135deg, #ff9500, #ff3b30)', action: () => router.push('/publish-center') },
  { label: '系统监控', desc: '查看运行状态', icon: DataAnalysis, gradient: 'linear-gradient(135deg, #ccff00, #00ccff)', action: () => ElMessage.info('监控模块启动中...') },
  { label: '素材库', desc: '管理媒体资源', icon: Upload, gradient: 'linear-gradient(135deg, #af52de, #ff2d55)', action: () => router.push('/material-management') },
  { label: '关于系统', desc: '查看版本信息', icon: DataAnalysis, gradient: 'linear-gradient(135deg, #5e5ce6, #0071e3)', action: () => router.push('/about') }
]

const getStatusType = (status) => {
  const map = { completed: 'success', running: 'warning', pending: 'info', failed: 'danger' }
  return map[status] || 'info'
}

const handleQuickAction = (action) => {
  if (action.action) {
    action.action()
  }
}

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timeInterval) clearInterval(timeInterval)
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.dashboard {
  max-width: 1600px;
  margin: 0 auto;
}

// ===== 统计卡片 =====
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-lg;
  margin-bottom: $spacing-xl;
}

.stat-card {
  animation: fade-in-up 0.6s ease-out forwards;
  animation-delay: var(--delay);
  opacity: 0;

  @keyframes fade-in-up {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
}

.stat-card-inner {
  position: relative;
  padding: $spacing-lg;
  overflow: hidden;
}

.stat-bg-glow {
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.15;
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
  border-radius: $radius-md;
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
  font-weight: 700;
  color: $text-primary;
  line-height: 1;
}

.value-unit {
  font-size: 14px;
  color: $text-tertiary;
}

.stat-label {
  font-size: 13px;
  color: $text-secondary;
  font-family: $font-mono;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-footer {
  position: relative;
  z-index: 1;
  margin-top: $spacing-md;
  padding-top: $spacing-sm;
  border-top: $border-light;
}

.stat-change {
  display: inline-flex;
  align-items: center;
  gap: $spacing-xs;
  font-size: 12px;
  font-family: $font-mono;
  font-weight: 600;
  text-transform: uppercase;

  &.up {
    color: $success-color;
  }

  &.down {
    color: $danger-color;
  }

  :deep(svg) {
    width: 12px;
    height: 12px;
  }
}

// ===== 主网格布局 =====
.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 0.8fr;
  gap: $spacing-lg;
  margin-bottom: $spacing-lg;
}

// ===== 面板样式 =====
.panel {
  background: transparent;
  border: none;

  &.brutal-card {
    background: $bg-card;
    border: $border-main;
    backdrop-filter: blur(20px);
  }
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-md $spacing-lg;
  border-bottom: $border-light;
}

.panel-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-family: $font-mono;
  font-size: 14px;
  font-weight: 700;
  color: $text-primary;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0;

  .panel-icon {
    color: $primary-color;
  }
}

.task-count {
  font-size: 12px;
  color: $primary-color;
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
  margin-bottom: $spacing-sm;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid transparent;
  border-radius: $radius-md;
  transition: all $transition-fast;

  &:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.1);
  }

  &:last-child {
    margin-bottom: 0;
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
  font-weight: 600;
  color: $text-primary;
}

.platform-accounts {
  font-size: 11px;
  color: $text-tertiary;
  font-family: $font-mono;
  text-transform: uppercase;
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
  font-weight: 700;
  color: $text-primary;
}

.stat-mini-label {
  font-size: 10px;
  color: $text-tertiary;
  font-family: $font-mono;
  text-transform: uppercase;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: $text-tertiary;

  &.online {
    background: $success-color;
    box-shadow: 0 0 10px rgba($success-color, 0.6);
  }
}

// ===== 任务列表 =====
.task-list {
  padding: $spacing-md;
  max-height: 300px;
  overflow-y: auto;
}

.task-item {
  display: flex;
  align-items: stretch;
  gap: $spacing-sm;
  padding: $spacing-sm;
  margin-bottom: $spacing-sm;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid transparent;
  border-radius: $radius-md;
  transition: all $transition-fast;

  &:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.1);
  }

  &.completed {
    opacity: 0.6;
  }

  &.running {
    border-color: rgba($warning-color, 0.3);

    .task-priority.high {
      background: $warning-color;
      animation: pulse 1.5s ease-in-out infinite;
    }
  }

  &.pending {
    border-color: rgba($info-color, 0.2);
  }
}

.task-priority {
  width: 3px;
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
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.task-header {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-bottom: $spacing-xs;
}

.task-title {
  font-size: 13px;
  font-weight: 500;
  color: $text-primary;
}

.task-meta {
  display: flex;
  gap: $spacing-md;
  font-size: 11px;
  color: $text-tertiary;
  font-family: $font-mono;
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
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid transparent;
  border-radius: $radius-md;
  cursor: pointer;
  transition: all $transition-normal;

  &:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);

    .action-icon {
      transform: scale(1.05);
    }
  }
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: $radius-md;
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
  font-size: 13px;
  font-weight: 600;
  color: $text-primary;
  margin-bottom: $spacing-xs;
}

.action-desc {
  font-size: 11px;
  color: $text-tertiary;
  font-family: $font-mono;
  text-transform: uppercase;
}

// ===== 系统监控 =====
.system-monitor {
  padding: $spacing-lg;
}

.monitor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
  padding-bottom: $spacing-md;
  border-bottom: $border-light;
}

.monitor-title {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  font-family: $font-mono;
  font-size: 14px;
  font-weight: 700;
  color: $text-primary;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0;

  .monitor-icon {
    color: $primary-color;
    animation: blink 2s ease-in-out infinite;
  }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.monitor-time {
  font-size: 14px;
  color: $primary-color;
}

.monitor-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: $spacing-lg;
  margin-bottom: $spacing-lg;
}

.monitor-item {
  display: flex;
  align-items: center;
  gap: $spacing-md;
}

.monitor-label {
  font-family: $font-mono;
  font-size: 12px;
  font-weight: 600;
  color: $text-secondary;
  width: 40px;
}

.monitor-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
}

.monitor-fill {
  height: 100%;
  background: linear-gradient(90deg, $primary-color, #00ccff);
  border-radius: 4px;
  transition: width $transition-slow;
}

.monitor-value {
  font-family: $font-mono;
  font-size: 12px;
  font-weight: 600;
  color: $text-primary;
  width: 36px;
  text-align: right;
}

.monitor-terminal {
  padding: $spacing-md;
  background: rgba(0, 0, 0, 0.3);
  border-radius: $radius-md;
  font-family: $font-mono;
}

.terminal-line {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  margin-bottom: $spacing-xs;

  &:last-child {
    margin-bottom: 0;
  }
}

.terminal-prompt {
  color: $primary-color;
  font-weight: 600;
}

.terminal-text {
  color: $text-secondary;
  font-size: 12px;
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

  .monitor-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
