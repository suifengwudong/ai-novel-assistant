#!/bin/bash

# AI小说助手启动脚本

echo "🤖 AI小说助手启动器"
echo "===================="

# 检查Node.js是否安装
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装 Node.js 18+"
    exit 1
fi

# 检查npm是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装，请先安装 npm"
    exit 1
fi

echo "✅ Node.js 版本: $(node -v)"
echo "✅ npm 版本: $(npm -v)"

# 进入前端目录
cd frontend

# 检查依赖是否已安装
if [ ! -d "node_modules" ]; then
    echo "📦 正在安装前端依赖..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已安装"
fi

# 启动开发服务器
echo "🚀 启动前端开发服务器..."
echo "📱 前端访问地址: http://localhost:3000"
echo "🔗 后端API代理: http://localhost:8000/api/v1"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

npm run dev