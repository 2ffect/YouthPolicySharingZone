<template>
  <div class="content">
    <h1>관심 종목 정보 검색</h1>

    <!-- 검색 -->
    <form @submit.prevent="search" class="search-form">
      <input
        name="search"
        autocomplete="off"
        :value="keyword"
        type="text"
        @input="onInput"
        placeholder="검색어를 입력하세요"
      />
      <button type="submit">찾기</button>
    </form>

    <!-- 안내 문구 -->
    <p class="info-text">영상 카드를 누르면 해당 영상으로 이동됩니다.</p>

    <!-- 영상 -->
    <div class="card-container">
      <div
        class="card"
        v-for="video in store.videos"
        :key="video.id.videoId"
        role="button"
        tabindex="0"
        @click="openYoutube(video)"
        @keydown.enter="openYoutube(video)"
      >
        <img class="card_img" :src="video.snippet.thumbnails.default.url" alt="thumbnail" />
        <h4 class="card_name">{{ video.snippet.title }}</h4>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useYoutubeStore } from '@/stores/youtube.js'

const keyword = ref('')
const store = useYoutubeStore()

// 입력 핸들링
const onInput = (event) => {
  keyword.value = event.target.value
}

// 검색 실행
const search = () => {
  if (!keyword.value.trim()) {
    alert('검색어를 입력하세요.')
    return
  }
  store.loaddata(keyword.value)
  keyword.value = ''
}

// 영상 클릭 시 유튜브로 새 탭 이동
const openYoutube = (video) => {
  const videoId = video.id.videoId
  const url = `https://www.youtube.com/watch?v=${videoId}`
  window.open(url, '_blank')
}
</script>

<style scoped>
.content {
  max-width: 960px;
  margin: 2rem auto;
  padding: 0 16px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

h1 {
  font-size: 1.8rem;
  color: #0064ff;
  margin-bottom: 20px;
}

/* 검색창 */
.search-form {
  display: flex;
  gap: 12px;
  margin-bottom: 1.2rem;
}

input {
  flex-grow: 1;
  padding: 10px 14px;
  font-size: 15px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-family: inherit;
}

button {
  background-color: #0064ff;
  color: white;
  font-size: 15px;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #0053d6;
}

.info-text {
  text-align: right;
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.75rem;
}

/* 카드 컨테이너 */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: flex-start;
}

/* 카드 */
.card {
  flex: 1 1 calc(33.33% - 20px);
  max-width: calc(33.33% - 20px);
  background-color: #f9fbff;
  padding: 16px;
  border-radius: 16px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform 0.2s;
  cursor: pointer;
  text-align: center;
  box-sizing: border-box;
}

.card:hover {
  transform: translateY(-4px);
}

.card_img {
  width: 120px;
  height: 120px;
  border-radius: 12px;
  object-fit: cover;
  margin-bottom: 10px;
  border: 1px solid #eee;
}

.card_name {
  font-weight: 600;
  font-size: 0.95rem;
  color: #222;
  text-align: center;
  max-height: 2.8em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  word-break: break-word;
  padding: 0 4px;
}
</style>
