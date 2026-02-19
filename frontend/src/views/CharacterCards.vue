<template>
  <div class="character-cards-page">
    <n-card title="👤 角色卡片系统">
      <template #header-extra>
        <n-button type="primary" @click="showAddModal = true">
          + 新增角色
        </n-button>
      </template>

      <!-- 角色卡片网格 -->
      <n-grid x-gap="16" y-gap="16" :cols="3" responsive="screen" :item-responsive="true">
        <n-gi
          v-for="char in characters"
          :key="char.id"
          span="xs:12 s:6 m:4"
        >
          <n-card
            :title="char.name"
            hoverable
            class="character-card"
          >
            <template #header-extra>
              <n-space>
                <n-tag :type="getRoleTagType(char.role)" size="small">{{ char.role }}</n-tag>
                <n-button text size="tiny" @click="editCharacter(char)">编辑</n-button>
                <n-button text size="tiny" type="error" @click="deleteCharacter(char.id)">删除</n-button>
              </n-space>
            </template>

            <n-space vertical size="small">
              <div v-if="char.appearance">
                <n-text depth="3" style="font-size:12px">外貌</n-text>
                <n-text style="display:block; font-size:13px">{{ char.appearance }}</n-text>
              </div>
              <div v-if="char.personality">
                <n-text depth="3" style="font-size:12px">性格</n-text>
                <n-text style="display:block; font-size:13px">{{ char.personality }}</n-text>
              </div>
              <div v-if="char.speech_style">
                <n-text depth="3" style="font-size:12px">说话风格</n-text>
                <n-text style="display:block; font-size:13px">{{ char.speech_style }}</n-text>
              </div>
              <div v-if="char.background">
                <n-text depth="3" style="font-size:12px">背景</n-text>
                <n-text style="display:block; font-size:13px; white-space:pre-wrap">{{ char.background }}</n-text>
              </div>
              <div v-if="char.tags && char.tags.length">
                <n-space size="small" style="margin-top:4px">
                  <n-tag v-for="tag in char.tags" :key="tag" size="small" round>{{ tag }}</n-tag>
                </n-space>
              </div>
            </n-space>

            <template #action>
              <n-button
                text
                size="small"
                type="info"
                @click="copyContextPrompt(char)"
              >
                📋 复制 Prompt 片段
              </n-button>
            </template>
          </n-card>
        </n-gi>
      </n-grid>

      <n-empty v-if="characters.length === 0" description="暂无角色，点击「新增角色」创建" style="margin-top:60px" />
    </n-card>

    <!-- 新增/编辑角色 Modal -->
    <n-modal v-model:show="showAddModal" preset="card" :title="editingChar ? '编辑角色' : '新增角色'" style="width:560px">
      <n-form :model="formData" label-placement="left" label-width="80px">
        <n-form-item label="姓名" required>
          <n-input v-model:value="formData.name" placeholder="角色姓名" />
        </n-form-item>
        <n-form-item label="角色定位">
          <n-select
            v-model:value="formData.role"
            :options="roleOptions"
            placeholder="选择角色定位"
          />
        </n-form-item>
        <n-form-item label="外貌描述">
          <n-input v-model:value="formData.appearance" type="textarea" :rows="2" placeholder="描述外貌特征..." />
        </n-form-item>
        <n-form-item label="性格特点">
          <n-input v-model:value="formData.personality" type="textarea" :rows="2" placeholder="描述性格特点..." />
        </n-form-item>
        <n-form-item label="说话风格">
          <n-input v-model:value="formData.speech_style" placeholder="如：温柔、简短有力、喜欢反问..." />
        </n-form-item>
        <n-form-item label="人物背景">
          <n-input v-model:value="formData.background" type="textarea" :rows="3" placeholder="人物的背景故事..." />
        </n-form-item>
        <n-form-item label="标签">
          <n-dynamic-tags v-model:value="formData.tags" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space justify="end">
          <n-button @click="showAddModal = false">取消</n-button>
          <n-button type="primary" @click="saveCharacter">保存</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useMessage } from 'naive-ui';
import { useClipboard } from '@vueuse/core';

const message = useMessage();
const { copy } = useClipboard();

interface Character {
  id: string;
  name: string;
  role: string;
  appearance: string;
  personality: string;
  speech_style: string;
  background: string;
  tags: string[];
}

const characters = ref<Character[]>([]);
const showAddModal = ref(false);
const editingChar = ref<Character | null>(null);

const defaultForm = (): Character => ({
  id: '',
  name: '',
  role: 'protagonist',
  appearance: '',
  personality: '',
  speech_style: '',
  background: '',
  tags: [],
});

const formData = reactive<Character>(defaultForm());

const roleOptions = [
  { label: '主角', value: 'protagonist' },
  { label: '反派', value: 'antagonist' },
  { label: '配角', value: 'supporting' },
  { label: '路人', value: 'minor' },
];

const getRoleTagType = (role: string): 'success' | 'error' | 'warning' | 'default' => {
  const map: Record<string, 'success' | 'error' | 'warning' | 'default'> = {
    protagonist: 'success',
    antagonist: 'error',
    supporting: 'warning',
    minor: 'default',
  };
  return map[role] ?? 'default';
};

const editCharacter = (char: Character) => {
  editingChar.value = char;
  Object.assign(formData, { ...char });
  showAddModal.value = true;
};

const deleteCharacter = (id: string) => {
  characters.value = characters.value.filter(c => c.id !== id);
  message.success('角色已删除');
};

const saveCharacter = () => {
  if (!formData.name.trim()) {
    message.warning('请输入角色姓名');
    return;
  }
  if (editingChar.value) {
    const idx = characters.value.findIndex(c => c.id === editingChar.value!.id);
    if (idx !== -1) {
      characters.value[idx] = { ...formData };
    }
    message.success('角色已更新');
  } else {
    characters.value.push({ ...formData, id: `char_${Date.now()}` });
    message.success('角色已添加');
  }
  showAddModal.value = false;
  editingChar.value = null;
  Object.assign(formData, defaultForm());
};

const copyContextPrompt = (char: Character) => {
  const parts: string[] = [];
  parts.push(`【角色：${char.name}（${char.role}）】`);
  if (char.appearance) parts.push(`- 外貌：${char.appearance}`);
  if (char.personality) parts.push(`- 性格：${char.personality}`);
  if (char.speech_style) parts.push(`- 说话风格：${char.speech_style}`);
  if (char.background) parts.push(`- 背景：${char.background}`);
  copy(parts.join('\n'));
  message.success(`已复制「${char.name}」的 Prompt 片段`);
};
</script>

<style scoped>
.character-cards-page {
  padding: 24px;
}
.character-card {
  height: 100%;
}
</style>
