<template>
  <div class="editor-page">
    <!-- 顶部工具栏 -->
    <div class="editor-toolbar">
      <div class="toolbar-left">
        <n-button text @click="goBack">
          <template #icon>
            <n-icon><ArrowBackIcon /></n-icon>
          </template>
          返回项目
        </n-button>
        <n-divider vertical />
        <n-input
          v-model:value="project.title"
          class="title-input"
          placeholder="项目标题"
          :bordered="false"
          @change="debouncedSave"
        />
        <n-tag v-if="saveStatus === 'saving'" type="warning" size="small" round>保存中...</n-tag>
        <n-tag v-else-if="saveStatus === 'saved'" type="success" size="small" round>已保存</n-tag>
        <n-tag v-else-if="saveStatus === 'error'" type="error" size="small" round>保存失败</n-tag>
      </div>
      <div class="toolbar-right">
        <n-space align="center">
          <n-text depth="3" style="font-size: 13px;">字数：{{ wordCount }}</n-text>
          <n-button size="small" @click="showAIPanel = !showAIPanel">
            <template #icon>
              <n-icon><SparklesIcon /></n-icon>
            </template>
            AI 助手
          </n-button>
          <n-select
            v-model:value="project.status"
            :options="statusOptions"
            size="small"
            style="width: 110px;"
            @update:value="debouncedSave"
          />
        </n-space>
      </div>
    </div>

    <!-- 主编辑区 -->
    <div class="editor-body" :class="{ 'with-ai-panel': showAIPanel }">
      <!-- 写作编辑器 -->
      <div class="writing-area">
        <n-spin :show="loading">
          <n-input
            v-model:value="project.content"
            type="textarea"
            class="main-editor"
            style="height: 100%;"
            placeholder="开始写作吧...

在这里输入您的小说内容，AI 助手随时待命。"
            :autosize="false"
            @input="onContentInput"
          />
        </n-spin>
      </div>

      <!-- AI 助手侧边栏 -->
      <div v-if="showAIPanel" class="ai-panel">
        <n-card title="🤖 AI 助手" size="small" class="ai-card">
          <n-tabs type="segment" size="small" animated>
            <!-- 智能润色 -->
            <n-tab-pane name="polish" tab="润色">
              <div class="ai-section">
                <n-radio-group v-model:value="polishFocus" size="small">
                  <n-radio-button value="general">综合</n-radio-button>
                  <n-radio-button value="descriptive">描写</n-radio-button>
                  <n-radio-button value="emotional">情感</n-radio-button>
                  <n-radio-button value="action">动作</n-radio-button>
                </n-radio-group>
                <n-input
                  v-model:value="selectedText"
                  type="textarea"
                  :rows="6"
                  placeholder="粘贴需要润色的段落..."
                  style="margin-top: 8px;"
                />
                <n-button
                  type="primary"
                  block
                  :loading="polishing"
                  style="margin-top: 8px;"
                  @click="handlePolish"
                >
                  开始润色
                </n-button>
                <div v-if="polishResult" class="ai-result">
                  <n-text depth="3" style="font-size: 12px;">润色结果：</n-text>
                  <n-input
                    :value="polishResult"
                    type="textarea"
                    :rows="8"
                    readonly
                    style="margin-top: 4px;"
                  />
                  <n-button
                    size="small"
                    block
                    style="margin-top: 6px;"
                    @click="copyPolishResult"
                  >
                    📋 复制结果
                  </n-button>
                </div>
              </div>
            </n-tab-pane>

            <!-- AI 续写 -->
            <n-tab-pane name="generate" tab="续写">
              <div class="ai-section">
                <n-text depth="3" style="font-size: 12px; display: block; margin-bottom: 8px;">
                  提示词（可选）：
                </n-text>
                <n-input
                  v-model:value="generatePrompt"
                  type="textarea"
                  :rows="4"
                  placeholder="描述接下来的情节走向，或留空让 AI 自由发挥..."
                />
                <n-button
                  type="primary"
                  block
                  :loading="generating"
                  style="margin-top: 8px;"
                  @click="handleGenerate"
                >
                  AI 续写
                </n-button>
                <div v-if="generatedText" class="ai-result">
                  <n-text depth="3" style="font-size: 12px;">续写内容：</n-text>
                  <n-input
                    :value="generatedText"
                    type="textarea"
                    :rows="10"
                    readonly
                    style="margin-top: 4px;"
                  />
                  <n-button
                    size="small"
                    type="success"
                    block
                    style="margin-top: 6px;"
                    @click="appendGenerated"
                  >
                    ✅ 插入到文档末尾
                  </n-button>
                </div>
              </div>
            </n-tab-pane>

            <!-- 读者反馈 -->
            <n-tab-pane name="feedback" tab="反馈">
              <div class="ai-section">
                <n-text depth="3" style="font-size: 12px; display: block; margin-bottom: 8px;">
                  选择要测试的段落：
                </n-text>
                <n-input
                  v-model:value="feedbackText"
                  type="textarea"
                  :rows="6"
                  placeholder="粘贴要获取反馈的段落..."
                />
                <n-button
                  type="primary"
                  block
                  :loading="loadingFeedback"
                  style="margin-top: 8px;"
                  @click="handleFeedback"
                >
                  召唤读者试毒
                </n-button>
                <div v-if="feedbackResult && Object.keys(feedbackResult).length" class="ai-result">
                  <div v-for="(comments, type) in feedbackResult" :key="type" style="margin-top: 8px;">
                    <n-tag :type="getTagType(type as string)" size="small" round>
                      {{ getReaderName(type as string) }}
                    </n-tag>
                    <ul style="margin: 4px 0 0 16px; padding: 0;">
                      <li v-for="(c, i) in comments" :key="i" style="font-size: 12px; margin-bottom: 4px;">{{ c }}</li>
                    </ul>
                  </div>
                </div>
              </div>
            </n-tab-pane>
          </n-tabs>
        </n-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useClipboard } from '@vueuse/core'
import {
  ArrowBackOutline as ArrowBackIcon,
  SparklesOutline as SparklesIcon,
} from '@vicons/ionicons5'
import { getProject, updateProject } from '../api/projects'
import { polishContent, simulateFeedback, generateStream } from '../api/novel'

const route = useRoute()
const router = useRouter()
const message = useMessage()
const { copy } = useClipboard()

const projectId = computed(() => route.params.id as string)
const loading = ref(true)
const saveStatus = ref<'idle' | 'saving' | 'saved' | 'error'>('idle')
const showAIPanel = ref(false)

const project = ref({
  id: '',
  title: '',
  content: '',
  status: 'draft' as 'draft' | 'published' | 'archived',
})

// Word count computed from content
const wordCount = computed(() => {
  const text = project.value.content || ''
  // Count Chinese characters + English words
  const chinese = (text.match(/[\u4e00-\u9fa5]/g) || []).length
  const english = (text.match(/\b[a-zA-Z]+\b/g) || []).length
  return chinese + english
})

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '已发布', value: 'published' },
  { label: '已归档', value: 'archived' },
]

// --- AI Panel state ---
const polishFocus = ref('general')
const selectedText = ref('')
const polishing = ref(false)
const polishResult = ref('')

const generating = ref(false)
const generatePrompt = ref('')
const generatedText = ref('')

const feedbackText = ref('')
const loadingFeedback = ref(false)
const feedbackResult = ref<Record<string, string[]>>({})

// --- Load project ---
onMounted(async () => {
  try {
    const data = await getProject(projectId.value)
    project.value = {
      id: data.id,
      title: data.title,
      content: data.content || '',
      status: data.status as 'draft' | 'published' | 'archived',
    }
  } catch {
    message.error('加载项目失败')
    router.push('/projects')
  } finally {
    loading.value = false
  }
})

// --- Auto-save with debounce ---
let saveTimer: ReturnType<typeof setTimeout> | null = null

const debouncedSave = () => {
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = setTimeout(saveProject, 1500)
}

const onContentInput = () => {
  debouncedSave()
}

const saveProject = async () => {
  saveStatus.value = 'saving'
  try {
    await updateProject(projectId.value, {
      title: project.value.title,
      content: project.value.content,
      status: project.value.status,
    })
    saveStatus.value = 'saved'
    setTimeout(() => {
      if (saveStatus.value === 'saved') saveStatus.value = 'idle'
    }, 3000)
  } catch {
    saveStatus.value = 'error'
    message.error('保存失败，请重试')
  }
}

onUnmounted(() => {
  if (saveTimer) clearTimeout(saveTimer)
})

// --- Navigation ---
const goBack = () => {
  if (saveTimer) {
    clearTimeout(saveTimer)
    saveProject().finally(() => router.push('/projects'))
  } else {
    router.push('/projects')
  }
}

// --- AI: Polish ---
const handlePolish = async () => {
  if (!selectedText.value.trim()) {
    message.warning('请输入需要润色的内容')
    return
  }
  polishing.value = true
  polishResult.value = ''
  try {
    polishResult.value = await polishContent(selectedText.value, polishFocus.value)
    message.success('润色完成')
  } catch {
    message.error('润色失败，请重试')
  } finally {
    polishing.value = false
  }
}

const copyPolishResult = () => {
  copy(polishResult.value)
  message.success('已复制到剪贴板')
}

// --- AI: Generate continuation ---
const handleGenerate = async () => {
  generating.value = true
  generatedText.value = ''

  // Build context: last 500 chars of content + user prompt
  const contextSnippet = (project.value.content || '').slice(-500)
  const systemMsg = '你是一位专业网络小说作者，请根据给定的上下文续写小说内容，保持风格连贯，每次续写约300字。'
  const prompt = contextSnippet
    ? `【上文末尾】\n${contextSnippet}\n\n【续写要求】${generatePrompt.value || '请自然地续写下一段情节'}`
    : generatePrompt.value || '请写一段引人入胜的小说开头'

  try {
    await generateStream(
      { prompt, system_message: systemMsg, max_tokens: 800 },
      (chunk) => { generatedText.value += chunk }
    )
    message.success('续写完成')
  } catch {
    message.error('续写失败，请重试')
  } finally {
    generating.value = false
  }
}

const appendGenerated = () => {
  if (!generatedText.value) return
  project.value.content = (project.value.content || '') + '\n\n' + generatedText.value
  generatedText.value = ''
  generatePrompt.value = ''
  debouncedSave()
  message.success('已插入到文档末尾')
}

// --- AI: Feedback ---
const handleFeedback = async () => {
  if (!feedbackText.value.trim()) {
    message.warning('请输入需要反馈的内容')
    return
  }
  loadingFeedback.value = true
  feedbackResult.value = {}
  try {
    feedbackResult.value = await simulateFeedback(
      feedbackText.value,
      ['casual', 'critical', 'lore', 'emotional']
    )
    message.success('读者反馈已生成')
  } catch {
    message.error('获取反馈失败')
  } finally {
    loadingFeedback.value = false
  }
}

const getReaderName = (type: string) => {
  const map: Record<string, string> = {
    casual: '小白读者',
    critical: '老白读者',
    lore: '考据党',
    emotional: '情感党',
  }
  return map[type] || type
}

const getTagType = (type: string): 'success' | 'error' | 'warning' | 'info' | 'default' => {
  const map: Record<string, 'success' | 'error' | 'warning' | 'info' | 'default'> = {
    casual: 'success',
    critical: 'error',
    lore: 'warning',
    emotional: 'info',
  }
  return map[type] ?? 'default'
}
</script>

<style scoped>
.editor-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px);
  background: #fafafa;
}

/* 顶部工具栏 */
.editor-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 16px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
  flex-shrink: 0;
  gap: 12px;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.toolbar-right {
  flex-shrink: 0;
}

.title-input {
  font-size: 18px;
  font-weight: 600;
  max-width: 400px;
}

/* 编辑区主体 */
.editor-body {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.writing-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 24px 48px;
}

.writing-area :deep(.n-spin-content) {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.main-editor {
  flex: 1;
  height: 100%;
  font-size: 17px;
  line-height: 2;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Georgia', serif;
}

.main-editor :deep(textarea) {
  height: 100% !important;
  resize: none;
  border: none;
  box-shadow: none;
  background: transparent;
  font-size: 17px;
  line-height: 2;
  font-family: 'PingFang SC', 'Microsoft YaHei', 'Georgia', serif;
  color: #1a1a1a;
}

.main-editor :deep(.n-input__border),
.main-editor :deep(.n-input__state-border) {
  display: none;
}

/* AI 侧边栏 */
.ai-panel {
  width: 340px;
  flex-shrink: 0;
  border-left: 1px solid #e8e8e8;
  background: white;
  overflow-y: auto;
}

.ai-card {
  border-radius: 0;
  border: none;
  height: 100%;
}

.ai-card :deep(.n-card__content) {
  padding: 8px 12px;
}

.ai-section {
  padding: 4px 0;
}

.ai-result {
  margin-top: 12px;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #e8e8e8;
}

/* With AI panel: narrow the writing area */
.editor-body.with-ai-panel .writing-area {
  padding: 24px 32px;
}

@media (max-width: 900px) {
  .editor-body.with-ai-panel {
    flex-direction: column;
  }
  .ai-panel {
    width: 100%;
    height: 300px;
    border-left: none;
    border-top: 1px solid #e8e8e8;
  }
  .writing-area {
    padding: 16px;
  }
}
</style>
