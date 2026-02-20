<template>
  <div class="workspace">
    <!-- 页面头部 -->
    <div class="workspace-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <n-icon size="32" class="title-icon">
              <BookIcon />
            </n-icon>
            写作工作台
          </h1>
          <p class="page-subtitle">开始您的创意写作之旅</p>
        </div>
        <div class="header-right">
          <n-space>
            <n-button type="primary" size="large" @click="createNewProject">
              <template #icon>
                <n-icon>
                  <PlusIcon />
                </n-icon>
              </template>
              新建项目
            </n-button>
            <n-button size="large" @click="openRecentProject">
              <template #icon>
                <n-icon>
                  <FolderIcon />
                </n-icon>
              </template>
              打开项目
            </n-button>
          </n-space>
        </div>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="workspace-content">
      <!-- 左侧主要区域 -->
      <div class="main-section">
        <!-- 快速操作区 -->
        <n-card class="action-card" title="🚀 快速开始" hoverable>
          <n-grid cols="1 s:2 m:3" responsive="screen" :x-gap="16" :y-gap="16">
            <n-grid-item>
              <div class="action-item primary" @click="createNewProject">
                <div class="action-icon">
                  <n-icon size="48" color="#18a058">
                    <PlusIcon />
                  </n-icon>
                </div>
                <div class="action-content">
                  <h3>新建小说</h3>
                  <p>从空白开始创作</p>
                </div>
              </div>
            </n-grid-item>

            <n-grid-item>
              <div class="action-item" @click="openRecentProject">
                <div class="action-icon">
                  <n-icon size="48" color="#2080f0">
                    <FolderIcon />
                  </n-icon>
                </div>
                <div class="action-content">
                  <h3>继续写作</h3>
                  <p>打开最近项目</p>
                </div>
              </div>
            </n-grid-item>

            <n-grid-item>
              <div class="action-item" @click="importProject">
                <div class="action-icon">
                  <n-icon size="48" color="#f0a020">
                    <UploadIcon />
                  </n-icon>
                </div>
                <div class="action-content">
                  <h3>导入项目</h3>
                  <p>从文件导入</p>
                </div>
              </div>
            </n-grid-item>
          </n-grid>
        </n-card>

        <!-- 最近项目 -->
        <n-card class="projects-card" title="📂 最近项目" hoverable>
          <n-empty v-if="recentProjects.length === 0" description="暂无最近项目">
            <template #icon>
              <n-icon size="64" color="#cccccc">
                <FolderIcon />
              </n-icon>
            </template>
          </n-empty>
          <div v-else class="projects-list">
            <div
              v-for="project in recentProjects"
              :key="project.id"
              class="project-item"
              @click="openProject(project)"
            >
              <div class="project-icon">
                <n-icon size="32" color="#2080f0">
                  <DocumentIcon />
                </n-icon>
              </div>
              <div class="project-info">
                <h4>{{ project.title }}</h4>
                <p>{{ project.lastModified }}</p>
                <small>{{ project.genre }}</small>
              </div>
              <div class="project-actions">
                <n-button text size="small" @click.stop="openProject(project)">
                  打开
                </n-button>
              </div>
            </div>
          </div>
        </n-card>
      </div>

      <!-- 右侧边栏 -->
      <div class="sidebar-section">
        <!-- 写作统计 -->
        <n-card class="stats-card" title="📊 写作统计" hoverable>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-icon">
                <n-icon size="32" color="#18a058">
                  <DocumentIcon />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ formatNumber(stats.totalWords) }}</div>
                <div class="stat-label">总字数</div>
              </div>
            </div>

            <div class="stat-item">
              <div class="stat-icon">
                <n-icon size="32" color="#2080f0">
                  <CalendarIcon />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ formatNumber(stats.todayWords) }}</div>
                <div class="stat-label">今日字数</div>
              </div>
            </div>

            <div class="stat-item">
              <div class="stat-icon">
                <n-icon size="32" color="#f0a020">
                  <TimeIcon />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stats.writingDays }}</div>
                <div class="stat-label">写作天数</div>
              </div>
            </div>

            <div class="stat-item">
              <div class="stat-icon">
                <n-icon size="32" color="#d03050">
                  <FolderIcon />
                </n-icon>
              </div>
              <div class="stat-content">
                <div class="stat-value">{{ stats.projectCount }}</div>
                <div class="stat-label">项目数量</div>
              </div>
            </div>
          </div>
        </n-card>

        <!-- 写作工具 -->
        <n-card class="tools-card" title="🛠️ 写作工具" hoverable>
          <div class="tools-grid">
            <div class="tool-item" @click="$router.push('/characters')">
              <div class="tool-icon">
                <n-icon size="36" color="#18a058">
                  <PeopleIcon />
                </n-icon>
              </div>
              <div class="tool-content">
                <h4>角色卡片</h4>
                <p>管理人物角色</p>
              </div>
            </div>

            <div class="tool-item" @click="$router.push('/plot-tree')">
              <div class="tool-icon">
                <n-icon size="36" color="#2080f0">
                  <TreeIcon />
                </n-icon>
              </div>
              <div class="tool-content">
                <h4>大纲树</h4>
                <p>构建故事结构</p>
              </div>
            </div>

            <div class="tool-item" @click="$router.push('/style')">
              <div class="tool-icon">
                <n-icon size="36" color="#f0a020">
                  <PaletteIcon />
                </n-icon>
              </div>
              <div class="tool-content">
                <h4>风格学习</h4>
                <p>分析写作风格</p>
              </div>
            </div>

            <div class="tool-item" @click="$router.push('/polish')">
              <div class="tool-icon">
                <n-icon size="36" color="#d03050">
                  <SparklesIcon />
                </n-icon>
              </div>
              <div class="tool-content">
                <h4>智能润色</h4>
                <p>优化文章内容</p>
              </div>
            </div>

            <div class="tool-item" @click="$router.push('/feedback')">
              <div class="tool-icon">
                <n-icon size="36" color="#9060f0">
                  <ChatIcon />
                </n-icon>
              </div>
              <div class="tool-content">
                <h4>读者反馈</h4>
                <p>收集读者意见</p>
              </div>
            </div>
          </div>
        </n-card>

        <!-- 写作提示 -->
        <n-card class="tips-card" title="💡 写作提示" hoverable>
          <div class="writing-tip">
            <n-icon size="24" color="#f0a020" class="tip-icon">
              <LightbulbIcon />
            </n-icon>
            <p>{{ currentTip }}</p>
          </div>
          <n-button text @click="nextTip" style="margin-top: 12px;">
            换一个提示
          </n-button>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProjects, type NovelProject } from '../api/projects'
import {
  Add as PlusIcon,
  FolderOpenOutline as FolderIcon,
  CloudUploadOutline as UploadIcon,
  PeopleOutline as PeopleIcon,
  GitBranchOutline as TreeIcon,
  ColorPaletteOutline as PaletteIcon,
  SparklesOutline as SparklesIcon,
  ChatbubbleOutline as ChatIcon,
  DocumentOutline as DocumentIcon,
  CalendarOutline as CalendarIcon,
  TimeOutline as TimeIcon,
  BookOutline as BookIcon,
  BulbOutline as LightbulbIcon
} from '@vicons/ionicons5'

const router = useRouter()

// 最近项目数据
const recentProjects = ref<NovelProject[]>([])

// 写作统计
const stats = ref({
  totalWords: 0,
  todayWords: 0,
  writingDays: 0,
  projectCount: 0
})

// 写作提示
const writingTips = [
  '写作就像冥想，你需要安静地倾听内心的声音。',
  '好的开头是成功的一半，但完美的开头往往需要多次修改。',
  '不要害怕修改，伟大的作品都是修改出来的。',
  '保持每日写作习惯，即使只有几百字也很重要。',
  '从生活中汲取灵感，观察周围的人和事。',
  '阅读是最好的写作老师，多读多写。',
  '给角色赋予真实的动机和情感。',
  '故事的冲突是推动情节发展的核心。'
]

const currentTip = ref(writingTips[0])
const currentTipIndex = ref(0)

// 格式化数字
const formatNumber = (num: number) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万'
  }
  return num.toString()
}

// 换一个提示
const nextTip = () => {
  currentTipIndex.value = (currentTipIndex.value + 1) % writingTips.length
  currentTip.value = writingTips[currentTipIndex.value]
}

// 新建项目
const createNewProject = () => {
  // TODO: 实现新建项目逻辑
  console.log('新建小说项目')
}

// 打开最近项目
const openRecentProject = () => {
  // TODO: 实现打开最近项目逻辑
  console.log('打开最近项目')
}

// 导入项目
const importProject = () => {
  // TODO: 实现导入项目逻辑
  console.log('导入项目')
}

// 打开项目
const openProject = (project: NovelProject) => {
  router.push(`/projects/${project.id}/edit`)
}

onMounted(async () => {
  try {
    // 加载最近项目
    const projects = await getProjects()
    // 按更新时间排序，取最新的3个
    recentProjects.value = projects
      .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      .slice(0, 3)
      .map(project => ({
        ...project,
        lastModified: new Date(project.updated_at).toLocaleString('zh-CN')
      }))

    // 计算统计数据
    const allProjects = projects
    stats.value.projectCount = allProjects.length
    stats.value.totalWords = allProjects.reduce((sum, p) => sum + (p.word_count || 0), 0)

    // TODO: 计算今日字数和写作天数（需要后端API支持）
    stats.value.todayWords = 0
    stats.value.writingDays = 0
  } catch (error) {
    console.error('加载工作台数据失败:', error)
    // 出错时使用默认数据
    recentProjects.value = []
    stats.value = {
      totalWords: 0,
      todayWords: 0,
      writingDays: 0,
      projectCount: 0
    }
  }
})
</script>

<style scoped>
.workspace {
  padding: 24px;
  min-height: calc(100vh - 64px);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 页面头部 */
.workspace-header {
  margin-bottom: 32px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 32px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.header-left {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 8px 0;
}

.title-icon {
  color: #2080f0;
}

.page-subtitle {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.header-right {
  flex-shrink: 0;
}

/* 主要内容区 */
.workspace-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  min-height: calc(100vh - 200px);
}

.main-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.sidebar-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 卡片样式 */
.action-card,
.projects-card,
.stats-card,
.tools-card,
.tips-card {
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: none;
}

.action-card:hover,
.projects-card:hover,
.stats-card:hover,
.tools-card:hover,
.tips-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

/* 快速操作区 */
.action-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: white;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.action-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.action-item.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.action-item.primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

.action-icon {
  flex-shrink: 0;
}

.action-content h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
  font-weight: 600;
}

.action-content p {
  margin: 0;
  font-size: 14px;
  opacity: 0.8;
}

/* 项目列表 */
.projects-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.project-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e8e8e8;
}

.project-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border-color: #2080f0;
}

.project-icon {
  flex-shrink: 0;
}

.project-info {
  flex: 1;
}

.project-info h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.project-info p {
  margin: 0 0 4px 0;
  font-size: 14px;
  color: #666;
}

.project-info small {
  font-size: 12px;
  color: #999;
  background: #f0f0f0;
  padding: 2px 8px;
  border-radius: 12px;
}

.project-actions {
  flex-shrink: 0;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e8e8e8;
}

.stat-icon {
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin: 0;
}

/* 工具卡片 */
.tools-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
}

.tool-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e8e8e8;
}

.tool-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border-color: #2080f0;
}

.tool-icon {
  flex-shrink: 0;
}

.tool-content h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
}

.tool-content p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

/* 提示卡片 */
.writing-tip {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #fff8e1 0%, #fff3c4 100%);
  border-radius: 12px;
  border-left: 4px solid #f0a020;
}

.writing-tip p {
  margin: 0;
  font-size: 14px;
  color: #5d4e37;
  line-height: 1.5;
}

.tip-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .workspace-content {
    grid-template-columns: 1fr;
  }

  .header-content {
    flex-direction: column;
    gap: 24px;
    text-align: center;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .workspace {
    padding: 16px;
  }

  .header-content {
    padding: 24px 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .action-item,
  .project-item,
  .tool-item {
    padding: 16px;
  }

  .stat-item {
    padding: 12px;
  }
}
</style>