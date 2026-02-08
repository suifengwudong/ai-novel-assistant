import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1', // 根据实际后端配置调整
  timeout: 60000
});

// 风格画像接口定义
export interface StyleProfile {
  id: string;
  name: string;
  lexical_features: string[];
  sentence_patterns: string[];
  rhetorical_devices: string[];
  tone: string;
}

// 风格学习
export const analyzeStyle = async (sampleText: string, styleName: string): Promise<StyleProfile> => {
  const { data } = await api.post<StyleProfile>('/style/analyze', {
    sample_text: sampleText,
    style_name: styleName
  });
  return data;
};

// 润色优化
export const polishContent = async (content: string, focus: string): Promise<string> => {
  const { data } = await api.post<{ result: string }>('/agent/polish', {
    content,
    focus
  });
  return data.result;
};

// 读者反馈
export const simulateFeedback = async (content: string, readerTypes: string[]): Promise<Record<string, string[]>> => {
  const { data } = await api.post<Record<string, string[]>>('/agent/feedback', {
    content,
    reader_types: readerTypes
  });
  return data;
};