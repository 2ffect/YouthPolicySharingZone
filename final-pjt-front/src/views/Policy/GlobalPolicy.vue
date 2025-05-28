<template>
  <div class="main-container">
    <h2 class="highlight">청년 해외 정책</h2>
    <p class="subtitle">청년의 해외 경험을 돕는 정책들을 확인해보세요.</p>

    <span @click="showExchange = true" class="info-text">
      환율이 궁금하다면?
    </span>
    <Exchange v-if="showExchange" @close="showExchange = false" />

    <div class="card-container">
      <RouterLink
        v-for="policy in policyStore.policies"
        :key="policy.plcyNo"
        :to="{
          name: 'policy_detail',
          params: {
            policy_keyword: policy.plcyKywdNm,
            policy_id: policy.id
          }
        }"
        class="policy-card"
      >
        <h3 class="policy-title">{{ policy.plcyNm }}</h3>
        <p class="policy-desc">{{ policy.plcyExplnCn }}</p>
        <p class="policy-date"><strong>신청 기간:</strong> {{ policy.aplyYmD }}</p>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePolicyStore } from '@/stores/policy'
import Exchange from './Finance/Exchange.vue'

const showExchange = ref(false)
const policyStore = usePolicyStore()

onMounted(() => {
  policyStore.getPolicies('global')
})
</script>

<style scoped>
.main-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 26px;
  font-family: 'Pretendard', sans-serif;
}

.highlight {
  font-size: 1.7rem;
  color: #0064ff;
  margin-bottom: 6px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.subtitle {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
  text-align: left;
}

.info-text {
  display: inline-block;
  font-size: 0.9rem;
  color: #e4ab10;
  margin-bottom: 20px;
  cursor: pointer;
  transition: color 0.3s ease;
  font-weight: 500;
  text-align: left;
}

.info-text:hover {
  color: #333;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

.policy-card {
  background-color: #f9fbff;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
  transition: transform 0.2s ease;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.policy-card:hover {
  transform: translateY(-4px);
}

.policy-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

/* ✅ 2줄 이상 말줄임 처리 */
.policy-desc {
  font-size: 0.95rem;
  color: #555;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2; 
  -webkit-box-orient: vertical;
  line-height: 1.4;
}

.policy-date {
  font-size: 0.85rem;
  color: #666;
}
</style>
