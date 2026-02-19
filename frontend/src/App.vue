<template>
  <n-config-provider :theme="theme">
    <n-message-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-loading-bar-provider>
            <div id="app">
              <n-layout style="height: 100vh">
                <!-- 侧边栏导航 -->
                <n-layout-sider
                  :collapsed="collapsed"
                  :collapsed-width="64"
                  :width="240"
                  show-trigger="bar"
                  @collapse="collapsed = true"
                  @expand="collapsed = false"
                >
                  <div class="sidebar-header">
                    <n-h3 v-if="!collapsed" style="margin: 0; color: white;">
                      🤖 AI小说助手
                    </n-h3>
                    <n-icon v-else size="32" color="white">
                      <RobotIcon />
                    </n-icon>
                  </div>

                  <n-menu
                    :collapsed="collapsed"
                    :collapsed-icon-size="22"
                    :options="menuOptions"
                    :value="activeKey"
                    @update:value="handleMenuUpdate"
                  />
                </n-layout-sider>

                <!-- 主内容区 -->
                <n-layout>
                  <n-layout-header style="padding: 0 24px;">
                    <div class="header-content">
                      <n-space align="center">
                        <n-button text @click="collapsed = !collapsed">
                          <template #icon>
                            <n-icon>
                              <MenuIcon />
                            </n-icon>
                          </template>
                        </n-button>
                        <n-breadcrumb>
                          <n-breadcrumb-item>
                            {{ currentRouteTitle }}
                          </n-breadcrumb-item>
                        </n-breadcrumb>
                      </n-space>

                      <n-space align="center">
                        <n-button text @click="toggleTheme">
                          <template #icon>
                            <n-icon>
                              <component :is="theme === lightTheme ? DarkIcon : LightIcon" />
                            </n-icon>
                          </template>
                        </n-button>
                      </n-space>
                    </div>
                  </n-layout-header>

                  <n-layout-content style="padding: 0;">
                    <router-view />
                  </n-layout-content>
                </n-layout>
              </n-layout>
            </div>
          </n-loading-bar-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { darkTheme, lightTheme } from 'naive-ui'
import {
  Menu as RobotIcon,
  Menu as MenuIcon,
  Sunny as LightIcon,
  Moon as DarkIcon
} from '@vicons/ionicons5'

const router = useRouter()
const route = useRoute()

const collapsed = ref(false)
const theme = ref(lightTheme)
const activeKey = ref('workspace')

// 菜单配置
const menuOptions = [
  {
    label: '✍️ 写作工作台',
    key: 'workspace',
    icon: () => h('span', { style: 'font-size: 18px' }, '✍️')
  },
  {
    label: '📁 项目管理',
    key: 'projects',
    icon: () => h('span', { style: 'font-size: 18px' }, '📁')
  },
  {
    label: '🎨 风格学习',
    key: 'style',
    icon: () => h('span', { style: 'font-size: 18px' }, '🎨')
  },
  {
    label: '✏️ 智能润色',
    key: 'polish',
    icon: () => h('span', { style: 'font-size: 18px' }, '✏️')
  },
  {
    label: '💬 读者反馈',
    key: 'feedback',
    icon: () => h('span', { style: 'font-size: 18px' }, '💭')
  },
  {
    label: '👤 角色卡片',
    key: 'characters',
    icon: () => h('span', { style: 'font-size: 18px' }, '🃏')
  },
  {
    label: '🌳 大纲树',
    key: 'plot-tree',
    icon: () => h('span', { style: 'font-size: 18px' }, '📋')
  }
]

// 当前路由标题
const currentRouteTitle = computed(() => {
  return route.meta.title as string || 'AI小说助手'
})

// 菜单点击处理
const handleMenuUpdate = (key: string) => {
  activeKey.value = key
  router.push(`/${key}`)
}

// 主题切换
const toggleTheme = () => {
  theme.value = theme.value === lightTheme ? darkTheme : lightTheme
}

// 根据路由路径更新激活菜单项
const updateActiveKey = () => {
  const path = route.path.replace(/^\//, '')
  // 编辑器路由归属于项目管理
  if (path.startsWith('projects/')) {
    activeKey.value = 'projects'
  } else {
    activeKey.value = path || 'workspace'
  }
}

// 初始化
onMounted(() => {
  updateActiveKey()
})

// 监听路由变化
watch(() => route.path, updateActiveKey)
</script>

<style scoped>
#app {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.sidebar-header {
  padding: 16px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

#app {
  height: 100vh;
}

/* Naive UI 自定义样式 */
.n-card {
  border-radius: 8px;
}

.n-button {
  border-radius: 6px;
}

.n-input {
  border-radius: 6px;
}
</style>