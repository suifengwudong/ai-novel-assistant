import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import { createDiscreteApi, darkTheme, lightTheme } from 'naive-ui'

import App from './App.vue'
import StyleAnalysis from './views/StyleAnalysis.vue'
import Polishing from './views/Polishing.vue'
import Feedback from './views/Feedback.vue'

import './style.css'

const { message, notification, dialog, loadingBar } = createDiscreteApi([
  'message',
  'dialog',
  'notification',
  'loadingBar'
])

// 路由配置
const routes = [
  { path: '/', redirect: '/style' },
  { path: '/style', component: StyleAnalysis, meta: { title: '风格学习' } },
  { path: '/polish', component: Polishing, meta: { title: '智能润色' } },
  { path: '/feedback', component: Feedback, meta: { title: '读者反馈' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} - AI小说助手`
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