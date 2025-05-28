<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">✖</button>
      <h2 class="modal-title">환율 계산기</h2>

      <div class="calculator">
        <label for="amount">금액 (KRW):</label>
        <input type="number" id="amount" v-model.number="krwAmount" placeholder="ex. 10000" />

        <label for="currency">통화 선택:</label>
        <select
          :value="selectedCurrencyId"
          @change="onCurrencyChange($event)"
        >
          <option disabled value="">통화를 선택하세요</option>
          <option v-for="ex in exchangeList" :key="ex.id" :value="ex.id">
            {{ ex.cur_nm }} {{ ex.cur_unit }}
          </option>
        </select>

        <label for="rateType">계산 기준:</label>
        <select v-model="rateType">
          <option value="deal_bas_r">기준 환율</option>
          <option value="ttb">송금 받을 때 (TTB)</option>
          <option value="tts">송금 보낼 때 (TTS)</option>
        </select>

        <div v-if="selectedCurrency" class="result-box">
          <p>선택한 환율 ({{ rateTypeLabel }}): <strong>{{ selectedCurrency[rateType] }} 원</strong></p>
          <p><strong>{{ krwAmount }}원</strong> ≈ <strong class="highlight">{{ convertedAmount }} {{ selectedCurrency.cur_unit }}</strong></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, watchEffect, onMounted, computed } from 'vue'
import { useExchangeStore } from '@/stores/finances'

const exchangeStore = useExchangeStore()
const krwAmount = ref(0)
const selectedCurrency = ref(null)
const rateType = ref('deal_bas_r')
const convertedAmount = ref(0)

const selectedCurrencyId = ref('')

const exchangeList = computed(() => exchangeStore.exchange)

function onCurrencyChange(event) {
  selectedCurrencyId.value = event.target.value
  selectedCurrency.value = exchangeList.value.find(ex => ex.id == selectedCurrencyId.value) || null
}


// exchangeStore.exchange가 바뀔 때마다 드롭다운 갱신
watch(
  () => exchangeStore.exchange,
  (newVal) => {
    // 선택된 id가 사라졌다면 선택 해제
    if (!newVal.find(ex => ex.id == selectedCurrencyId.value)) {
      selectedCurrencyId.value = ''
      selectedCurrency.value = null
    }
  }
)

onMounted(async () => {
  await exchangeStore.saveExchangeRate()
  await exchangeStore.getExchange()
})


defineEmits(['close'])

const rateTypeLabel = computed(() => {
  switch (rateType.value) {
    case 'ttb': return '송금 받을 때';
    case 'tts': return '송금 보낼 때';
    default: return '기준 환율';
  }
})


watchEffect(() => {
  if (!selectedCurrency.value || !krwAmount.value) {
    convertedAmount.value = 0
    return
  }
  const rawRate = selectedCurrency.value[rateType.value]
  if (!rawRate) {
    convertedAmount.value = 0
    return
  }

  const rate = parseFloat(rawRate.replace(/,/g, ''))
  convertedAmount.value = (krwAmount.value / rate).toFixed(2)
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  font-family: 'Pretendard', sans-serif;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 600px;
  width: 90%;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.modal-title {
  margin-bottom: 1rem;
  font-size: 20px;
  color: #333;
  font-weight: bold;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: transparent;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #333;
}

.calculator {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

label {
  font-size: 14px;
  color: #444;
  margin-top: 0.5rem;
}

input, select {
  padding: 0.5rem;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.result-box {
  background-color: #f0f6ff;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
  color: #333;
  font-size: 14px;
  line-height: 1.4;
}

.highlight {
  color: #0064ff;
  font-weight: bold;
}
</style>
