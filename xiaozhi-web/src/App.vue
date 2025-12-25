<template>
  <div id="app">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo-section">
            <span class="logo-icon">📊</span>
            <h1>小志标签处理</h1>
          </div>
          <div class="header-subtitle">数据分析工具</div>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #1f2937;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
}

.app-header {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 40px;
  height: 70px !important;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
  position: relative;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1400px;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 28px;
}

.app-header h1 {
  color: white;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 1px;
}

.header-subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  font-weight: 400;
}

.el-main {
  padding: 24px;
  min-height: calc(100vh - 70px);
}

/* 全局按钮样式优化 */
.el-button--primary {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border: none;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
  transition: all 0.3s ease;
}

.el-button--primary:hover {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

/* 全局表格样式优化 */
.el-table {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.el-table th.el-table__cell {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
  color: #475569;
  font-weight: 600;
}

/* 全局输入框样式优化 */
.el-input__wrapper {
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.el-input__wrapper:focus-within {
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* 全局卡片样式 */
.el-tabs--border-card {
  border: none;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.el-tabs__header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.el-tabs__item {
  font-weight: 500;
  transition: all 0.3s ease;
}

.el-tabs__item.is-active {
  color: #6366f1;
}

.el-tabs__content {
  padding: 24px;
  background: white;
}

/* 全局分割线 */
.el-divider {
  margin: 24px 0;
}

/* 上传组件样式 */
.el-upload-list__item {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.el-upload-list__item:hover {
  background: #f8fafc;
}
</style>
