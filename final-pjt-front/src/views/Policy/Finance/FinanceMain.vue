<template>
  <div>
    <div class="link-container">
      <RouterLink
        :to="{ name: 'deposit' }"
        class="link-button"
        :class="{ active: route.name === 'deposit' }"
      >예금 상품</RouterLink>

      <RouterLink
        :to="{ name: 'saving' }"
        class="link-button"
        :class="{ active: route.name === 'saving' }"
      >적금 상품</RouterLink>

      <RouterLink
        :to="{ name: 'info' }"
        class="link-button"
        :class="{ active: route.name === 'info' }"
      >주식 정보</RouterLink>
    </div>

    <RouterView />
  </div>
</template>

<script setup>
import { RouterView, RouterLink, useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped>
.link-container {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
  margin-bottom: 24px;
  font-family: 'Pretendard', sans-serif;
}

.link-button {
  padding: 12px 20px;
  background-color: #f1f3f5;
  border-radius: 10px;
  color: #333;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  transition: all 0.25s ease;
}

.link-button:hover {
  background-color: #e3e8ee;
  color: #0064ff;
}

.link-button.active {
  background-color: #0064ff;
  color: #fff;
  box-shadow: 0 2px 8px rgba(0, 100, 255, 0.3);
}

.content {
  max-width: 960px;
  margin: 2rem auto;
  font-family: 'Pretendard', sans-serif;
}

select {
  margin: 1rem 0;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.product-box {
  margin-bottom: 1.5rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  background-color: #f9f9f9;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}
</style>

