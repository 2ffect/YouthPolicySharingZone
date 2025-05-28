<template>
  <div class="detail-wrapper">
    <h2 class="title">{{ policyStore.policy.plcyNm }}</h2>

    <div class="policy-content">
      <p class="desc">{{ policyStore.policy.plcyExplnCn }}</p>
      <div class="info">
        <p><strong>상세 내용:</strong> {{ policyStore.policy.plcySprtCn }}</p>
        <p><strong>정책 번호:</strong> {{ policyStore.policy.plcyNo }}</p>
        <p><strong>학력 제한:</strong> {{ policyStore.policy.schoolCd }}</p>
        <p><strong>결혼 여부:</strong> {{ policyStore.policy.mrgSttsCd }}</p>
        <p><strong>재직 여부:</strong> {{ policyStore.policy.jobCd }}</p>
        <p><strong>지원 기간:</strong> {{ policyStore.policy.aplyYmD }}</p>
      </div>
    </div>

    <div class="bottom-bar">
      <div v-if="accountStore.isLogin">
        <button
          class="scrap-button"
          v-if="policyStore.isPolicyScrapped"
          @click.prevent="onUnscrapPolicy"
        >
          스크랩 취소
        </button>
        <button
          class="scrap-button"
          v-else
          @click.prevent="onScrapPolicy"
        >
          스크랩 하기
        </button>
      </div>

      <div class="back-button">
        <RouterLink
          v-if="route.params.policy_keyword === '금리혜택'"
          :to="{ name: 'finance_policy' }"
        >
          <button>목록으로 돌아가기</button>
        </RouterLink>
        <RouterLink
          v-else-if="route.params.policy_keyword === '장기미취업청년'"
          :to="{ name: 'job_policy' }"
        >
          <button>목록으로 돌아가기</button>
        </RouterLink>
        <RouterLink v-else :to="{ name: 'global_policy' }">
          <button>목록으로 돌아가기</button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePolicyStore } from '@/stores/policy'
import { useAccountStore } from '@/stores/accounts'

const route = useRoute()
const policyStore = usePolicyStore()
const accountStore = useAccountStore()

const onUnscrapPolicy = () => {
  policyStore.unscrapPolicy(route.params.policy_id)
}

const onScrapPolicy = () => {
  policyStore.scrapPolicy(route.params.policy_id)
}

onMounted(() => {
  policyStore.getPolicy(route.params.policy_id)
  policyStore.checkIfScrapped(route.params.policy_id)
})
</script>

<style scoped>
.detail-wrapper {
  max-width: 960px;
  margin: 2rem auto;
  padding: 0 16px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 24px;
  color: #222;
  border-bottom: 2px solid #ccc;
  padding-bottom: 12px;
}

.policy-content {
  padding-bottom: 32px;
  line-height: 1.75;
  font-size: 1rem;
  color: #333;
}

.desc {
  margin-bottom: 20px;
  font-weight: 500;
}

.info p {
  margin-bottom: 10px;
  color: #444;
}

.bottom-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 32px;
  flex-wrap: wrap;
  gap: 12px;
}

.scrap-button {
  padding: 10px 20px;
  background-color: #0064ff;
  color: white;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.scrap-button:hover {
  background-color: #004fc2;
}

.back-button button {
  padding: 10px 20px;
  background-color: #3c80ceec;
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.back-button button:hover {
  background-color: #3c80ce;
}
</style>
