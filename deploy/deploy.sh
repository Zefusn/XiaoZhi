#!/bin/bash
# 宝塔面板部署脚本 - www.xz.luckymax.cn
# 在服务器上执行此脚本进行部署

# 配置变量
SITE_NAME="www.xz.luckymax.cn"
SITE_PATH="/www/wwwroot/${SITE_NAME}"
BACKEND_PATH="${SITE_PATH}/backend"
PYTHON_VERSION="3.9"  # 根据服务器实际情况调整

echo "=== 开始部署 ${SITE_NAME} ==="

# 1. 创建目录结构
echo "[1/6] 创建目录结构..."
mkdir -p ${SITE_PATH}/dist
mkdir -p ${BACKEND_PATH}
mkdir -p ${BACKEND_PATH}/uploads

# 2. 设置 Python 虚拟环境
echo "[2/6] 设置 Python 虚拟环境..."
cd ${BACKEND_PATH}
python${PYTHON_VERSION} -m venv venv
source venv/bin/activate

# 3. 安装 Python 依赖
echo "[3/6] 安装 Python 依赖..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 4. 设置目录权限
echo "[4/6] 设置目录权限..."
chown -R www:www ${SITE_PATH}
chmod -R 755 ${SITE_PATH}
chmod -R 777 ${BACKEND_PATH}/uploads

# 5. 创建 Supervisor 配置（用于管理 Flask 进程）
echo "[5/6] 创建 Supervisor 配置..."
cat > /etc/supervisor/conf.d/${SITE_NAME}.conf << EOF
[program:xiaozhi-backend]
directory=${BACKEND_PATH}
command=${BACKEND_PATH}/venv/bin/gunicorn -c gunicorn.conf.py app:app
user=www
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=${BACKEND_PATH}/logs/gunicorn.log
environment=PATH="${BACKEND_PATH}/venv/bin"
EOF

# 创建日志目录
mkdir -p ${BACKEND_PATH}/logs

# 6. 启动后端服务
echo "[6/6] 启动后端服务..."
supervisorctl reread
supervisorctl update
supervisorctl start xiaozhi-backend

echo "=== 部署完成 ==="
echo "前端文件请上传到: ${SITE_PATH}/dist/"
echo "后端文件请上传到: ${BACKEND_PATH}/"
echo "访问地址: https://${SITE_NAME}"
