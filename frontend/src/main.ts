import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import { createDiscreteApi } from 'naive-ui'

import App from './App.vue'

import './style.css'

const { message, notification, dialog, loadingBar } = createDiscreteApi([
  'message',
  'dialog',
  'notification',
  'loadingBar'
])

// 路由配置 — 使用懒加载，按需分包提升首屏速度
const routes = [
  { path: '/', redirect: '/projects' },
  { path: '/projects', component: () => import('./views/Projects.vue'), meta: { title: '项目管理' } },
  { path: '/login', component: () => import('./views/Login.vue'), meta: { title: '登录' } },
  { path: '/register', component: () => import('./views/Register.vue'), meta: { title: '注册' } },
  { path: '/style', component: () => import('./views/StyleAnalysis.vue'), meta: { title: '风格学习' } },
  { path: '/polish', component: () => import('./views/Polishing.vue'), meta: { title: '智能润色' } },
  { path: '/feedback', component: () => import('./views/Feedback.vue'), meta: { title: '读者反馈' } },
  { path: '/characters', component: () => import('./views/CharacterCards.vue'), meta: { title: '角色卡片' } },
  { path: '/plot-tree', component: () => import('./views/PlotTree.vue'), meta: { title: '大纲树' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - AI小说助手` : 'AI小说助手'
  next()
})

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(pinia)

// 全局提供 Naive UI 的离散 API
app.provide('message', message)
app.provide('notification', notification)
app.provide('dialog', dialog)
app.provide('loadingBar', loadingBar)

app.mount('#app')