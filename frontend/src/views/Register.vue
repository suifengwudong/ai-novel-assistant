<template>
  <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <n-card title="注册" style="width: 380px;">
      <n-form :model="form" label-placement="left" label-width="80px">
        <n-form-item label="用户名">
          <n-input v-model:value="form.username" placeholder="请输入用户名" />
        </n-form-item>
        <n-form-item label="邮箱">
          <n-input v-model:value="form.email" placeholder="请输入邮箱" />
        </n-form-item>
        <n-form-item label="密码">
          <n-input v-model:value="form.password" type="password" placeholder="请输入密码" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space vertical style="width: 100%;">
          <n-button type="primary" block :loading="loading" @click="handleRegister">注册</n-button>
          <n-button text block @click="router.push('/login')">已有账号？立即登录</n-button>
        </n-space>
      </template>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import axios from 'axios'

const router = useRouter()
const message = useMessage()
const loading = ref(false)
const form = ref({ username: '', email: '', password: '' })

const handleRegister = async () => {
  if (!form.value.username || !form.value.email || !form.value.password) {
    return message.warning('请填写所有字段')
  }
  loading.value = true
  try {
    await axios.post('/api/v1/auth/register', form.value)
    message.success('注册成功，请登录')
    router.push('/login')
  } catch (e: any) {
    message.error(e?.response?.data?.detail || '注册失败，用户名或邮箱已被使用，或服务异常')
  } finally {
    loading.value = false
  }
}
</script>
