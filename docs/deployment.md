# 📦 本地部署指南

## 方式一：Docker部署（推荐）

### 1. 安装Docker
- Windows/Mac: 下载 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Linux: `curl -fsSL https://get.docker.com | sh`

### 2. 克隆项目
```bash
git clone https://github.com/yourusername/ai-novel-assistant.git
cd ai-novel-assistant
```

### 3. 配置API密钥
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的大模型API密钥
```

### 4. 一键启动
```bash
bash scripts/deploy.sh
```

### 5. 访问系统
- 前端: http://localhost:3000
- API文档: http://localhost:8000/docs

---

## 方式二：手动部署

### 1. 安装Python 3.10+
```bash
python --version  # 确认版本 >= 3.10
```

### 2. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
export LLM_API_KEY="your_api_key_here"
export LLM_PROVIDER="openai"  # 或 anthropic / qwen
```

### 4. 初始化数据库
```bash
python scripts/init_db.py
```

### 5. 启动后端
```bash
python -m uvicorn main:app --reload
```

### 6. 启动前端
```bash
cd ../frontend
npm install
npm run dev
```

---

## 大模型配置

### 支持的模型

| 提供商 | 模型 | 配置示例 |
|--------|------|-------------|
| OpenAI | GPT-4 | `LLM_PROVIDER=openai` |
| Anthropic | Claude 3.5 | `LLM_PROVIDER=anthropic` |
| 阿里云 | 通义千问Max | `LLM_PROVIDER=qwen` |
| 本地 | Ollama | `LLM_PROVIDER=ollama` |

### 本地模型部署（无需API密钥）

```bash
# 1. 安装Ollama
curl https://ollama.ai/install.sh | sh

# 2. 下载模型
ollama pull qwen2.5:72b

# 3. 配置环境变量
export LLM_PROVIDER=ollama
export LLM_MODEL=qwen2.5:72b
```

---

## 常见问题

### Q: 端口被占用怎么办？
```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "8080:8000"  # 改为8080
```

### Q: 数据存储在哪里？
- Docker部署: `./data` 目录
- 手动部署: `~/.novel-assistant/data`

### Q: 如何备份数据？
```bash
# Docker部署
tar -czf backup.tar.gz ./data

# 手动部署
tar -czf backup.tar.gz ~/.novel-assistant/data
```

### Q: 如何查看日志？
```bash
# Docker部署
docker-compose logs -f backend

# 手动部署
tail -f ./logs/app.log
```

### Q: 如何更新项目？
```bash
git pull origin main
docker-compose build
docker-compose restart
```

---

## 系统要求

- Python 3.10+
- Docker 20.10+
- Docker Compose 1.29+
- 4GB+ RAM
- 10GB+ 硬盘空间

---

## 获取帮助

如有问题，请：
1. 查看 [FAQ](../docs/faq.md)
2. 提交 [Issue](https://github.com/yourusername/ai-novel-assistant/issues)
3. 加入 [讨论区](https://github.com/yourusername/ai-novel-assistant/discussions)
