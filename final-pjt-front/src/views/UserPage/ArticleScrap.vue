<template>
  <div class="container">
    <h2 class="highlight">스크랩한 게시글</h2>
    <RouterLink
      v-for="(article, index) in articles"
      :key="article.id"
      :to="{ name: 'article_detail', params: { article_id: article.id } }"
      class="card"
    >
      <h3 class="title">{{ article.title }}</h3>
      <p class="date">작성일: {{ formatDate(article.created_at) }}</p>
    </RouterLink>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'
import { RouterLink } from 'vue-router'

const accountStore = useAccountStore()
const articles = computed(() => accountStore.scrappedArticle)

const formatDate = (dateStr) => {
  return dateStr ? dateStr.slice(0, 10) : ''
}

onMounted(() => {
  accountStore.getScrappedArticle()
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
  font-size: 1.6rem;
  color: #0064ff;
  margin-bottom: 24px;
  text-align: left;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.05);
}

.card {
  display: block;
  text-decoration: none;
  color: inherit;
  border-radius: 12px;
  background-color: #f9f9f9;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.title {
  font-size: 1.05rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #222;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.date {
  font-size: 0.85rem;
  color: #888;
}
</style>
