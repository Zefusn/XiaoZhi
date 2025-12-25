<template>
  <div class="home-container">
    <el-tabs v-model="activeTab" type="border-card" class="main-tabs">
      <!-- 第一页：Excel 数据分析 -->
      <el-tab-pane label="Excel 数据分析" name="analysis">
        <ExcelAnalysis />
      </el-tab-pane>

      <!-- 第二页：小志标签处理 -->
      <el-tab-pane label="小志标签处理" name="label">
        <LabelProcess />
      </el-tab-pane>

      <!-- 第三页：SQL 查询 -->
      <el-tab-pane label="SQL 查询" name="sql">
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
  min-height: calc(100vh - 120px);
}
</style>
