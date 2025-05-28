<template>
  <div class="article-area">
    <h2 class="article-title">게시글 작성하기</h2>
    <form @submit.prevent="onCreateArticle">
      <label for="title">제목</label>
      <input type="text" id="title" placeholder="제목을 입력하세요" v-model="title" required />

      <label for="content">내용</label>
      <textarea id="content" placeholder="내용을 입력하세요" v-model="content" required></textarea>

      <div class="button-group">
        <button type="submit" class="btn">게시하기</button>
        <RouterLink :to="{ name: 'community' }">
          <button type="button" class="btn cancel">작성 취소</button>
        </RouterLink>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useCommunityStore } from '@/stores/community.js'

const title = ref('')
const content = ref('')
const communityStore = useCommunityStore()

const onCreateArticle = () => {
  const articleInfo = {
    title: title.value,
    content: content.value,
  }
  communityStore.createArticle(articleInfo)
}
</script>

<style scoped>
.article-area {
  min-height: 500px;
  max-width: 960px;
  width: 100%;
  margin: 2rem auto;
  padding: 32px;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

.article-title {
  font-size: 1.6rem;
  margin-bottom: 24px;
  color: #0064ff;
  font-weight: 700;
  text-align: center;
}

label {
  display: block;
  margin-top: 16px;
  font-weight: bold;
  color: #333;
}

input,
textarea {
  width: 100%;
  padding: 12px;
  margin-top: 6px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  resize: vertical;
}

textarea {
  min-height: 300px;
}

.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: bold;
  font-size: 14px;
  cursor: pointer;
  border: none;
  transition: background-color 0.2s ease;
  background-color: #0064ff;
  color: white;
}

.btn:hover {
  background-color: #004fc2;
}

.btn.cancel {
  background-color: #ccc;
  color: #333;
}

.btn.cancel:hover {
  background-color: #aaa;
}
</style>
