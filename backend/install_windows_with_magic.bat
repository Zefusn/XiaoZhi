@echo off
echo ===================================
echo 小志数据 - Windows 专用安装脚本
echo ===================================
echo.

echo 检查 Python 环境...
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到 Python，请确保已安装 Python 并添加到系统路径
    pause
    exit /b 1
)

echo.
echo 检查 pip 版本...
python -m pip --version
if %errorlevel% neq 0 (
    echo 错误: 未找到 pip
    pause
    exit /b 1
)

echo.
echo 正在升级 pip...
python -m pip install --upgrade pip

echo.
echo 开始安装依赖...

echo 1/4. 安装 wheel
python -m pip install --upgrade wheel

echo 2/4. 安装 setuptools
python -m pip install --upgrade setuptools

echo 3/4. 安装基础依赖
python -m pip install Flask==2.3.3 flask-cors==4.0.0 Werkzeug==2.3.7

echo 4/4. 安装 Excel 处理依赖
python -m pip install openpyxl==3.1.2 xlrd==2.0.1

echo.
echo ===================================
echo 依赖安装完成！
echo ===================================
echo.

echo 提示：如果遇到问题，请重新启动应用程序

pause