<template>
<div class="main">
  <div class="community-header">
    <h1>커뮤니티</h1>
  </div>

  <div class="article-list">
    <ArticleListItem />

    <!-- 버튼을 리스트 아래쪽에 배치 -->
    <div v-if="accountStore.isLogin" class="write-button-wrapper">
      <RouterLink :to="{ name: 'article_create' }">
        <button class="write-button">게시글 작성</button>
      </RouterLink>
    </div>
  </div>
</div>

</template>


<script setup>
  import { onMounted } from 'vue'
  import { RouterView, RouterLink } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts';
  import ArticleListItem from '@/views/Community/ArticleListItem.vue'
  const accountStore = useAccountStore()

  // token이 있을 경우 유저 정보 다시 불러오기
  onMounted(() => {
    if (accountStore.token.value && !accountStore.userInfo) {
      accountStore.getUserInfo()
    }
  })
</script>

<style scoped>

.main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px;
  background-color: #ffffff;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  box-sizing: border-box;
}

h1 {
  font-size: 24px;
  font-weight: bold;
  color: #0064ff;
  text-align: left;
  margin-bottom: 24px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}


/* nav, navbar 관련 기존 정의 제거 */
.navbar,
.nav,
.navbar a,
.navbar button,
.navbar a:hover,
.navbar button:hover {
  all: unset;
}

/* 반응형 대응 */
@media (max-width: 768px) {
  .main {
    padding: 20px;
    background-color: #f9f9f9;
  }

  h1 {
    font-size: 20px;
    text-align: center;
  }

  button {
    width: 100%;
    padding: 10px 0;
  }
}
.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.community-header h1 {
  flex: 1;
  text-align: center;
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
  margin: 0;
}




.article-list {
  position: relative;
  border-radius: 12px;
  box-shadow: 0 2px 6px 2px rgba(0, 0, 0, 0.1);
  padding: 8px; /* ← 여기 줄임 */
  min-height: 300px;
  display: flex;
  flex-direction: column;
}


.write-button-wrapper {
  margin-top: auto;
  text-align: right; /* 오른쪽 정렬 */
  margin-top: 20px;
}
.write-button-wrapper a {
  text-decoration: none; /* 밑줄 제거 */
}
.write-button {
  all: unset;
  background-color: #0064ff;
  color: white;
  font-size: 14px;
  font-weight: 600;
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s ease;
}

.write-button:hover {
  background-color: #0053d6;
}
</style>