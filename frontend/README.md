# AI小说助手前端

基于 Vue 3 + TypeScript + Naive UI + Vite 构建的现代化小说创作助手前端应用。

## ✨ 功能特性

- **🎨 风格学习系统**: 分析样章文本，提取写作风格特征
- **✒️ 智能润色助手**: 支持多种润色模式，提升文本质量
- **💬 读者反馈模拟**: 模拟不同类型读者的评论和反馈
- **🎯 现代化UI**: 基于 Naive UI 的美观界面设计
- **📱 响应式布局**: 支持桌面端和移动端访问

## 🚀 快速开始

### 安装依赖

```bash
npm install
```

### 开发环境

```bash
npm run dev
```

访问 `http://localhost:3000` 查看应用。

### 构建生产版本

```bash
npm run build
```

### 代码检查

```bash
npm run lint
```

## 📁 项目结构

```
frontend/
├── src/
│   ├── api/           # API 接口封装
│   │   └── novel.ts   # 小说创作相关 API
│   ├── views/         # 页面组件
│   │   ├── StyleAnalysis.vue    # 风格学习页面
│   │   ├── Polishing.vue        # 润色优化页面
│   │   └── Feedback.vue         # 读者反馈页面
│   ├── App.vue        # 根组件
│   ├── main.ts        # 应用入口
│   └── style.css      # 全局样式
├── public/            # 静态资源
├── index.html         # HTML 模板
├── vite.config.ts     # Vite 配置
├── tsconfig.json      # TypeScript 配置
└── package.json       # 项目依赖
```

## 🔧 技术栈

- **Vue 3**: 渐进式 JavaScript 框架
- **TypeScript**: 类型安全的 JavaScript 超集
- **Naive UI**: Vue 3 的组件库
- **Vue Router**: 官方路由管理器
- **Pinia**: 状态管理库
- **Vite**: 下一代前端构建工具
- **Axios**: HTTP 客户端
- **@vueuse/core**: Vue 实用工具函数

## 🌐 浏览器支持

- Chrome >= 87
- Firefox >= 78
- Safari >= 14
- Edge >= 88

## 📝 开发指南

### 代码规范

- 使用 TypeScript 进行类型检查
- 遵循 Vue 3 Composition API 最佳实践
- 使用 ESLint 进行代码质量检查
- 组件命名使用 PascalCase
- 文件命名使用 kebab-case

### API 集成

后端 API 基础路径通过环境变量 `VITE_API_BASE_URL` 配置，默认代理到 `http://localhost:8000/api/v1`。

### 主题定制

应用支持亮色和暗色主题切换，可通过右上角按钮进行切换。

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](../LICENSE) 文件了解详情。