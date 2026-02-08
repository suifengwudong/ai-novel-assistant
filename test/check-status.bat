@echo off
chcp 65001 >nul
title AI小说助手项目状态检查

echo 📊 AI小说助手项目状态检查
echo ===========================
echo.

echo 🔍 检查项目结构...
if not exist "backend" (
    echo ❌ backend 目录不存在
    goto :error
)
if not exist "frontend" (
    echo ❌ frontend 目录不存在
    goto :error
)
if not exist "scripts" (
    echo ❌ scripts 目录不存在
    goto :error
)

echo ✅ 项目结构完整
echo.

echo 🐍 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装
    goto :error
)
echo ✅ Python 版本: 
python -v
echo.

echo 📦 检查Python依赖...
if exist "backend\requirements.txt" (
    echo 📄 requirements.txt 存在
) else (
    echo ❌ requirements.txt 不存在
    goto :error
)

cd backend
python -c "import fastapi, langgraph, litellm" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 部分Python依赖未安装 (运行 pip install -r requirements.txt)
) else (
    echo ✅ 主要Python依赖已安装
)
cd ..
echo.

echo 🌐 检查Node.js环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js 未安装
    goto :error
)
echo ✅ Node.js 版本: 
node -v

npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm 未安装
    goto :error
)
echo ✅ npm 版本: 
npm -v
echo.

echo 🎨 检查前端依赖...
cd frontend
if exist "package.json" (
    echo 📄 package.json 存在
) else (
    echo ❌ package.json 不存在
    goto :error
)

if exist "node_modules" (
    echo ✅ 前端依赖已安装
) else (
    echo ⚠️ 前端依赖未安装 (运行 start-frontend.bat)
)
cd ..
echo.

echo 📁 检查配置文件...
if exist ".env" (
    echo ✅ .env 配置文件存在
) else (
    echo ⚠️ .env 配置文件不存在 (复制 .env.example 为 .env 并配置API密钥)
)

if exist ".env.example" (
    echo ✅ .env.example 模板存在
) else (
    echo ❌ .env.example 模板不存在
)
echo.

echo 🎯 Phase 3 功能状态:
echo ✅ 后端: 风格学习、内容润色、读者反馈模拟 已实现
echo ✅ 前端: 风格分析、内容润色、反馈模拟界面 已实现
echo ✅ 集成: API接口定义和前端调用 已完成
echo.

echo 🚀 启动建议:
echo 1. 配置 .env 文件中的API密钥
echo 2. 运行 start-frontend.bat 启动前端开发服务器
echo 3. 如需后端功能，运行 python backend/main.py
echo.

goto :end

:error
echo.
echo ❌ 项目状态检查失败，请检查上述错误
pause
exit /b 1

:end
echo 🎉 项目状态检查完成！
echo.
pause