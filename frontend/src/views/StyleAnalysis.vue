<template>
  <div class="style-analysis-page">
    <n-card title="✨ 风格学习系统">
      <n-grid x-gap="12" :cols="2">
        <!-- 左侧：输入区 -->
        <n-gi>
          <n-form-item label="风格名称">
            <n-input v-model:value="styleName" placeholder="例如：赛博朋克风、鲁迅风" />
          </n-form-item>
          <n-form-item label="样章文本 (建议 2000 字以上)">
            <n-input
              v-model:value="sampleText"
              type="textarea"
              :rows="15"
              placeholder="请粘贴一段具有代表性的样章内容..."
            />
          </n-form-item>
          <n-button type="primary" :loading="loading" @click="handleAnalyze" block>
            开始分析风格
          </n-button>
        </n-gi>

        <!-- 右侧：分析结果 -->
        <n-gi>
          <n-card title="风格画像" embedded :bordered="false" v-if="result">
            <n-descriptions column="1" label-placement="left" bordered>
              <n-descriptions-item label="整体基调">
                <n-tag type="info">{{ result.tone }}</n-tag>
              </n-descriptions-item>
            </n-descriptions>

            <n-divider dashed>特征维度</n-divider>

            <div class="feature-group">
              <n-text strong>📚 用词特征</n-text>
              <n-space style="margin-top: 8px">
                <n-tag v-for="tag in result.lexical_features" :key="tag" type="success" size="small">
                  {{ tag }}
                </n-tag>
              </n-space>
            </div>

            <div class="feature-group" style="margin-top: 16px">
              <n-text strong>📝 句式习惯</n-text>
              <n-space style="margin-top: 8px">
                <n-tag v-for="tag in result.sentence_patterns" :key="tag" type="warning" size="small">
                  {{ tag }}
                </n-tag>
              </n-space>
            </div>

            <div class="feature-group" style="margin-top: 16px">
              <n-text strong>🎨 修辞手法</n-text>
              <n-space style="margin-top: 8px">
                <n-tag v-for="tag in result.rhetorical_devices" :key="tag" type="error" size="small">
                  {{ tag }}
                </n-tag>
              </n-space>
            </div>

            <template #action>
              <n-button secondary type="success" block>应用此风格到创作</n-button>
            </template>
          </n-card>

          <n-empty v-else description="暂无分析结果，请在左侧提交样章" class="empty-state" />
        </n-gi>
      </n-grid>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useMessage } from 'naive-ui';
import { analyzeStyle, type StyleProfile } from '../api/novel';

const message = useMessage();
const loading = ref(false);
const styleName = ref('');
const sampleText = ref('');
const result = ref<StyleProfile | null>(null);

const handleAnalyze = async () => {
  if (!styleName.value || !sampleText.value) {
    message.warning('请填写风格名称和样章内容');
    return;
  }

  loading.value = true;
  try {
    result.value = await analyzeStyle(sampleText.value, styleName.value);
    message.success('风格分析完成！');
  } catch (error) {
    message.error('分析失败，请重试');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.style-analysis-page {
  padding: 24px;
}
.empty-state {
  margin-top: 100px;
}
</style>