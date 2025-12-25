<template>
  <div class="sql-query">
    <el-alert
      title="提示"
      type="info"
      description="请先在 Excel 数据分析或小志标签处理页面加载数据，然后再执行 SQL 查询"
      :closable="false"
      class="mb-20"
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
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import api from '@/utils/request'

const sqlQuery = ref('')
const loading = ref(false)
const results = ref([])
const columns = ref([])
const tableRef = ref()
const selectedRows = ref([])

const executeQuery = async () => {
  if (!sqlQuery.value.trim()) {
    ElMessage.warning('请输入 SQL 查询语句')
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
  padding: 20px;
}

.result-section {
  margin-top: 20px;
}

.result-section h3 {
  margin-bottom: 15px;
  color: #303133;
}

.mb-10 {
  margin-bottom: 10px;
}

.mb-20 {
  margin-bottom: 20px;
}

.mt-10 {
  margin-top: 10px;
}
</style>
