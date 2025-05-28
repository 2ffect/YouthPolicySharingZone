<template>
  <div class="container">
    <h2 class="highlight">스크랩한 정책</h2>

    <div class="card-container">
      <RouterLink
        v-for="(policy, index) in policies"
        :key="index"
        :to="{
          name: 'policy_detail',
          params: {
            policy_keyword: policy.plcyKywdNm,
            policy_id: policy.id
          }
        }"
        class="policy-card"
      >
        <h3 class="title">{{ policy.plcyNm }}</h3>
        <p class="desc">{{ policy.plcyExplnCn }}</p>
        <p class="date">신청 기간: {{ policy.aplyYmD }}</p>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()
const policies = computed(() => accountStore.scrappedPolicy)

onMounted(() => {
  accountStore.getScrappedPolicy()
})
</script>

<style scoped>
.container {
  max-width: 960px;
  margin: 2rem auto;
  padding: 0 16px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

.highlight {
  font-size: 1.8rem;
  color: #0064ff;
  margin-bottom: 24px;
  text-align: left;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.05);
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.policy-card {
  text-decoration: none;
  color: inherit;
  background-color: #edf5fa;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
  padding: 16px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.policy-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #222;
  margin-bottom: 10px;
}

.desc {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.5;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* ✅ 2줄 이상 ... 처리 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.date {
  font-size: 0.85rem;
  color: #888;
}
</style>
