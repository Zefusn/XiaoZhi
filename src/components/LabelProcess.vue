<template>
  <div class="label-process">
    <el-form :model="form" label-width="180px">
      <el-form-item label="选择 Excel 文件">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :limit="1"
          :on-change="handleFileChange"
          :on-remove="handleFileRemove"
          :on-exceed="handleFileExceed"
          :file-list="fileList"
          accept=".xlsx,.xls,.xlsm,.xltx,.xltm"
        >
          <el-button type="primary" :icon="Upload">选择文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              仅支持 .xlsx, .xls, .xlsm, .xltx, .xltm 文件
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
          :on-remove="handleFilterFileRemove"
          :on-exceed="handleFilterFileExceed"
          :file-list="filterFileList"
          accept=".xlsx,.xls,.xlsm,.xltx,.xltm"
        >
          <el-button type="primary" :icon="Upload">选择过滤文件</el-button>
          <template #tip>
            <div class="el-upload__tip">
              选择包含需要去除的 userContent 的 Excel 文件
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

      <el-form-item label="选择平台">
        <el-radio-group v-model="form.platform">
          <el-radio label="安卓">安卓</el-radio>
          <el-radio label="iOS">iOS</el-radio>
          <el-radio label="鸿蒙">鸿蒙</el-radio>
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
        <el-table-column prop="label" :label="getLabelColumnTitle" min-width="200" />
        <el-table-column 
          v-if="showCountColumn" 
          prop="count" 
          label="数量" 
          width="120" 
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
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload } from '@element-plus/icons-vue'
import api from '@/utils/request'
import { selectedFile as sharedSelectedFile, filterFile as sharedFilterFile, fileName as sharedFileName, filterFileName as sharedFilterFileName, updateSelectedFile, updateFileName, updateFilterFile, updateFilterFileName } from '@/store/fileStore'

const form = reactive({
  deviceIds: 'ac28a948f719463aa730514e04ca66e6,4d530e405ee02c82,1b1e906119545bc1,e364860f627f5e18,0276ecb7a675de03,774f3938009049de87b974b89b2df1dd,8ca5dde4ab6fcc46,00344d2ee15746babb5d6270a7d25551,60467f3ec8b04dd9847c9ef847edbe8d,cd0dc52d06117fb9,3da02abec00d495bbbb401ba4ed8253d,3d21ce8e7f584765,d136cd6ef5f0b53e,e80d34b2ee6fc588,67a7e394bdbb87c6,266afcda853c4f80,0d638755f40323e2,7550b688dde06d23,f7f42dc48701c3b6,9771bb5db3ec2ab3,3ad6ea34129240f5974e27f9ecd3a01f,030575dd2d444a3ebf5b110aece14f89,535d620d0f030465,6b148ea3088089ec,a60a2ff1d9c3ccfb,22ccbb1f4183522b,b053fed6f322070d,3a764e1d2e06400d8475f5703083dea1,4c96f7aa72fc4f54b9f89004679db9eb,0bc2724e948c466ab154f536b5729604,f75fbcb1a4644e9eb3f93b9d55fdb2fb,cf7c87b73c4d1903',
  platform: '安卓',
  analysisType: 'default'
})

const uploadRef = ref()
const filterUploadRef = ref()
const tableRef = ref()
// 使用共享的文件状态
const selectedFile = sharedSelectedFile
const filterFile = sharedFilterFile
const loading = ref(false)
const results = ref([])
const selectedRows = ref([])
// 文件列表用于显示已选择的文件
const fileList = ref([])
const filterFileList = ref([])

// 监听共享文件状态变化，同步文件列表显示
watch(sharedFileName, (newName) => {
  if (newName) {
    fileList.value = [{ name: newName, uid: Date.now() }]
  } else {
    fileList.value = []
  }
})

watch(sharedFilterFileName, (newName) => {
  if (newName) {
    filterFileList.value = [{ name: newName, uid: Date.now() }]
  } else {
    filterFileList.value = []
  }
})

// 计算属性：根据分析类型决定是否显示数量列
const showCountColumn = computed(() => {
  return form.analysisType !== 'function'
})

// 计算属性：根据分析类型决定列标题
const getLabelColumnTitle = computed(() => {
  if (form.analysisType === 'function') {
    return '内容'
  } else {
    return '标签名称'
  }
})

const handleFileChange = (file) => {
  updateSelectedFile(file.raw)
  updateFileName(file.name)
  // 更新文件列表
  fileList.value = [{ name: file.name, uid: file.uid }]
}

const handleFileExceed = (files) => {
  // 当超出文件数量限制时，自动替换为新文件
  uploadRef.value.clearFiles()
  const file = files[0]
  uploadRef.value.handleStart(file)
  updateSelectedFile(file)
  updateFileName(file.name)
  fileList.value = [{ name: file.name, uid: file.uid || Date.now() }]
}

const handleFileRemove = () => {
  updateSelectedFile(null)
  updateFileName('')
  // 清空文件列表
  fileList.value = []
}

const handleFilterFileChange = (file) => {
  if (file) {
    updateFilterFile(file.raw)
    updateFilterFileName(file.name)
    // 更新过滤文件列表
    filterFileList.value = [{ name: file.name, uid: file.uid }]
  }
}

const handleFilterFileExceed = (files) => {
  // 当超出文件数量限制时，自动替换为新文件
  filterUploadRef.value.clearFiles()
  const file = files[0]
  filterUploadRef.value.handleStart(file)
  updateFilterFile(file)
  updateFilterFileName(file.name)
  filterFileList.value = [{ name: file.name, uid: file.uid || Date.now() }]
}

const handleFilterFileRemove = () => {
  updateFilterFile(null)
  updateFilterFileName('')
  // 清空过滤文件列表
  filterFileList.value = []
}

const setDefaultDeviceIds = () => {
  form.deviceIds = 'ac28a948f719463aa730514e04ca66e6,4d530e405ee02c82,1b1e906119545bc1,e364860f627f5e18,0276ecb7a675de03,774f3938009049de87b974b89b2df1dd,8ca5dde4ab6fcc46,00344d2ee15746babb5d6270a7d25551,60467f3ec8b04dd9847c9ef847edbe8d,cd0dc52d06117fb9,3da02abec00d495bbbb401ba4ed8253d,3d21ce8e7f584765,d136cd6ef5f0b53e,e80d34b2ee6fc588,67a7e394bdbb87c6,266afcda853c4f80,0d638755f40323e2,7550b688dde06d23,f7f42dc48701c3b6,9771bb5db3ec2ab3,3ad6ea34129240f5974e27f9ecd3a01f,030575dd2d444a3ebf5b110aece14f89,535d620d0f030465,6b148ea3088089ec,a60a2ff1d9c3ccfb,22ccbb1f4183522b,b053fed6f322070d,3a764e1d2e06400d8475f5703083dea1,4c96f7aa72fc4f54b9f89004679db9eb,0bc2724e948c466ab154f536b5729604,f75fbcb1a4644e9eb3f93b9d55fdb2fb,cf7c87b73c4d1903'
}

const generateResults = async () => {
  if (!sharedSelectedFile.value) {
    ElMessage.warning('请先选择 Excel 文件')
    return
  }

  loading.value = true
  const formData = new FormData()
  formData.append('file', sharedSelectedFile.value)
  if (sharedFilterFile.value) {
    formData.append('filterFile', sharedFilterFile.value)
  }
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
  
  let text
  if (showCountColumn.value) {
    // 包含数量列
    text = selectedRows.value
      .map(row => `${row.label}\t${row.count}`)
      .join('\n')
  } else {
    // 不包含数量列，只复制标签名称（或内容）
    text = selectedRows.value
      .map(row => row.label)
      .join('\n')
  }
  
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}
</script>

<style scoped>
.label-process {
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

.mt-10 {
  margin-top: 12px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-upload-list__item) {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-top: 8px;
  padding: 8px 12px;
  background: #f9fafb;
}

:deep(.el-upload-list__item-name) {
  color: #6366f1;
  font-weight: 500;
}

:deep(.el-checkbox__label),
:deep(.el-radio__label) {
  font-weight: 400;
}

:deep(.el-button--success) {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border: none;
}

:deep(.el-button--success:hover) {
  background: linear-gradient(135deg, #059669 0%, #047857 100%);
}
</style>