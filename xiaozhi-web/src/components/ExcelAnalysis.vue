<template>
  <div class="excel-analysis">
    <el-form :model="form" label-width="180px">
      <el-form-item label="选择 Excel 文件">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :limit="1"
          :on-change="handleFileChange"
          accept=".xlsx,.xls,.xlsm,.xltx,.xltm"
        >
          <el-button type="primary" :icon="Upload">选择文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              {{ fileName || '仅支持 .xlsx, .xls, .xlsm, .xltx, .xltm 文件' }}
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item label="导入需去除的数据">
        <el-upload
          ref="filterUploadRef"
          :auto-upload="false"
          :limit="1"
          :on-change="handleFilterFileChange"
          accept=".xlsx,.xls,.xlsm,.xltx,.xltm"
        >
          <el-button type="primary" :icon="Upload">选择过滤文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              {{ filterFileName || '选择包含需要去除的 userContent 的 Excel 文件' }}
            </div>
          </template>
        </el-upload>
      </el-form-item>

      <el-form-item label="需要去除的设备ID">
        <el-input
          v-model="form.deviceIds"
          placeholder="多个设备ID用逗号分隔"
          clearable
        />
        <el-button @click="setDefaultDeviceIds" size="small" style="margin-top: 5px;">
          设置默认设备ID
        </el-button>
      </el-form-item>

      <el-form-item label="数据类型">
        <el-checkbox-group v-model="form.dataTypes">
          <el-checkbox label="initial">初始数据</el-checkbox>
          <el-checkbox label="user">用户数据</el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item label="选择平台">
        <el-radio-group v-model="form.platform">
          <el-radio label="安卓">安卓</el-radio>
          <el-radio label="iOS">iOS</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="analyzeData" :loading="loading">
          查询
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
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="metric" label="指标" width="200" />
        <el-table-column prop="initialData" label="初始数据" />
        <el-table-column prop="userData" label="用户数据" />
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
  deviceIds: 'ac44a75398c981f7,d05eae7f04ed5d52,a60a2ff1d9c3ccfb,0276ecb7a675de03,368b4f5495a5e564,f7f42dc48701c3b6,f7f42dc48701c3b6,6b148ea3088089ec,d1579a130a93aab9,e80d34b2ee6fc588,8ff0f2727c76ee81,cb00707bd8231384,22ccbb1f4183522b,22ccbb1f4183522b,f71400c874c7ae03,b053fed6f322070d,77ffb26dd8aec8d7,b19393e3fb39fed1,aa165cc58b7b69e1,066a1f89fe9e631a,766b3ef3f8f35119,c8cbd47c78e3adba,9fe81ff00522beff',
  dataTypes: ['initial', 'user'],
  platform: '安卓'
})

const uploadRef = ref()
const filterUploadRef = ref()
const tableRef = ref()
const fileName = ref('')
const filterFileName = ref('')
const selectedFile = ref(null)
const filterFile = ref(null)
const loading = ref(false)
const results = ref([])
const selectedRows = ref([])

const handleFileChange = (file) => {
  selectedFile.value = file.raw
  fileName.value = file.name
}

const handleFilterFileChange = (file) => {
  if (file) {
    filterFile.value = file.raw
    filterFileName.value = file.name
  }
}

const setDefaultDeviceIds = () => {
  form.deviceIds = 'ac44a75398c981f7,d05eae7f04ed5d52,a60a2ff1d9c3ccfb,0276ecb7a675de03,368b4f5495a5e564,f7f42dc48701c3b6,f7f42dc48701c3b6,6b148ea3088089ec,d1579a130a93aab9,e80d34b2ee6fc588,8ff0f2727c76ee81,cb00707bd8231384,22ccbb1f4183522b,22ccbb1f4183522b,f71400c874c7ae03,b053fed6f322070d,77ffb26dd8aec8d7,b19393e3fb39fed1,aa165cc58b7b69e1,066a1f89fe9e631a,766b3ef3f8f35119,c8cbd47c78e3adba,9fe81ff00522beff'
}

const analyzeData = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择Excel文件')
    return
  }

  loading.value = true
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  if (filterFile.value) {
    formData.append('filterFile', filterFile.value)
  }
  formData.append('deviceIds', form.deviceIds)
  formData.append('dataTypes', JSON.stringify(form.dataTypes))
  formData.append('platform', form.platform)

  try {
    const res = await api.post('/analyze', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    results.value = res.data
    ElMessage.success('分析完成')
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
    .map(row => `${row.metric}\t${row.initialData}\t${row.userData}`)
    .join('\n')
  
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}
</script>

<style scoped>
.excel-analysis {
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