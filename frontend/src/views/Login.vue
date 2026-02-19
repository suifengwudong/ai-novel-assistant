<template>
  <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <n-card title="登录" style="width: 380px;">
      <n-form :model="form" label-placement="left" label-width="80px">
        <n-form-item label="用户名">
          <n-input v-model:value="form.username" placeholder="请输入用户名" @keydown.enter="handleLogin" />
        </n-form-item>
        <n-form-item label="密码">
          <n-input v-model:value="form.password" type="password" placeholder="请输入密码" @keydown.enter="handleLogin" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space vertical style="width: 100%;">
          <n-button type="primary" block :loading="loading" @click="handleLogin">登录</n-button>
          <n-button text block @click="router.push('/register')">没有账号？立即注册</n-button>
        </n-space>
      </template>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const message = useMessage()
const authStore = useAuthStore()
const loading = ref(false)
const form = ref({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    return message.warning('请输入用户名和密码')
  }
  loading.value = true
  try {
    await authStore.login(form.value.username, form.value.password)
    message.success('登录成功')
    router.push('/projects')
  } catch {
    message.error('用户名或密码错误')
  } finally {
    loading.value = false
  }
}
</script>
