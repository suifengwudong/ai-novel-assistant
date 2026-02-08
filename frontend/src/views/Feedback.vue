<template>
  <div class="feedback-page">
    <n-grid x-gap="24" :cols="12">
      <!-- 左侧内容区 -->
      <n-gi :span="7">
        <n-card title="📖 章节内容" style="height: 100%">
          <n-input
            v-model:value="content"
            type="textarea"
            :rows="25"
            placeholder="粘贴章节内容，测试读者反应..."
            style="font-size: 16px; line-height: 1.8;"
          />
          <template #action>
            <n-button type="info" block @click="handleSimulate" :loading="loading">
              召唤读者试毒
            </n-button>
          </template>
        </n-card>
      </n-gi>

      <!-- 右侧评论区 -->
      <n-gi :span="5">
        <n-card title="💬 读者反馈模拟" style="height: 100%">
          <n-tabs type="segment" animated>
            <n-tab-pane name="all" tab="全部反馈">
              <n-scrollbar style="max-height: 600px">
                <div v-if="hasFeedback">
                  <div v-for="(comments, type) in feedbackResult" :key="type" class="feedback-group">
                    <n-divider title-placement="left">
                      <n-tag :type="getTagType(type)" round size="small">
                        {{ getReaderName(type) }}
                      </n-tag>
                    </n-divider>
                    <n-list hoverable>
                      <n-list-item v-for="(comment, index) in comments" :key="index">
                        <template #prefix>
                          <n-avatar size="small" :src="getAvatar(type)" />
                        </template>
                        <n-thing :title="comment" content-style="margin-top: 0;">
                        </n-thing>
                      </n-list-item>
                    </n-list>
                  </div>
                </div>
                <n-empty v-else description="等待投喂内容..." style="margin-top: 50px" />
              </n-scrollbar>
            </n-tab-pane>
          </n-tabs>
        </n-card>
      </n-gi>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useMessage } from 'naive-ui';
import { simulateFeedback } from '../api/novel';

const message = useMessage();
const loading = ref(false);
const content = ref('');
const feedbackResult = ref<Record<string, string[]>>({});

const hasFeedback = computed(() => Object.keys(feedbackResult.value).length > 0);

const handleSimulate = async () => {
  if (!content.value) return;
  loading.value = true;
  try {
    // 默认模拟所有类型读者
    const types = ['casual', 'critical', 'lore', 'emotional'];
    feedbackResult.value = await simulateFeedback(content.value, types);
    message.success('读者反馈已生成');
  } catch (e) {
    message.error('模拟失败');
  } finally {
    loading.value = false;
  }
};

const getReaderName = (type: string) => {
  const map: Record<string, string> = {
    casual: '小白读者 (爽文党)',
    critical: '老白读者 (毒舌)',
    lore: '考据党 (列文虎克)',
    emotional: '情感党 (CP粉)'
  };
  return map[type] || type;
};

const getTagType = (type: string) => {
  const map: Record<string, any> = {
    casual: 'success',
    critical: 'error',
    lore: 'warning',
    emotional: 'info'
  };
  return map[type] || 'default';
};

const getAvatar = (type: string) => {
  // 这里可以使用随机头像API
  return `https://api.dicebear.com/7.x/adventurer/svg?seed=${type}`;
};
</script>

<style scoped>
.feedback-page {
  padding: 24px;
  height: calc(100vh - 64px);
}
.feedback-group {
  margin-bottom: 24px;
}
</style>