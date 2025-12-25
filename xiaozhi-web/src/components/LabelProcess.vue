<template>
  <div class="label-process">
    <el-form :model="form" label-width="180px">
      <el-form-item label="选择 Excel 文件">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :limit="1"
          :on-change="handleFileChange"
          accept=".xlsx,.xls"
        >
          <el-button type="primary" :icon="Upload">选择文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              {{ fileName || '仅支持 .xlsx 和 .xls 文件' }}
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item label="需要去除的设备ID">
        <el-input
          v-model="form.deviceIds"
          placeholder="多个设备ID用逗号分隔，例如：device1,device2"
          clearable
        />
      </el-form-item>

      <el-form-item label="选择平台">
        <el-radio-group v-model="form.platform">
          <el-radio label="安卓">安卓</el-radio>
          <el-radio label="iOS">iOS</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="分析类型">
        <el-radio-group v-model="form.analysisType">
          <el-radio label="default">默认分析</el-radio>
          <el-radio label="function">功能使用</el-radio>
          <el-radio label="lowVolume">低量标签</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="generateResults" :loading="loading">
          生成
        </el-button>
      </el-form-item>
    </el-form>

    <el-divider />

    <div class="result-section" v-if="results.length > 0">
      <h3>分析结果</h3>
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
        <el-table-column prop="label" label="标签名称" min-width="200" />
        <el-table-column prop="count" label="数量" width="120" />
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
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import api from '@/utils/request'

const form = reactive({
  deviceIds: '',
  platform: '安卓',
  analysisType: 'default'
})

const uploadRef = ref()
const tableRef = ref()
const fileName = ref('')
const selectedFile = ref(null)
const loading = ref(false)
const results = ref([])
const selectedRows = ref([])

const handleFileChange = (file) => {
  selectedFile.value = file.raw
  fileName.value = file.name
}

const generateResults = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择 Excel 文件')
    return
  }

  if (!form.deviceIds) {
    ElMessage.warning('请输入需要去除的设备ID')
    return
  }

  loading.value = true
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  formData.append('deviceIds', form.deviceIds)
  formData.append('platform', form.platform)
  formData.append('analysisType', form.analysisType)

  try {
    const res = await api.post('/label-process', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    results.value = res.data
    ElMessage.success('生成完成')
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
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
    .map(row => `${row.label}\t${row.count}`)
    .join('\n')
  
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}
</script>

<style scoped>
.label-process {
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

.mt-10 {
  margin-top: 10px;
}
</style>
