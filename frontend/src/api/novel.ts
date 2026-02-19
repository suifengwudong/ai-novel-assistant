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

// 流式生成请求参数
export interface GenerateRequest {
  prompt: string;
  system_message?: string;
  temperature?: number;
  max_tokens?: number;
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

/**
 * 流式生成文本（打字机效果）
 * 使用 fetch + ReadableStream 消费 Server-Sent Events
 *
 * @param request   生成请求参数
 * @param onChunk   每收到一个文本片段时的回调
 * @returns         Promise，生成完成后 resolve
 */
export const generateStream = (
  request: GenerateRequest,
  onChunk: (text: string) => void
): Promise<void> => {
  return new Promise((resolve, reject) => {
    fetch('/api/v1/agent/generate/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    })
      .then(async (response) => {
        if (!response.ok) {
          const err = await response.text();
          return reject(new Error(`HTTP ${response.status}: ${err}`));
        }
        const reader = response.body!.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() ?? '';

          for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const payload = line.slice(6).trim();
            if (payload === '[DONE]') {
              resolve();
              return;
            }
            try {
              const parsed = JSON.parse(payload) as { content?: string; error?: string };
              if (parsed.error) {
                return reject(new Error(parsed.error));
              }
              if (parsed.content) {
                onChunk(parsed.content);
              }
            } catch {
              // ignore malformed SSE lines
            }
          }
        }
        resolve();
      })
      .catch(reject);
  });
};