<template>
  <div class="main-container">
    <h2 class="highlight">마이페이지</h2>

    <nav class="navbar">
      <div class="nav">
        <RouterLink :to="{ name: 'user_info' }">개인 정보 수정</RouterLink>
        <RouterLink :to="{ name: 'policy_scrap' }">스크랩한 정책</RouterLink>
        <RouterLink :to="{ name: 'article_scrap' }">스크랩한 게시글</RouterLink>
      </div>
    </nav>

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
  padding: 32px 16px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

.highlight {
  font-size: 1.8rem;
  color: #0064ff;
  margin-bottom: 16px;
  text-align: left;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.05);
}

.navbar {
  border-bottom: 1px solid #ddd;
  padding-bottom: 16px;
  margin-bottom: 24px;
}

.nav {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  font-size: 15px;
  font-weight: 600;
}

.nav a {
  color: #333;
  text-decoration: none;
  padding-bottom: 4px;
  transition: color 0.2s ease, border-color 0.2s ease;
  border-bottom: 2px solid transparent;
}

.nav a:hover {
  color: #0064ff;
  border-color: #0064ff;
}
</style>
