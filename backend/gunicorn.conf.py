# Gunicorn 配置文件
# 用于生产环境运行 Flask 应用

import multiprocessing

# 绑定地址和端口
bind = "127.0.0.1:5000"

# 工作进程数（推荐 CPU 核心数 * 2 + 1）
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 超时时间（秒）
timeout = 120

# 保持连接时间
keepalive = 5

# 最大请求数，超过后重启 worker（防止内存泄漏）
max_requests = 1000
max_requests_jitter = 50

# 日志配置
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# 进程名称
proc_name = "xiaozhi-backend"

# 守护进程模式（由 Supervisor 管理时设为 False）
daemon = False

# 预加载应用
preload_app = True
