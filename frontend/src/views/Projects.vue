<template>
  <div class="projects-page" style="padding: 24px;">
    <n-space justify="space-between" align="center" style="margin-bottom: 16px;">
      <n-h2 style="margin: 0;">📁 项目管理</n-h2>
      <n-button type="primary" @click="showCreate = true">新建项目</n-button>
    </n-space>

    <n-space style="margin-bottom: 16px;">
      <n-select
        v-model:value="statusFilter"
        :options="statusOptions"
        placeholder="筛选状态"
        clearable
        style="width: 160px;"
        @update:value="loadProjects"
      />
    </n-space>

    <n-spin :show="loading">
      <n-grid :cols="3" x-gap="16" y-gap="16">
        <n-gi v-for="project in projects" :key="project.id">
          <n-card
            :title="project.title"
            hoverable
            @click="selectedProject = project"
          >
            <template #header-extra>
              <n-tag :type="statusType(project.status)" size="small">{{ project.status }}</n-tag>
            </template>
            <n-text depth="3" style="display: block; margin-bottom: 8px;">
              {{ project.description || '暂无描述' }}
            </n-text>
            <n-text depth="3" style="font-size: 12px;">
              {{ project.genre ? `类型: ${project.genre}` : '' }}
              &nbsp;字数: {{ project.word_count }}
            </n-text>
            <template #action>
              <n-space>
                <n-button size="small" @click.stop="startEdit(project)">编辑</n-button>
                <n-button size="small" @click.stop="startExport(project)">导出</n-button>
                <n-button size="small" type="error" @click.stop="handleDelete(project.id)">删除</n-button>
              </n-space>
            </template>
          </n-card>
        </n-gi>
      </n-grid>
    </n-spin>

    <!-- 项目详情 -->
    <n-modal v-model:show="!!selectedProject" preset="card" style="width: 700px;" :title="selectedProject?.title">
      <n-descriptions v-if="selectedProject" :column="2" label-placement="left" bordered>
        <n-descriptions-item label="状态">
          <n-tag :type="statusType(selectedProject.status)">{{ selectedProject.status }}</n-tag>
        </n-descriptions-item>
        <n-descriptions-item label="类型">{{ selectedProject.genre || '-' }}</n-descriptions-item>
        <n-descriptions-item label="字数">{{ selectedProject.word_count }}</n-descriptions-item>
        <n-descriptions-item label="创建时间">{{ selectedProject.created_at?.slice(0, 10) }}</n-descriptions-item>
        <n-descriptions-item label="描述" :span="2">{{ selectedProject.description || '-' }}</n-descriptions-item>
      </n-descriptions>
      <n-input
        v-if="selectedProject"
        :value="selectedProject.content || ''"
        type="textarea"
        readonly
        :rows="10"
        style="margin-top: 16px;"
      />
    </n-modal>

    <!-- 新建项目 -->
    <n-modal v-model:show="showCreate" preset="card" title="新建项目" style="width: 560px;">
      <n-form :model="form" label-placement="left" label-width="80px">
        <n-form-item label="标题" required>
          <n-input v-model:value="form.title" placeholder="项目标题" />
        </n-form-item>
        <n-form-item label="描述">
          <n-input v-model:value="form.description" type="textarea" :rows="3" placeholder="项目描述" />
        </n-form-item>
        <n-form-item label="类型">
          <n-input v-model:value="form.genre" placeholder="如: 玄幻、言情" />
        </n-form-item>
        <n-form-item label="状态">
          <n-select v-model:value="form.status" :options="statusOptions.slice(1)" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space justify="end">
          <n-button @click="showCreate = false">取消</n-button>
          <n-button type="primary" :loading="saving" @click="handleCreate">创建</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 编辑项目 -->
    <n-modal v-model:show="showEdit" preset="card" title="编辑项目" style="width: 560px;">
      <n-form :model="editForm" label-placement="left" label-width="80px">
        <n-form-item label="标题" required>
          <n-input v-model:value="editForm.title" />
        </n-form-item>
        <n-form-item label="描述">
          <n-input v-model:value="editForm.description" type="textarea" :rows="3" />
        </n-form-item>
        <n-form-item label="类型">
          <n-input v-model:value="editForm.genre" />
        </n-form-item>
        <n-form-item label="状态">
          <n-select v-model:value="editForm.status" :options="statusOptions.slice(1)" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space justify="end">
          <n-button @click="showEdit = false">取消</n-button>
          <n-button type="primary" :loading="saving" @click="handleUpdate">保存</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 导出 -->
    <n-modal v-model:show="showExport" preset="card" title="导出项目" style="width: 400px;">
      <n-form-item label="格式">
        <n-select v-model:value="exportFormat" :options="exportOptions" />
      </n-form-item>
      <template #action>
        <n-space justify="end">
          <n-button @click="showExport = false">取消</n-button>
          <n-button type="primary" :loading="exporting" @click="handleExport">下载</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import {
  getProjects, createProject, updateProject, deleteProject, exportProject,
  type NovelProject, type ProjectCreate, type ProjectUpdate
} from '../api/projects'

const message = useMessage()
const loading = ref(false)
const saving = ref(false)
const exporting = ref(false)
const projects = ref<NovelProject[]>([])
const statusFilter = ref<string | null>(null)
const selectedProject = ref<NovelProject | null>(null)
const showCreate = ref(false)
const showEdit = ref(false)
const showExport = ref(false)
const exportProjectRef = ref<NovelProject | null>(null)
const exportFormat = ref<'markdown' | 'pdf' | 'epub'>('markdown')

const form = ref<ProjectCreate>({ title: '', description: '', genre: '', status: 'draft' })
const editForm = ref<ProjectUpdate & { id: string }>({ id: '', title: '', description: '', genre: '', status: 'draft' })

const statusOptions = [
  { label: '全部', value: null },
  { label: '草稿', value: 'draft' },
  { label: '已发布', value: 'published' },
  { label: '已归档', value: 'archived' },
]

const exportOptions = [
  { label: 'Markdown', value: 'markdown' },
  { label: 'PDF', value: 'pdf' },
  { label: 'EPUB', value: 'epub' },
]

const statusType = (s: string) => ({ draft: 'default', published: 'success', archived: 'warning' }[s] as any || 'default')

const loadProjects = async () => {
  loading.value = true
  try {
    projects.value = await getProjects(statusFilter.value || undefined)
  } catch {
    message.error('加载项目失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = async () => {
  if (!form.value.title) return message.warning('请输入标题')
  saving.value = true
  try {
    await createProject(form.value)
    showCreate.value = false
    form.value = { title: '', description: '', genre: '', status: 'draft' }
    await loadProjects()
    message.success('创建成功')
  } catch {
    message.error('创建失败')
  } finally {
    saving.value = false
  }
}

const startEdit = (p: NovelProject) => {
  editForm.value = { id: p.id, title: p.title, description: p.description, genre: p.genre, status: p.status }
  showEdit.value = true
}

const handleUpdate = async () => {
  saving.value = true
  try {
    const { id, ...body } = editForm.value
    await updateProject(id, body)
    showEdit.value = false
    await loadProjects()
    message.success('更新成功')
  } catch {
    message.error('更新失败')
  } finally {
    saving.value = false
  }
}

const handleDelete = async (id: string) => {
  try {
    await deleteProject(id)
    await loadProjects()
    message.success('已删除')
  } catch {
    message.error('删除失败')
  }
}

const startExport = (p: NovelProject) => {
  exportProjectRef.value = p
  showExport.value = true
}

const handleExport = async () => {
  if (!exportProjectRef.value) return
  exporting.value = true
  try {
    await exportProject(exportProjectRef.value.id, exportFormat.value, exportProjectRef.value.title)
    showExport.value = false
    message.success('导出成功')
  } catch (e: any) {
    message.error(e?.response?.data?.detail || '导出失败，请检查网络或所选格式的依赖库是否安装')
  } finally {
    exporting.value = false
  }
}

onMounted(loadProjects)
</script>
