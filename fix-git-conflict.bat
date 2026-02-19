@echo off
chcp 65001 >nul
echo 🔄 解决Git Push冲突...

cd f:\Uni\s\2025_4寒\Projects\ai-novel-assistant

echo 📥 步骤1: 拉取远程更改...
git pull origin main

if %errorlevel% neq 0 (
    echo ❌ 拉取失败，检查是否有冲突需要解决
    echo 请手动解决冲突后运行: git push origin main:main
    pause
    exit /b 1
)

echo ✅ 拉取成功

echo 📤 步骤2: 推送更改...
git push origin main:main

if %errorlevel% neq 0 (
    echo ❌ 推送失败
    echo 可能仍有冲突，请检查git status
    pause
    exit /b 1
)

echo ✅ 推送成功！
echo 🎉 Git冲突已解决
pause