<template>
  <div class="plot-tree-page">
    <n-card title="🌳 交互式大纲树">
      <template #header-extra>
        <n-space>
          <n-button @click="showAddNodeModal = true">+ 添加节点</n-button>
          <n-button secondary @click="clearAll">清空</n-button>
        </n-space>
      </template>

      <n-grid x-gap="16" :cols="2">
        <!-- 左侧：树形结构 -->
        <n-gi>
          <n-card title="大纲结构" size="small" embedded :bordered="false">
            <n-tree
              v-if="treeData.length"
              :data="treeData"
              key-field="id"
              label-field="title"
              :render-label="renderLabel"
              block-line
              expand-on-click
              :default-expanded-keys="allNodeIds"
            />
            <n-empty v-else description="暂无大纲，点击「添加节点」创建第一个节点" style="margin-top:40px" />
          </n-card>
        </n-gi>

        <!-- 右侧：节点详情 -->
        <n-gi>
          <n-card title="节点详情" size="small" embedded :bordered="false">
            <div v-if="selectedNode">
              <n-descriptions column="1" label-placement="left" bordered size="small">
                <n-descriptions-item label="标题">{{ selectedNode.title }}</n-descriptions-item>
                <n-descriptions-item label="类型">
                  <n-tag :type="getNodeTypeTag(selectedNode.type)" size="small">{{ selectedNode.type }}</n-tag>
                </n-descriptions-item>
                <n-descriptions-item label="状态">
                  <n-tag :type="getStatusTag(selectedNode.status)" size="small">{{ getStatusLabel(selectedNode.status) }}</n-tag>
                </n-descriptions-item>
                <n-descriptions-item label="大纲描述">{{ selectedNode.description || '(暂无)' }}</n-descriptions-item>
                <n-descriptions-item label="涉及角色">
                  <n-space size="small">
                    <n-tag v-for="c in selectedNode.characters" :key="c" size="small">{{ c }}</n-tag>
                    <n-text v-if="!selectedNode.characters.length" depth="3">无</n-text>
                  </n-space>
                </n-descriptions-item>
                <n-descriptions-item label="埋下伏笔">
                  <n-space size="small" vertical>
                    <n-tag v-for="l in selectedNode.open_loops" :key="l" type="warning" size="small">{{ l }}</n-tag>
                    <n-text v-if="!selectedNode.open_loops.length" depth="3">无</n-text>
                  </n-space>
                </n-descriptions-item>
                <n-descriptions-item label="回收伏笔">
                  <n-space size="small" vertical>
                    <n-tag v-for="l in selectedNode.closed_loops" :key="l" type="success" size="small">{{ l }}</n-tag>
                    <n-text v-if="!selectedNode.closed_loops.length" depth="3">无</n-text>
                  </n-space>
                </n-descriptions-item>
                <n-descriptions-item label="偏离度">
                  <n-progress
                    type="line"
                    :percentage="Math.round(selectedNode.deviation_score * 100)"
                    :color="selectedNode.deviation_score > 0.5 ? '#f00' : '#18a058'"
                    style="width:200px"
                  />
                </n-descriptions-item>
              </n-descriptions>

              <n-divider dashed />

              <n-space>
                <n-button type="primary" size="small" @click="editNode(selectedNode)">编辑</n-button>
                <n-select
                  v-model:value="selectedNode.status"
                  :options="statusOptions"
                  size="small"
                  style="width:120px"
                  @update:value="(v) => updateNodeStatus(selectedNode!, v)"
                />
                <n-button type="error" size="small" @click="deleteNode(selectedNode.id)">删除</n-button>
              </n-space>
            </div>
            <n-empty v-else description="点击左侧节点查看详情" style="margin-top:60px" />
          </n-card>
        </n-gi>
      </n-grid>
    </n-card>

    <!-- 添加/编辑节点 Modal -->
    <n-modal v-model:show="showAddNodeModal" preset="card" :title="editingNode ? '编辑节点' : '添加大纲节点'" style="width:560px">
      <n-form :model="nodeForm" label-placement="left" label-width="80px">
        <n-form-item label="标题" required>
          <n-input v-model:value="nodeForm.title" placeholder="节点标题" />
        </n-form-item>
        <n-form-item label="类型">
          <n-select v-model:value="nodeForm.type" :options="typeOptions" />
        </n-form-item>
        <n-form-item label="父节点">
          <n-select
            v-model:value="nodeForm.parent_id"
            :options="parentOptions"
            clearable
            placeholder="顶级节点（不选则为根节点）"
          />
        </n-form-item>
        <n-form-item label="大纲描述">
          <n-input v-model:value="nodeForm.description" type="textarea" :rows="3" placeholder="此节点的情节大纲..." />
        </n-form-item>
        <n-form-item label="涉及角色">
          <n-dynamic-tags v-model:value="nodeForm.characters" />
        </n-form-item>
        <n-form-item label="埋下伏笔">
          <n-dynamic-tags v-model:value="nodeForm.open_loops" />
        </n-form-item>
        <n-form-item label="回收伏笔">
          <n-dynamic-tags v-model:value="nodeForm.closed_loops" />
        </n-form-item>
      </n-form>
      <template #action>
        <n-space justify="end">
          <n-button @click="showAddNodeModal = false">取消</n-button>
          <n-button type="primary" @click="saveNode">保存</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue';
import { useMessage } from 'naive-ui';
import type { TreeOption } from 'naive-ui';

const message = useMessage();

interface PlotNode {
  id: string;
  title: string;
  type: 'volume' | 'chapter' | 'scene';
  status: 'draft' | 'writing' | 'finished';
  description: string;
  characters: string[];
  open_loops: string[];
  closed_loops: string[];
  deviation_score: number;
  parent_id: string | null;
  children: PlotNode[];
}

const nodes = ref<PlotNode[]>([]);
const selectedNode = ref<PlotNode | null>(null);
const showAddNodeModal = ref(false);
const editingNode = ref<PlotNode | null>(null);

const defaultNodeForm = (): Omit<PlotNode, 'id' | 'children'> => ({
  title: '',
  type: 'chapter',
  status: 'draft',
  description: '',
  characters: [],
  open_loops: [],
  closed_loops: [],
  deviation_score: 0,
  parent_id: null,
});

const nodeForm = ref(defaultNodeForm());

const typeOptions = [
  { label: '卷 (Volume)', value: 'volume' },
  { label: '章 (Chapter)', value: 'chapter' },
  { label: '场景 (Scene)', value: 'scene' },
];

const statusOptions = [
  { label: '草稿', value: 'draft' },
  { label: '写作中', value: 'writing' },
  { label: '已完成', value: 'finished' },
];

const parentOptions = computed(() =>
  nodes.value.map(n => ({ label: n.title, value: n.id }))
);

const allNodeIds = computed(() => nodes.value.map(n => n.id));

// Build Naive UI tree data from flat node list
const treeData = computed<TreeOption[]>(() => {
  const map = new Map<string, PlotNode & { children: PlotNode[] }>();
  nodes.value.forEach(n => map.set(n.id, { ...n, children: [] }));

  const roots: PlotNode[] = [];
  nodes.value.forEach(n => {
    const node = map.get(n.id)!;
    if (n.parent_id && map.has(n.parent_id)) {
      map.get(n.parent_id)!.children.push(node);
    } else {
      roots.push(node);
    }
  });

  const toTreeOption = (n: PlotNode): TreeOption => ({
    key: n.id,
    label: n.title,
    children: (n.children && n.children.length) ? n.children.map(toTreeOption) : undefined,
    // extra data stored on the node itself
    _node: n,
  });

  return roots.map(toTreeOption);
});

const renderLabel = ({ option }: { option: TreeOption }) => {
  const node = (option as any)._node as PlotNode;
  const statusColor: Record<string, string> = {
    draft: '#999',
    writing: '#f0a020',
    finished: '#18a058',
  };
  return h('span', { style: 'display:flex;align-items:center;gap:6px;cursor:pointer', onClick: () => { selectedNode.value = node; } }, [
    h('span', null, option.label as string),
    h('span', { style: `font-size:10px;color:${statusColor[node.status]}` }, `[${getStatusLabel(node.status)}]`),
  ]);
};

const getNodeTypeTag = (type: string): 'info' | 'success' | 'warning' => {
  const map: Record<string, 'info' | 'success' | 'warning'> = { volume: 'info', chapter: 'success', scene: 'warning' };
  return map[type] ?? 'info';
};

const getStatusTag = (status: string): 'default' | 'warning' | 'success' => {
  const map: Record<string, 'default' | 'warning' | 'success'> = { draft: 'default', writing: 'warning', finished: 'success' };
  return map[status] ?? 'default';
};

const getStatusLabel = (status: string): string => {
  const map: Record<string, string> = { draft: '草稿', writing: '写作中', finished: '已完成' };
  return map[status] ?? status;
};

const editNode = (node: PlotNode) => {
  editingNode.value = node;
  nodeForm.value = { ...node };
  showAddNodeModal.value = true;
};

const deleteNode = (id: string) => {
  nodes.value = nodes.value.filter(n => n.id !== id);
  if (selectedNode.value?.id === id) selectedNode.value = null;
  message.success('节点已删除');
};

const updateNodeStatus = (node: PlotNode, status: string) => {
  node.status = status as PlotNode['status'];
  message.success(`状态已更新为：${getStatusLabel(status)}`);
};

const saveNode = () => {
  if (!nodeForm.value.title.trim()) {
    message.warning('请输入节点标题');
    return;
  }
  if (editingNode.value) {
    const idx = nodes.value.findIndex(n => n.id === editingNode.value!.id);
    if (idx !== -1) {
      nodes.value[idx] = { ...nodeForm.value as PlotNode, id: editingNode.value.id, children: [] };
    }
    message.success('节点已更新');
  } else {
    nodes.value.push({ ...nodeForm.value as PlotNode, id: `node_${Date.now()}`, children: [] });
    message.success('节点已添加');
  }
  showAddNodeModal.value = false;
  editingNode.value = null;
  nodeForm.value = defaultNodeForm();
};

const clearAll = () => {
  nodes.value = [];
  selectedNode.value = null;
  message.info('已清空所有节点');
};
</script>

<style scoped>
.plot-tree-page {
  padding: 24px;
}
</style>
