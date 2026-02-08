@echo off
chcp 65001 >nul
title AI小说助手前端启动器

echo 🤖 AI小说助手启动器
echo ====================
echo.

REM 检查Node.js是否安装
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装，请先安装 Node.js 18+
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

REM 检查npm是否安装
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm 未安装，请先安装 npm
    pause
    exit /b 1
)

echo ✅ Node.js 版本: 
node -v
echo ✅ npm 版本: 
npm -v
echo.

REM 进入前端目录
cd frontend

REM 检查依赖是否已安装
if not exist "node_modules" (
    echo 📦 正在安装前端依赖...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
) else (
    echo ✅ 依赖已安装
)
echo.

REM 启动开发服务器
echo 🚀 启动前端开发服务器...
echo 📱 前端访问地址: http://localhost:3000
echo 🔗 后端API代理: http://localhost:8000/api/v1
echo.
echo 按 Ctrl+C 停止服务器
echo.

npm run dev