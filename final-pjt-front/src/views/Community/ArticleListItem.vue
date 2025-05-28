<template>
  <div class="main">
    <table class="article-table">
      <thead>
        <tr>
          <th>번호</th>
          <th>제목</th>
          <th>작성자</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(article, index) in communityStore.articles"
          :key="article.id"
          class="clickable-row"
          @click="$router.push({ name: 'article_detail', params: { article_id: article.id } })"
        >
          <td>{{ index + 1 }}</td>
          <td>{{ article.title }}</td>
          <td>{{ article.nickname }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useCommunityStore } from '@/stores/community.js'
const communityStore = useCommunityStore()

onMounted(()=>{
  communityStore.getArticles()
})

</script>

<style scoped>
.main {
  width: 100%; /* ← div 안에서 꽉 차게 */
  padding: 0;   /* ← 내부 여백 제거 */
  margin: 0 auto;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  background-color: transparent; /* 배경은 부모에서 받도록 */
}


.article-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.article-table th,
.article-table td {
  padding: 12px;
  border-bottom: 1px solid #ddd;
}

.article-table thead {
  background-color: #f1f3f5;
}

.clickable-row {
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.clickable-row:hover {
  background-color: #f0f8ff;
}
</style>
