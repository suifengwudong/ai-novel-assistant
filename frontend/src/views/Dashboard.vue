<template>
  <div class="dashboard-page" style="padding: 24px;">
    <n-h1 style="margin-bottom: 24px;">🎯 欢迎使用 AI 小说助手</n-h1>

    <n-grid :cols="3" x-gap="16" y-gap="16">
      <!-- 快速开始 -->
      <n-gi>
        <n-card title="🚀 快速开始" hoverable @click="$router.push('/projects')">
          <n-p>创建您的第一个小说项目，开始AI辅助创作之旅</n-p>
          <template #action>
            <n-button type="primary" @click.stop="$router.push('/projects')">开始创作</n-button>
          </template>
        </n-card>
      </n-gi>

      <!-- 项目统计 -->
      <n-gi>
        <n-card title="📊 项目统计">
          <n-statistic title="总项目数" :value="stats.totalProjects" />
          <n-statistic title="草稿项目" :value="stats.draftProjects" style="margin-top: 16px;" />
          <n-statistic title="已发布" :value="stats.publishedProjects" style="margin-top: 16px;" />
        </n-card>
      </n-gi>

      <!-- 最近活动 -->
      <n-gi>
        <n-card title="📝 最近活动">
          <n-empty v-if="recentProjects.length === 0" description="暂无项目" />
          <n-list v-else :bordered="false">
            <n-list-item v-for="project in recentProjects" :key="project.id">
              <n-thing :title="project.title" :description="project.updated_at?.slice(0, 10)">
                <template #action>
                  <n-tag :type="statusType(project.status)" size="small">{{ project.status }}</n-tag>
                </template>
              </n-thing>
            </n-list-item>
          </n-list>
        </n-card>
      </n-gi>

      <!-- 风格学习 -->
      <n-gi>
        <n-card title="🎨 风格学习" hoverable @click="$router.push('/style')">
          <n-p>分析优秀作品的写作风格，提升您的创作水平</n-p>
          <template #action>
            <n-button @click.stop="$router.push('/style')">开始学习</n-button>
          </template>
        </n-card>
      </n-gi>

      <!-- 智能润色 -->
      <n-gi>
        <n-card title="✏️ 智能润色" hoverable @click="$router.push('/polish')">
          <n-p>使用AI技术优化您的文稿，使其更加流畅优美</n-p>
          <template #action>
            <n-button @click.stop="$router.push('/polish')">开始润色</n-button>
          </template>
        </n-card>
      </n-gi>

      <!-- 角色管理 -->
      <n-gi>
        <n-card title="👥 角色管理" hoverable @click="$router.push('/characters')">
          <n-p>创建和管理小说中的角色，确保人物形象鲜明</n-p>
          <template #action>
            <n-button @click.stop="$router.push('/characters')">管理角色</n-button>
          </template>
        </n-card>
      </n-gi>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import { getProjects, type NovelProject } from '../api/projects'

const message = useMessage()
const stats = ref({
  totalProjects: 0,
  draftProjects: 0,
  publishedProjects: 0
})
const recentProjects = ref<NovelProject[]>([])

const statusType = (s: string) => ({ draft: 'default', published: 'success', archived: 'warning' }[s] as any || 'default')

const loadDashboard = async () => {
  try {
    const projects = await getProjects()
    stats.value = {
      totalProjects: projects.length,
      draftProjects: projects.filter(p => p.status === 'draft').length,
      publishedProjects: projects.filter(p => p.status === 'published').length
    }
    // 最近5个项目
    recentProjects.value = projects.slice(0, 5)
  } catch {
    message.error('加载数据失败')
  }
}

onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>
.dashboard-page {
  min-height: calc(100vh - 64px);
}
</style>