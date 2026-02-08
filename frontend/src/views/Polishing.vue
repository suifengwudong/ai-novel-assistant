<template>
  <div class="polishing-page">
    <n-card title="✒️ 智能润色助手">
      <div class="toolbar">
        <n-space align="center">
          <n-text>润色侧重：</n-text>
          <n-radio-group v-model:value="focus" name="focusgroup">
            <n-radio-button value="general">综合优化</n-radio-button>
            <n-radio-button value="descriptive">画面描写</n-radio-button>
            <n-radio-button value="emotional">情感渲染</n-radio-button>
            <n-radio-button value="action">动作场面</n-radio-button>
          </n-radio-group>
          <n-button type="primary" :loading="loading" @click="handlePolish">
            开始润色
          </n-button>
        </n-space>
      </div>

      <n-grid x-gap="24" :cols="2" style="margin-top: 16px">
        <n-gi>
          <n-card title="原文" size="small">
            <n-input
              v-model:value="originalContent"
              type="textarea"
              :rows="20"
              placeholder="在此输入需要润色的段落..."
              class="content-area"
            />
          </n-card>
        </n-gi>
        <n-gi>
          <n-card title="润色结果" size="small">
             <n-input
              v-model:value="polishedContent"
              type="textarea"
              :rows="20"
              readonly
              placeholder="润色后的内容将显示在这里..."
              class="content-area"
              :class="{ 'highlight-change': polishedContent }"
            />
             <template #header-extra>
               <n-button text size="tiny" v-if="polishedContent" @click="copyResult">复制</n-button>
             </template>
          </n-card>
        </n-gi>
      </n-grid>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useMessage } from 'naive-ui';
import { polishContent } from '../api/novel';
import { useClipboard } from '@vueuse/core';

const message = useMessage();
const { copy } = useClipboard();

const loading = ref(false);
const focus = ref('general');
const originalContent = ref('');
const polishedContent = ref('');

const handlePolish = async () => {
  if (!originalContent.value) return;

  loading.value = true;
  try {
    polishedContent.value = await polishContent(originalContent.value, focus.value);
    message.success('润色完成');
  } catch (e) {
    message.error('服务请求失败');
  } finally {
    loading.value = false;
  }
};

const copyResult = () => {
  copy(polishedContent.value);
  message.success('已复制到剪贴板');
};
</script>

<style scoped>
.polishing-page {
  padding: 24px;
}
.toolbar {
  margin-bottom: 16px;
}
.content-area {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  line-height: 1.8;
  font-size: 16px;
}
</style>