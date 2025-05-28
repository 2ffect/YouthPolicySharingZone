<template>
  <div class="content">
    <h1>적금 상품</h1>

    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>🏦 실시간으로 적금 상품을 불러오는 중입니다...</p>
    </div>

    <div v-else>
      <!-- 은행 선택 + 적립 방식 선택 -->
      <div class="control-bar">
        <select v-model="selectedBank" @change="getSavingProducts">
          <option value="">전체 은행</option>
          <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
        </select>

        <div class="saving-type-toggle">
          <button
            :class="{ active: selectedType === '정액적립식' }"
            @click="selectedType = '정액적립식'"
          >
            정액적립식
          </button>
          <button
            :class="{ active: selectedType === '자유적립식' }"
            @click="selectedType = '자유적립식'"
          >
            자유적립식
          </button>
        </div>
      </div>

      <!-- 안내 문구 -->
      <p class="info-text">모든 금리는 우대 금리를 모두 반영한 최고 금리로 표시됩니다.</p>
      <p class="info-text">아래 정보는 {{ formattedTime }} 기준 금융감독원으로부터 제공받은 정보입니다.</p>

      <!-- 적금 테이블 -->
      <table class="product-table">
        <thead>
          <tr>
            <th>은행명</th>
            <th>상품명</th>
            <th>6개월</th>
            <th>12개월</th>
            <th>24개월</th>
            <th>36개월</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd">
            <td>{{ product.kor_co_nm }}</td>
            <td>{{ product.fin_prdt_nm }}</td>
            <td :class="{ highlight: highestRateTerm(product) === 6 }">{{ rateByTerm(product, 6) }}</td>
            <td :class="{ highlight: highestRateTerm(product) === 12 }">{{ rateByTerm(product, 12) }}</td>
            <td :class="{ highlight: highestRateTerm(product) === 24 }">{{ rateByTerm(product, 24) }}</td>
            <td :class="{ highlight: highestRateTerm(product) === 36 }">{{ rateByTerm(product, 36) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchBanks, fetchSavingProducts } from '@/stores/finances.js'

const banks = ref([])
const products = ref([])
const selectedBank = ref('')
const selectedType = ref('정액적립식')
const fetchedTime = ref(null)
const formattedTime = ref('')
const isLoading = ref(false)

const formatDate = (date) => {
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const min = String(date.getMinutes()).padStart(2, '0')
  return `${yyyy}/${mm}/${dd} - ${hh}:${min}`
}

const getSavingProducts = async () => {
  isLoading.value = true
  try {
    const res = await fetchSavingProducts(selectedBank.value)
    products.value = res.data
    fetchedTime.value = new Date()
    formattedTime.value = formatDate(fetchedTime.value)
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  isLoading.value = true
  try {
    const bankRes = await fetchBanks()
    banks.value = bankRes.data.banks
    await getSavingProducts()
  } finally {
    isLoading.value = false
  }
})

const rateByTerm = (product, term) => {
  const option = product.options.find(opt => opt.save_trm === term && opt.rsrv_type_nm === selectedType.value)
  return option ? `${option.intr_rate2}%` : '-'
}

const highestRateTerm = (product) => {
  const filtered = product.options.filter(opt => opt.rsrv_type_nm === selectedType.value)
  if (!filtered.length) return null
  const maxOption = filtered.reduce((a, b) => (a.intr_rate2 > b.intr_rate2 ? a : b))
  return maxOption.save_trm
}

const filteredProducts = computed(() =>
  products.value.filter(product =>
    product.options.some(opt => opt.rsrv_type_nm === selectedType.value)
  )
)
</script>

<style scoped>
.content {
  max-width: 960px;
  margin: 2rem auto;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  padding: 0 16px;
}

h1 {
  font-size: 1.8rem;
  color: #0064ff;
  margin-bottom: 16px;
  text-align: left;
}

.control-bar {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  align-items: center;
  gap: 16px;
  margin-bottom: 1rem;
}

select {
  padding: 10px 14px;
  font-size: 15px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-family: inherit;
}

.saving-type-toggle {
  display: flex;
  gap: 8px;
}

.saving-type-toggle button {
  padding: 8px 16px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.saving-type-toggle button:hover {
  background-color: #e9f0ff;
}

.saving-type-toggle .active {
  background-color: #0064ff;
  color: white;
  font-weight: bold;
  border-color: #0064ff;
}

.info-text {
  text-align: right;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 4px;
}

.product-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.product-table th,
.product-table td {
  border: 1px solid #e0e0e0;
  padding: 12px 10px;
  text-align: center;
  font-size: 0.95rem;
}

.product-table th {
  background-color: #f0f4ff;
  color: #333;
  font-weight: 600;
}

.product-table tr:hover {
  background-color: #fafcff;
}

.highlight {
  background-color: #e0f0ff;
  font-weight: bold;
  color: #ff0000;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem 1rem;
  font-size: 1.1rem;
  color: #333;
}

.spinner {
  border: 6px solid #f3f3f3;
  border-top: 6px solid #0064ff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
