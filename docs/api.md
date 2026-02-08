# 📖 API文档

## 基础信息

**基础URL**: `http://localhost:8000`

**API版本**: `v1`

---

## 健康检查

### GET /health

```bash
curl http://localhost:8000/health
```

**响应**:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "development"
}
```

---

## 内容生成 API

### POST /api/v1/generation/chapter

生成章节内容

**请求体**:
```json
{
  "outline": "第一章大纲内容",
  "previous_chapter_id": null,
  "style": "default",
  "word_count": 3000
}
```

**响应**:
```json
{
  "content": "生成的章节内容...",
  "word_count": 3000,
  "summary": "自动生成的总结..."
}
```

---

### POST /api/v1/generation/dialogue

生成对话内容

**请求体**:
```json
{
  "scene_description": "场景描述",
  "characters": ["角色1", "角色2"],
  "tone": "default"
}
```

**响应**:
```json
{
  "dialogue": "生成的对话内容"
}
```

---

## 知识库 API

### POST /api/v1/knowledge/add

添加知识条目

**请求体**:
```json
{
  "content": "知识内容",
  "type": "core",
  "category": "character",
  "locked": false
}
```

**响应**:
```json
{
  "id": 1,
  "content": "知识内容",
  "type": "core",
  "category": "character"
}
```

---

### GET /api/v1/knowledge/retrieve

检索上下文

**查询参数**:
- `query`: 查询文本
- `top_k`: 返回数量（默认10）

**响应**:
```json
{
  "results": [
    "检索结果1",
    "检索结果2"
  ]
}
```

---

## 总结管理 API

### POST /api/v1/management/summarize

生成总结

**请求体**:
```json
{
  "chapter_id": 1,
  "level": "chapter"
}
```

**响应**:
```json
{
  "summary": "总结内容",
  "level": "chapter",
  "timestamp": "2024-01-01T00:00:00"
}
```

---

## 校验 API

### POST /api/v1/validation/check

校验内容逻辑

**请求体**:
```json
{
  "content": "待校验的内容",
  "check_type": "logic"
}
```

**响应**:
```json
{
  "passed": true,
  "issues": [],
  "suggestions": []
}
```

---

## 错误处理

所有错误都返回标准格式：

```json
{
  "error": "错误描述",
  "status_code": 400,
  "details": "详细信息"
}
```

### 常见错误码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 身份验证

暂无身份验证要求（开发版本）

生产环境将支持JWT Token认证。

---

## 速率限制

暂无速率限制

生产环境可能会添加。

---

## WebSocket API

暂无WebSocket端点

未来计划支持流式更新。

---

## Swagger文档

完整的交互式API文档可访问：

```
http://localhost:8000/docs
```

Redoc文档：

```
http://localhost:8000/redoc
```
