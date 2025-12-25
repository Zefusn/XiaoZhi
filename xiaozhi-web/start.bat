@echo off
echo ===================================
echo 小志标签数据 Web 应用启动脚本
echo ===================================
echo.

echo [1/3] 检查后端依赖...
cd backend
pip show flask >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装后端依赖...
    echo 提示: 如果安装失败，请运行 install_windows_with_magic.bat 脚本
    echo 或使用预编译的 wheel 文件安装
    call install_windows_with_magic.bat
) else (
    echo 后端依赖已安装
)

echo.
echo [2/3] 启动后端服务...
start cmd /k "cd /d %cd% && echo 启动 Flask 后端服务... && python app.py"

echo.
echo [3/3] 等待后端启动 (5秒)...
timeout /t 5 /nobreak >nul

cd ..
echo.
echo 检查前端依赖...
if not exist "node_modules" (
    echo 正在安装前端依赖，请稍候...
    call npm install
) else (
    echo 前端依赖已安装
)

echo.
echo 启动前端开发服务器...
start cmd /k "cd /d %cd% && echo 启动 Vue 前端服务... && npm run dev"

echo.
echo ===================================
echo 启动完成！
echo 后端地址: http://localhost:5000
echo 前端地址: http://localhost:5173
echo ===================================
echo.
echo 按任意键退出...
pause >nul
