<template>
  <div class="content">
    <h1>예금 상품</h1>

    <!-- 로딩 중 -->
    <div v-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>🏦 실시간으로 예금 상품을 불러오는 중입니다...</p>
    </div>

    <!-- 본문 내용 -->
    <div v-else>
      <!-- 은행 선택 -->
      <div class="control-bar">
        <select v-model="selectedBank" @change="getDepositProducts">
          <option value="">전체 은행</option>
          <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
        </select>
      </div>

      <!-- 안내 문구 -->
      <p class="info-text">모든 금리는 우대 금리를 모두 반영한 최고 금리로 표시됩니다.</p>
      <p class="info-text">아래 정보는 {{ formattedTime }} 기준 금융감독원으로부터 제공받은 정보입니다.</p>

      <!-- 예금 테이블 -->
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
          <tr v-for="product in products" :key="product.fin_prdt_cd">
            <td>{{ product.kor_co_nm }}</td>
            <td>{{ product.fin_prdt_nm }}</td>
            <td :class="{ highlight: maxTerm(product.options) === 6 }">{{ getRate(product.options, 6) }}</td>
            <td :class="{ highlight: maxTerm(product.options) === 12 }">{{ getRate(product.options, 12) }}</td>
            <td :class="{ highlight: maxTerm(product.options) === 24 }">{{ getRate(product.options, 24) }}</td>
            <td :class="{ highlight: maxTerm(product.options) === 36 }">{{ getRate(product.options, 36) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchBanks, fetchDepositProducts } from '@/stores/finances.js'

const banks = ref([])
const products = ref([])
const selectedBank = ref('')
const fetchedTime = ref(null)
const formattedTime = ref('')
const isLoading = ref(false)

const getDepositProducts = async () => {
  isLoading.value = true
  try {
    const res = await fetchDepositProducts(selectedBank.value)
    products.value = res.data
    fetchedTime.value = new Date()
    formattedTime.value = formatDate(fetchedTime.value)
  } finally {
    isLoading.value = false
  }
}

const getRate = (options, term) => {
  const opt = options.find(o => o.save_trm === term)
  return opt ? `${opt.intr_rate2}%` : '-'
}

const maxTerm = (options) => {
  const terms = [6, 12, 24, 36]
  let maxRate = -1
  let maxTerm = null
  for (const term of terms) {
    const opt = options.find(o => o.save_trm === term)
    if (opt && opt.intr_rate2 > maxRate) {
      maxRate = opt.intr_rate2
      maxTerm = term
    }
  }
  return maxTerm
}

const formatDate = (date) => {
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const min = String(date.getMinutes()).padStart(2, '0')
  return `${yyyy}/${mm}/${dd} - ${hh}:${min}`
}

onMounted(async () => {
  isLoading.value = true
  try {
    const bankRes = await fetchBanks()
    banks.value = bankRes.data.banks
    await getDepositProducts()
  } finally {
    isLoading.value = false
  }
})
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
  justify-content: flex-start;
  margin-bottom: 1rem;
}

select {
  padding: 10px 14px;
  font-size: 15px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-family: inherit;
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
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
  /* color: #ff3300; */
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

