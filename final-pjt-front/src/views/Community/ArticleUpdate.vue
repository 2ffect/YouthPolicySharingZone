<template>
  <div class="main">
    <div class="article-area">
      <div class="article-card">
        <div class="article-header">
          <h2 class="article-title">게시글 수정</h2>
        </div>

        <form @submit.prevent="onUpdateArticle" class="article-form">
          <div class="form-group">
            <label for="title">제목</label>
            <input type="text" id="title" v-model="title" class="input-field" />
          </div>

          <div class="form-group">
            <label for="content">내용</label>
            <textarea id="content" v-model="content" class="textarea-field"></textarea>
          </div>

          <div class="author-controls">
            <button type="submit" class="btn auth">수정 완료</button>
            <RouterLink :to="{ name: 'article_detail', params: { article_id: route.params.article_id }}">
              <button type="button" class="btn auth">수정 취소</button>
            </RouterLink>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useCommunityStore } from '@/stores/community'

const communityStore = useCommunityStore()
const route = useRoute()
const article = computed(() => communityStore.article)
const title = ref('')
const content = ref('')

const onUpdateArticle = function () {
  const articleInfo = {
    title: title.value,
    content: content.value,
  }
  communityStore.updateArticle(articleInfo, route.params.article_id)
}

onMounted(() => {
  title.value = article.value.title
  content.value = article.value.content
})
</script>

<style scoped>
.main {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

.article-area {
  display: flex;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin-bottom: 32px;
}

.article-card {
  width: 100%;
}

.article-header {
  margin-bottom: 16px;
}

.article-title {
  font-size: 22px;
  color: #333;
  margin-bottom: 8px;
}

.article-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.input-field,
.textarea-field {
  width: 100%;
  font-size: 16px;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  resize: vertical;
}

.textarea-field {
  min-height: 140px;
}

.author-controls {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 10px;
}
.author-controls a{
    text-decoration: none;
}
.btn {
  all: unset;
  background-color: #0064ff;
  color: white;
  font-size: 14px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  margin-right: 8px;
}

.btn:hover {
  background-color: #0053d6;
}

.btn.auth {
  background-color: #999;
}

.btn.auth:hover {
  background-color: #666;
}
</style>
