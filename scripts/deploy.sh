#!/bin/bash

# AI Novel Assistant 一键部署脚本

set -e  # 遇到错误立即退出

echo "🚀 开始部署 AI Novel Assistant..."
echo ""

# 1. 检查Docker环境
echo "📦 检查Docker环境..."
if ! command -v docker &> /dev/null; then
    echo "❌ 未检测到Docker，请先安装Docker Desktop"
    echo "   下载地址: https://www.docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker未运行，请启动Docker Desktop"
    exit 1
fi

echo "✅ Docker环境正常"
echo ""

# 2. 配置环境变量
echo "⚙️  配置环境变量..."
if [ ! -f .env ]; then
    echo "📝 未检测到.env文件，开始配置..."
    cp .env.example .env
    
    echo ""
    echo "请选择大模型提供商:"
    echo "  1) OpenAI (GPT-4)"
    echo "  2) Anthropic (Claude)"
    echo "  3) 通义千问"
    echo "  4) Ollama (本地模型)"
    read -p "请输入选项 (1-4): " provider_choice
    
    case $provider_choice in
        1)
            sed -i 's/LLM_PROVIDER=openai/LLM_PROVIDER=openai/' .env
            read -p "请输入OpenAI API Key: " api_key
            sed -i "s/LLM_API_KEY=your_api_key_here/LLM_API_KEY=$api_key/" .env
            ;;
        2)
            sed -i 's/LLM_PROVIDER=openai/LLM_PROVIDER=anthropic/' .env
            sed -i 's/LLM_MODEL=gpt-4/LLM_MODEL=claude-3-sonnet-20240229/' .env
            read -p "请输入Anthropic API Key: " api_key
            sed -i "s/LLM_API_KEY=your_api_key_here/LLM_API_KEY=$api_key/" .env
            ;;
        3)
            sed -i 's/LLM_PROVIDER=openai/LLM_PROVIDER=qwen/' .env
            sed -i 's/LLM_MODEL=gpt-4/LLM_MODEL=qwen-max/' .env
            read -p "请输入通义千问 API Key: " api_key
            sed -i "s/LLM_API_KEY=your_api_key_here/LLM_API_KEY=$api_key/" .env
            ;;
        4)
            sed -i 's/LLM_PROVIDER=openai/LLM_PROVIDER=ollama/' .env
            sed -i 's/LLM_MODEL=gpt-4/LLM_MODEL=qwen2.5:72b/' .env
            sed -i 's|LLM_BASE_URL=|LLM_BASE_URL=http://host.docker.internal:11434|' .env
            echo "ℹ️  请确保Ollama已安装并运行: ollama serve"
            ;;
        *)
            echo "❌ 无效选项"
            exit 1
            ;;
    esac
    
    echo "✅ 环境变量配置完成"
else
    echo "✅ 检测到已有.env文件"
fi
echo ""

# 3. 构建并启动服务
echo "🔨 构建Docker镜像..."
docker-compose build

echo ""
echo "🚀 启动服务..."
docker-compose up -d

echo ""
echo "⏳ 等待服务就绪..."
sleep 10

echo ""
echo "🔍 检查服务状态..."
docker-compose ps

echo ""
echo "✅ 部署完成！"
echo ""
echo "📱 访问地址:"
echo "   - 前端: http://localhost:3000"
echo "   - API文档: http://localhost:8000/docs"
echo "   - 健康检查: http://localhost:8000/health"
echo ""
echo "📚 使用提示:"
echo "   - 查看日志: docker-compose logs -f"
echo "   - 停止服务: docker-compose down"
echo "   - 重启服务: docker-compose restart"
echo ""
