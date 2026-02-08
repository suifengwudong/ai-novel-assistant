@echo off
chcp 65001 >nul
title AI小说助手完整启动器

echo 🤖 AI小说助手完整启动器
echo =========================
echo.

echo 🔍 检查项目环境...
if not exist "backend" (
    echo ❌ backend 目录不存在
    pause
    exit /b 1
)
if not exist "frontend" (
    echo ❌ frontend 目录不存在
    pause
    exit /b 1
)
if not exist ".env" (
    echo ⚠️ .env 配置文件不存在，某些功能可能无法正常工作
    echo 请复制 .env.example 为 .env 并配置API密钥
    echo.
)

echo ✅ 项目结构完整
echo.

echo 🐍 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装，请先安装 Python 3.10+
    pause
    exit /b 1
)
echo ✅ Python 已安装
echo.

echo 📦 检查Python依赖...
if exist "backend\requirements.txt" (
    cd backend
    python -c "import fastapi, langgraph, litellm" >nul 2>&1
    if %errorlevel% neq 0 (
        echo ⚠️ Python依赖未完全安装，正在安装...
        pip install -r requirements.txt
        if %errorlevel% neq 0 (
            echo ❌ Python依赖安装失败
            cd ..
            pause
            exit /b 1
        )
        echo ✅ Python依赖安装完成
    ) else (
        echo ✅ Python依赖已安装
    )
    cd ..
) else (
    echo ❌ requirements.txt 不存在
    pause
    exit /b 1
)
echo.

echo 🌐 检查Node.js环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装，请先安装 Node.js 18+
    pause
    exit /b 1
)
echo ✅ Node.js 已安装

yarn --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ yarn 未安装，请先安装 yarn
    pause
    exit /b 1
)
echo ✅ yarn 已安装
echo.

echo 🎨 检查前端依赖...
cd frontend
if not exist "node_modules" (
    echo 📦 安装前端依赖...
    yarn install
    if %errorlevel% neq 0 (
        echo ❌ 前端依赖安装失败
        cd ..
        pause
        exit /b 1
    )
    echo ✅ 前端依赖安装完成
) else (
    echo ✅ 前端依赖已安装
)
cd ..
echo.

echo 🗄️ 初始化数据库...
cd backend
if exist "scripts\init_db.py" (
    echo 📊 初始化数据库...
    python scripts\init_db.py
    if %errorlevel% neq 0 (
        echo ⚠️ 数据库初始化失败，但将继续启动服务
    ) else (
        echo ✅ 数据库初始化完成
    )
) else (
    echo ⚠️ init_db.py 脚本不存在，跳过数据库初始化
)
cd ..
echo.

echo 🚀 启动后端服务...
echo 后端API地址: http://localhost:8000
echo API文档地址: http://localhost:8000/docs
echo.
start "AI小说助手-后端" cmd /k "cd backend && python main.py"

echo ⏳ 等待后端服务启动...
timeout /t 3 /nobreak >nul

echo 🚀 启动前端服务...
echo 前端访问地址: http://localhost:3000
echo 后端API代理: http://localhost:8000/api/v1
echo.
start "AI小说助手-前端" cmd /k "cd frontend && yarn dev"

echo.
echo 🎉 AI小说助手启动完成！
echo.
echo 📱 前端界面: http://localhost:3000
echo 🔗 后端API: http://localhost:8000
echo 📚 API文档: http://localhost:8000/docs
echo.
echo 按任意键关闭所有服务...
pause >nul

echo 🛑 正在关闭服务...
taskkill /fi "WINDOWTITLE eq AI小说助手-后端*" /t /f >nul 2>&1
taskkill /fi "WINDOWTITLE eq AI小说助手-前端*" /t /f >nul 2>&1
echo ✅ 服务已关闭
echo.
pause