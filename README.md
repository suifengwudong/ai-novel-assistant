# 🎨 AI Novel Assistant - 基于智能体的小说创作助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Vue 3](https://img.shields.io/badge/Vue-3.0+-brightgreen.svg)](https://vuejs.org)

> 专为百万、千万字级超长篇小说创作设计的智能辅助系统，基于大语言模型和智能体技术，提供「内容管理+结构管理」双核心支撑。

[English](#english) | [中文](#chinese)

---

## ✨ 核心特性

### 🧠 超长文本记忆系统
- **三级总结体系**：章节→卷册→全文，自动梳理百万字小说脉络
- **双层知识管理**：核心信息持久化存储 + 即时细节智能检索
- **断点续创**：精准理解上下文，保持故事连贯性

### 🎯 可控性优先设计
- **核心信息锁定**：重要设定不可被AI篡改
- **全程手动编辑**：所有AI生成内容均可修改
- **作者主导权**：系统仅辅助，决策权在作者

### 🤖 智能体编排
- **意图理解Agent**：精准解析模糊指令
- **内容生成Agent**：多风格、多场景适配
- **逻辑校验Agent**：自动检测设定矛盾、人设崩塌
- **优化迭代Agent**：持续改进生成质量

### 📚 全方位创作辅助
- 章节续写、对话生成、场景描写
- 人物设定管理、世界观知识库
- 大纲规划、节奏把控
- 文字润色、逻辑校验

---

## 🚀 快速开始

### 方式一：Docker 一键部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/suifengwudong/ai-novel-assistant.git
cd ai-novel-assistant

# 2. 配置API密钥
cp .env.example .env
# 编辑 .env，填入你的大模型API密钥

# 3. 启动服务
bash scripts/deploy.sh

# 4. 访问系统
# 前端: http://localhost:3000
# API文档: http://localhost:8000/docs
```

### 方式二：手动部署

```bash
# 后端
cd backend
pip install -r requirements.txt
python scripts/init_db.py
uvicorn main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

### 方式二：一键启动完整系统（推荐）

```bash
# 一键启动前后端服务
test/start-all.bat
```

**启动内容**:
- ✅ 自动环境检查
- ✅ 依赖自动安装
- ✅ 数据库初始化
- ✅ 后端API服务 (http://localhost:8000)
- ✅ 前端开发服务器 (http://localhost:3000)

### 方式三：分别启动服务

```bash
# 仅启动前端
test/start-frontend.bat

# 后端需要单独启动
cd backend && python main.py
```

详细部署文档：[docs/deployment.md](docs/deployment.md)

---

## 📖 系统架构

```
用户交互层 (Vue 3 + Electron)
         ↓
   API服务层 (FastAPI)
         ↓
智能体编排层 (LangGraph)
         ↓
┌────────┬────────┬────────┬────────┐
│ 长文本 │ 逻辑   │ 风格   │ 知识   │
│ 记忆   │ 校验   │ 学习   │ 管理   │
└────────┴────────┴────────┴────────┘
         ↓
数据存储层 (SQLite + Chroma + Redis)
         ↓
大模型接入层 (OpenAI/Claude/Qwen/Ollama)
```

详细架构文档：[docs/architecture.md](docs/architecture.md)

---

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Naive UI |
| 桌面端 | Electron |
| 后端 | Python 3.10+ + FastAPI |
| 智能体 | LangGraph |
| 向量数据库 | Chroma |
| 关系数据库 | SQLite / PostgreSQL |
| 缓存 | Redis |
| 大模型接入 | LiteLLM (支持多模型) |

---

## 📚 文档

- [部署指南](docs/deployment.md) - 详细的安装和部署步骤
- [开发文档](docs/development.md) - 二次开发指南
- [API文档](docs/api.md) - RESTful API接口说明
- [架构设计](docs/architecture.md) - 系统架构详解
- [贡献指南](CONTRIBUTING.md) - 如何参与项目

---

## 🎯 开发路线图

### ✅ Phase 1: MVP核心 (完成)
- [x] 基础架构搭建
- [x] 大模型接入
- [x] 三级总结系统
- [x] 章节生成功能

### ✅ Phase 2: 长文本突破 (已完成)
- [x] 向量检索系统
- [x] 知识图谱
- [x] 断点续创
- [x] 逻辑校验引擎

### 📋 Phase 3: 完整体验 (完成)
- [x] 内容+结构管理闭环
- [x] 风格学习适配
- [x] 润色优化功能
- [x] 读者反馈模拟

### 🚀 Phase 4: 优化和部署 (进行中)
- [x] 代码质量工具 (ESLint + Prettier + TypeScript)
- [x] 前端打包优化 (路由懒加载 + vendor代码分割)
- [x] Docker生产部署支持 (前端多阶段构建 + nginx)
- [x] CI/CD流水线 (GitHub Actions)
- [ ] 百万字级性能优化
- [ ] 多端同步
- [ ] 高级分析功能
- [ ] 插件系统

---

## 🤝 贡献

我们欢迎所有形式的贡献！

- 🐛 报告Bug：[提交Issue](https://github.com/suifengwudong/ai-novel-assistant/issues)
- 💡 功能建议：[讨论区](https://github.com/suifengwudong/ai-novel-assistant/discussions)
- 🔧 代码贡献：查看 [贡献指南](CONTRIBUTING.md)
- 📖 文档改进：直接提交PR

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

- ✅ 可自由使用、修改、分发
- ✅ 可用于商业用途
- ⚠️ 需保留原作者版权声明

---

## 🙏 致谢

感谢以下开源项目：
- [FastAPI](https://fastapi.tiangolo.com) - 现代化的Web框架
- [LangChain](https://www.langchain.com) - LLM应用开发框架
- [Chroma](https://www.trychroma.com) - 向量数据库
- [Vue.js](https://vuejs.org) - 渐进式前端框架

---

## 📧 联系方式

- GitHub Issues: [提问/反馈](https://github.com/suifengwudong/ai-novel-assistant/issues)
- Discussions: [社区讨论](https://github.com/suifengwudong/ai-novel-assistant/discussions)

---

## ⭐ Star History

如果这个项目对你有帮助，请给我们一个 Star ⭐️

[![Star History Chart](https://api.star-history.com/svg?repos=suifengwudong/ai-novel-assistant&type=Date)](https://star-history.com/#suifengwudong/ai-novel-assistant&Date)

---

<p align="center">Made with ❤️ for writers</p>
