<template>
  <div class="home-container">
    <el-tabs v-model="activeTab" type="border-card" class="main-tabs">
      <!-- 第一页：小志总数据 -->
      <el-tab-pane name="analysis">
        <template #label>
          <span class="tab-label">
            <span class="tab-icon">📊</span>
            小志总数据
          </span>
        </template>
        <ExcelAnalysis />
      </el-tab-pane>

      <!-- 第二页：小志标签数据 -->
      <el-tab-pane name="label">
        <template #label>
          <span class="tab-label">
            <span class="tab-icon">🏷️</span>
            小志标签数据
          </span>
        </template>
        <LabelProcess />
      </el-tab-pane>

      <!-- 第三页：SQL 查询 -->
      <el-tab-pane name="sql">
        <template #label>
          <span class="tab-label">
            <span class="tab-icon">🔍</span>
            SQL 查询
          </span>
        </template>
        <SqlQuery />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ExcelAnalysis from '@/components/ExcelAnalysis.vue'
import LabelProcess from '@/components/LabelProcess.vue'
import SqlQuery from '@/components/SqlQuery.vue'

const activeTab = ref('analysis')
</script>

<style scoped>
.home-container {
  max-width: 1400px;
  margin: 0 auto;
}

.main-tabs {
  min-height: calc(100vh - 118px);
  border-radius: 16px;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
}

.tab-icon {
  font-size: 16px;
}

:deep(.el-tabs__item) {
  height: 50px;
  line-height: 50px;
  padding: 0 24px;
}

:deep(.el-tabs__nav-wrap::after) {
  display: none;
}

:deep(.el-tabs__active-bar) {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  height: 3px;
  border-radius: 3px;
}
</style>
