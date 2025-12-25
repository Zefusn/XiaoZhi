# 小志数据 Web 应用

这是一个基于 Vue 3 + Flask 的 Web 应用，用于处理和分析 Excel 数据中的标签信息。

## 功能特性

### 1. 小志总数据
- 上传 Excel 文件进行数据分析
- 支持导入需去除的数据（根据 userContent 去除相同内容）
- 支持设备ID过滤（默认设备ID已预设）
- 支持安卓/iOS平台选择
- 显示总数据量、使用人数、指令次数等统计信息
- 新增指标：有图片无文字数量/无指令总数，初始数据列显示userContent为空且imageUrls不为空的数量，用户数据列显示directives为空的数量，显示在表格最底部

### 2. 小志标签数据
- 上传 Excel 文件进行标签分析
- 支持导入需去除的数据（根据 userContent 去除相同内容）
- 支持设备ID过滤（默认设备ID已预设）
- 支持平台选择
- 支持三种分析类型：
  - 默认分析：标签数低于10的统称为其他，数量为低于10的标签数量之和，并放置在表格末尾
  - 功能使用：仅展示 question 的值为 功能使用的 userContent 的内容，不展示数量
  - 低量标签：仅展示标签数小于10，大于等于5的标签名称，展示数量，并按数量逆序排序

### 3. SQL 查询
- 自定义 SQL 查询已加载的数据
- 动态显示查询结果
- 支持复杂的数据分析需求

## 技术栈

### 前端
- Vue 3
- Element Plus
- Vite
- Axios
- Vue Router

### 后端
- Flask
- Pandas
- SQLite
- Flask-CORS

## 项目结构

```
xiaozhi-web/
├── backend/                # 后端代码
│   ├── app.py             # Flask 应用主文件
│   └── requirements.txt   # Python 依赖
├── src/                   # 前端源代码
│   ├── components/        # Vue 组件
│   │   ├── ExcelAnalysis.vue
│   │   ├── LabelProcess.vue
│   │   └── SqlQuery.vue
│   ├── router/            # 路由配置
│   ├── utils/             # 工具函数
│   ├── views/             # 页面视图
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── index.html             # HTML 模板
├── package.json           # 项目配置
└── vite.config.js         # Vite 配置
```

## 安装和运行

### 前端安装

```bash
cd xiaozhi-web
npm install
```

### 后端安装

```bash
cd backend
pip install -r requirements.txt
```

### 运行项目

1. 启动后端服务：
```bash
cd backend
python app.py
```
后端将在 `http://localhost:5000` 运行

2. 启动前端开发服务器：
```bash
npm run dev
```
前端将在 `http://localhost:5173` 运行

## 使用说明

1. **小志总数据页面**
   - 点击"选择文件"按钮上传 Excel 文件
   - 输入需要过滤的设备ID（可选）
   - 选择数据类型和平台
   - 点击"查询"按钮查看分析结果
   - 可以全选并复制结果

2. **小志标签数据页面**
   - 上传 Excel 文件
   - 输入需要过滤的设备ID
   - 选择平台和分析类型
   - 点击"生成"按钮查看标签统计
   - 可以全选并复制结果

3. **SQL 查询页面**
   - 在前两个页面中加载数据后
   - 输入自定义 SQL 查询语句
   - 点击"执行查询"查看结果
   - 可以全选并复制结果

## Excel 文件格式要求

### 数据分析页面
需要包含以下字段：
- `deviceId`: 设备ID
- `pkgName`: 包名
- `directives`: 指令
- `avail`: 是否有帮助（值为 "有帮助" 或 "无帮助"）

### 标签处理页面
需要包含以下字段：
- `deviceId`: 设备ID
- `pkgName`: 包名
- `question`: 问题/标签名称

## 注意事项

- 上传文件大小限制为 16MB
- 支持 .xlsx, .xls, .xlsm, .xltx, .xltm 格式
- SQL 查询基于最后一次加载的数据
- 数据存储在内存中，刷新页面后需要重新加载

## 开发

### 构建生产版本

```bash
npm run build
```

构建后的文件将在 `dist` 目录中。

### 预览生产版本

```bash
npm run preview
```
