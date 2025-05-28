<template>
  <div class="main-container">
    <div class="nav-container">

      <h2 class="highlight">청년 정책</h2>
      <p class="subtitle">정책 분야별로 맞춤형 정보를 확인해보세요.</p>
  
      <nav class="navbar">
        <div class="nav">
          <RouterLink :to="{ name: 'finance_policy' }">청년 우대 금융 상품</RouterLink> |
          <RouterLink :to="{ name: 'job_policy' }">청년 취업 정책</RouterLink> |
          <RouterLink :to="{ name: 'global_policy' }">청년 해외 정책</RouterLink>
        </div>
      </nav>
    </div>

    <RouterView />
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>

<style scoped>
.main-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 10px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

.highlight {
  font-size: 1.8rem;
  color: #0064ff;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
}

.subtitle {
  font-size: 14px;
  color: #666;
  text-align: center;
  margin-bottom: 24px;
}

.navbar {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #ddd;
  background-color: #ffffff;
  border-radius: 12px;
  /* box-shadow: 0 0px 0px rgba(0,0,0,0.05); */
  margin-bottom: 24px;
}

.nav {
  display: flex;
  gap: 24px;
  font-size: 15px;
  font-weight: 600;
}

.nav a {
  text-decoration: none;
  color: #333;
  transition: color 0.2s ease;
}

.nav a:hover {
  color: #0064ff;
}
.nav-container{
  box-shadow:  0px 2px rgba(0,0,0,0.05);
  border-radius: 12px;
}
</style>
