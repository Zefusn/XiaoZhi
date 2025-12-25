<template>
  <div class="sql-query">
    <el-alert
      v-if="!hasData"
      title="请先加载数据"
      type="warning"
      description="请先在「Excel 数据分析」或「小志标签处理」页面点击查询/生成按钮加载数据，然后再返回此页面执行 SQL 查询"
      :closable="false"
      class="mb-20"
      show-icon
    />
    
    <el-alert
      v-else
      title="数据已加载"
      type="success"
      :description="`当前已加载 ${dataCount} 条数据，表名为: data`"
      :closable="false"
      class="mb-20"
      show-icon
    />

    <el-form label-width="100px">
      <el-form-item label="SQL 查询">
        <el-input
          v-model="sqlQuery"
          type="textarea"
          :rows="10"
          placeholder="请输入 SQL 查询语句，例如：SELECT question, COUNT(*) as count FROM data GROUP BY question ORDER BY count DESC"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="executeQuery" :loading="loading">
          执行查询
        </el-button>
        <el-button @click="clearQuery">清空</el-button>
      </el-form-item>
    </el-form>

    <el-divider />

    <div class="result-section" v-if="results.length > 0">
      <h3>查询结果</h3>
      <el-button type="default" size="small" @click="selectAll" class="mb-10">
        全选
      </el-button>
      <el-table
        ref="tableRef"
        :data="results"
        border
        stripe
        @selection-change="handleSelectionChange"
        max-height="500"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column
          v-for="(column, index) in columns"
          :key="index"
          :prop="column"
          :label="column"
          min-width="150"
        />
      </el-table>
      <el-button
        type="success"
        size="small"
        @click="copySelection"
        class="mt-10"
        :disabled="selectedRows.length === 0"
      >
        复制选中内容
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onActivated } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/request'

const sqlQuery = ref('')
const loading = ref(false)
const results = ref([])
const columns = ref([])
const tableRef = ref()
const selectedRows = ref([])
const hasData = ref(false)
const dataCount = ref(0)

// 检查数据状态
const checkDataStatus = async () => {
  try {
    const res = await api.get('/data-status')
    hasData.value = res.hasData
    dataCount.value = res.dataCount
  } catch (error) {
    hasData.value = false
    dataCount.value = 0
  }
}

// 组件挂载时检查数据状态
onMounted(() => {
  checkDataStatus()
})

// 组件激活时重新检查数据状态
onActivated(() => {
  checkDataStatus()
})

const executeQuery = async () => {
  if (!sqlQuery.value.trim()) {
    ElMessage.warning('请输入 SQL 查询语句')
    return
  }
  
  // 先检查数据状态
  await checkDataStatus()
  if (!hasData.value) {
    ElMessage.warning('没有可用的数据，请先在「Excel 数据分析」或「小志标签处理」页面加载数据')
    return
  }

  loading.value = true
  try {
    const res = await api.post('/sql-query', {
      query: sqlQuery.value
    })
    
    if (res.data && res.data.length > 0) {
      columns.value = Object.keys(res.data[0])
      results.value = res.data
      ElMessage.success('查询成功')
    } else {
      results.value = []
      columns.value = []
      ElMessage.info('查询结果为空')
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const clearQuery = () => {
  sqlQuery.value = ''
  results.value = []
  columns.value = []
}

const selectAll = () => {
  results.value.forEach(row => {
    tableRef.value.toggleRowSelection(row, true)
  })
}

const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

const copySelection = () => {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请先选择要复制的数据')
    return
  }
  
  const text = selectedRows.value
    .map(row => columns.value.map(col => row[col]).join('\t'))
    .join('\n')
  
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}
</script>

<style scoped>
.sql-query {
  padding: 8px;
}

.result-section {
  margin-top: 24px;
  padding: 20px;
  background: #fafbfc;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.result-section h3 {
  margin-bottom: 16px;
  color: #1f2937;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.result-section h3::before {
  content: '';
  width: 4px;
  height: 18px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 2px;
}

.mb-10 {
  margin-bottom: 12px;
}

.mb-20 {
  margin-bottom: 24px;
}

.mt-10 {
  margin-top: 12px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-textarea__inner) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  border-radius: 8px;
  padding: 12px;
}

:deep(.el-alert) {
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
}

:deep(.el-alert .el-alert__title) {
  color: #1e40af;
  font-weight: 600;
}

:deep(.el-alert .el-alert__description) {
  color: #3b82f6;
}

:deep(.el-button--success) {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
}

:deep(.el-button--success:hover) {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
}
</style>
