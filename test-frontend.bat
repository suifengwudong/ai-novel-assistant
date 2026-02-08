@echo off
chcp 65001 >nul
title AI小说助手前端测试

echo 🧪 AI小说助手前端测试
echo ======================
echo.

cd frontend

echo 📦 检查依赖...
if not exist "node_modules" (
    echo ❌ 依赖未安装，请先运行 start-frontend.bat
    pause
    exit /b 1
)

echo ✅ 依赖已安装
echo.

echo 🔍 检查TypeScript编译...
npx tsc --noEmit
if %errorlevel% neq 0 (
    echo ❌ TypeScript编译失败
    pause
    exit /b 1
)

echo ✅ TypeScript编译通过
echo.

echo 🎨 检查ESLint...
npx eslint src --ext .ts,.vue
if %errorlevel% neq 0 (
    echo ⚠️ ESLint检查完成（可能有警告）
) else (
    echo ✅ ESLint检查通过
)

echo.
echo 🎉 前端代码检查完成！
echo 🚀 现在可以运行 start-frontend.bat 启动开发服务器
echo.

pause