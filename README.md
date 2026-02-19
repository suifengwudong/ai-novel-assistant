# 🎨 AI Novel Assistant - 基于智能体的小说创作助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Vue 3](https://img.shields.io/badge/Vue-3.0+-brightgreen.svg)](https://vuejs.org)
[![Naive UI](https://img.shields.io/badge/Naive-UI-2.37+-blue.svg)](https://www.naiveui.com)

> 专为百万、千万字级超长篇小说创作设计的智能辅助系统，基于大语言模型和智能体技术，提供「内容管理+结构管理」双核心支撑。

## ✅ 项目状态

- **后端**: ✅ 完全可用 - FastAPI + SQLAlchemy + JWT认证
- **前端**: ✅ 完全可用 - Vue 3 + Naive UI + TypeScript
- **数据库**: ✅ SQLite (开发) / PostgreSQL (生产)
- **认证**: ✅ JWT令牌认证 + 路由守卫
- **依赖**: ✅ 所有依赖正确，无冲突
- **构建**: ✅ 前后端均可正常构建和运行

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

## 🚀 快速开始

### 方式一：一键启动完整系统（推荐）

```bash
# 克隆项目
git clone https://github.com/suifengwudong/ai-novel-assistant.git
cd ai-novel-assistant

# 配置环境变量（可选）
cp .env.example .env
# 编辑 .env，配置LLM API密钥等

# 一键启动前后端服务
# Windows:
test\start-all.bat
# Linux/Mac:
bash test/start-all.sh

# 访问系统
# 前端界面: http://localhost:3000
# API文档: http://localhost:8000/docs
# 健康检查: http://localhost:8000/health
```

### 方式二：手动启动服务

```bash
# 1. 启动后端
cd backend
pip install -r requirements.txt
python scripts/init_db.py
python main.py

# 2. 启动前端（新终端）
cd frontend
npm install
npm run dev
```

### 方式三：Docker部署

```bash
# 构建并启动服务
docker-compose up --build

# 或者使用生产模式
docker-compose -f docker-compose.prod.yml up --build
```

```bash
# 仅启动前端
test/start-frontend.bat

# 后端需要单独启动
cd backend && python main.py
```

详细部署文档：[docs/deployment.md](docs/deployment.md)

---

## 📋 使用指南

### 首次使用

1. **启动系统**
   ```bash
   # 一键启动
   test/start-all.bat
   ```

2. **访问系统**
   - 前端界面: http://localhost:3000
   - API文档: http://localhost:8000/docs

3. **注册账户**
   - 点击右上角注册按钮
   - 填写用户名、邮箱和密码
   - 注册成功后登录

### 核心功能

#### 📊 仪表板
- 查看项目统计信息
- 快速访问各项功能
- 显示最近活动项目

#### 📁 项目管理
- **创建项目**: 点击"新建项目"按钮
- **编辑项目**: 点击项目卡片上的"编辑"按钮
- **导出项目**: 支持Markdown、PDF、EPUB格式
- **状态管理**: 草稿/已发布/已归档

#### 🎨 风格学习
- 上传优秀作品样本
- AI自动分析写作风格
- 生成风格画像和建议

#### ✏️ 智能润色
- 输入待润色文本
- AI提供优化建议
- 支持多风格润色

#### 👥 角色管理
- 创建角色卡片
- 管理人物设定
- 角色关系图谱

#### 🌳 大纲树
- 可视化小说结构
- 章节层级管理
- 情节发展规划

### API使用

系统提供完整的REST API：

```bash
# 用户认证
POST /api/v1/auth/register  # 注册
POST /api/v1/auth/login     # 登录
GET  /api/v1/auth/me        # 获取用户信息

# 项目管理
GET    /api/v1/projects     # 获取项目列表
POST   /api/v1/projects     # 创建项目
PUT    /api/v1/projects/:id # 更新项目
DELETE /api/v1/projects/:id # 删除项目

# 导出功能
POST /api/v1/export/projects/:id/:format  # 导出项目
```

---

## 🛠️ 开发工具

### 代码质量工具
- **后端**: `black` (格式化), `isort` (导入排序), `flake8` (代码检查)
- **前端**: `ESLint` (代码检查), `Prettier` (格式化)
- **测试**: `pytest` + `pytest-asyncio` (异步测试支持)

### 自动化任务
项目配置了完整的 VS Code 任务系统，支持：
- 🔍 代码检查和格式化
- 🏗️ 构建和测试
- 🚀 开发服务器启动
- 📦 Docker 镜像构建

### CI/CD 流水线
- **GitHub Actions**: 自动化代码检查、测试和构建
- **分支保护**: `main` 和 `develop` 分支的代码质量把关
- **多环境支持**: 本地开发和生产部署

---

## �📖 系统架构

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
