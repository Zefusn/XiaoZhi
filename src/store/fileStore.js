import { ref } from 'vue'

// 创建共享的文件状态
export const selectedFile = ref(null)
export const filterFile = ref(null)
export const fileName = ref('')
export const filterFileName = ref('')

// 重置所有文件状态
export const resetFiles = () => {
  selectedFile.value = null
  filterFile.value = null
  fileName.value = ''
  filterFileName.value = ''
}

// 更新主文件
export const updateSelectedFile = (file) => {
  selectedFile.value = file
}

// 更新过滤文件
export const updateFilterFile = (file) => {
  filterFile.value = file
}

// 更新主文件名
export const updateFileName = (name) => {
  fileName.value = name
}

// 更新过滤文件名
export const updateFilterFileName = (name) => {
  filterFileName.value = name
}