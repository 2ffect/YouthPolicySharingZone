<template>
  <div class="main-container">
    <div class="content-wrapper">
      <div class="chat-area">
        <h2><span class="highlight">청년정책</span>, 챗봇으로 쉽게 찾아보세요!</h2>
        <p class="subtitle">청년 우대 금융 상품, 청년 취업 정책, 청년 해외 정책 등 키워드로 찾아보아요.</p>
        <div class="chatbot-content">
          <div class="chatbot-chatbox">
            <Chatbot />
            <div v-if="!accountStore.isLogin" class="chatbot-overlay">
              <p class="overlay-text">로그인을 하고 챗봇을 이용해보세요!</p>
            </div>
            <div v-else-if="isMissingProfile" class="chatbot-overlay">
              <p class="overlay-text">
                <RouterLink :to="{ name: 'chatbot_profile' }">
                  <button class="login-button">추가정보 입력하고 챗봇 이용하러 가기 🔒</button>
                </RouterLink>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div class="right-area">
        <div class="login-box box">
          <div class="login-profile">
            <div v-if="accountStore.isLogin">
              <br>
              <div class="welcome-icon">🙋‍♂️</div>
              <p class="welcome-message">{{ accountStore.userInfo.username + ' (' + accountStore.userInfo.nickname + ') 님 안녕하세요 !' }}</p>
              <br>
              <span class="links">
                <RouterLink :to="{ name: 'user_info' }">마이페이지</RouterLink> |
                <RouterLink :to="{ name: 'policy_scrap' }">스크랩 한 정책</RouterLink> |
                <RouterLink :to="{ name: 'article_scrap' }">스크랩 한 게시글</RouterLink>
              </span>
            </div>
            <div v-else>
              <p class="login-text">로그인하여 맞춤 정책정보를 확인하세요.</p>
              <div class="login-actions">
                <RouterLink :to="{ name: 'login' }" class="login-button-wrapper">
                  <button class="login-button">로그인</button>
                </RouterLink>
                <RouterLink :to="{ name: 'signup' }" class="signup-link">회원가입</RouterLink>
              </div>
            </div>

          </div>
        </div>
        <div class="policy-box box">
          <div class="box-header">
            <h3 class="box-title">📌 정책 모아보기</h3>
            <RouterLink :to="{ name: 'finance_policy' }">
              <button class="preview-button">정책 바로가기</button>
            </RouterLink>
          </div>
          <ul class="preview-list">
            <li v-for="policy in policyStore.policies.slice(0, 5)" :key="policy.id" class="preview-item">
              <RouterLink :to="{ name: 'policy_detail', params: {policy_keyword: policy.plcyKywdNm, policy_id: policy.id} }" class="policy-link">
                <span class="policy-label">[청년우대금융] </span>
                <span class="policy-title">{{ policy.plcyNm }}</span>
              </RouterLink>
            </li>
          </ul>
        </div>
        <div class="article-box box">
          <div class="box-header">
            <h3 class="box-title">📰 게시글 모아보기</h3>
            <RouterLink :to="{ name: 'community' }">
              <button class="preview-button">게시판 바로가기</button>
            </RouterLink>
          </div>
          <ul class="preview-list">
            <li v-for="article in communityStore.articles.slice(0, 5)" :key="article.id" class="preview-item">
              <RouterLink :to="{ name: 'article_detail', params: { article_id: article.id } }" class="policy-link">
                <span class="policy-label">[{{ article.nickname }}] </span>
                <span class="policy-title">{{ article.title }}</span>
              </RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, watchEffect, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'
import { useChatbotStore } from '@/stores/chatbot.js'
import { usePolicyStore } from '@/stores/policy'
import { useCommunityStore } from '@/stores/community'
import Chatbot from '@/views/Chatbot/Chatbot.vue'

const accountStore = useAccountStore()
const chatbotStore = useChatbotStore()
const policyStore = usePolicyStore()
const communityStore = useCommunityStore()
const isMissingProfile = ref(false)

watch(() => accountStore.mustLoginRedirect, (val) => {
  if (val) {
    alert('로그인해야 이용 가능합니다.')
    accountStore.setMustLoginRedirect(false)
  }
}, { immediate: true })

watchEffect(async () => {
  if (accountStore.isLogin) {
    const valid = await chatbotStore.checkProfileInfo()
    isMissingProfile.value = !valid
  } else {
    isMissingProfile.value = false
  }
})



onMounted(() => {
  communityStore.getArticles()
  policyStore.getPolicies('finance')
})
</script>

<style scoped>
button,
.login-button {
  all: unset;
  background-color: #0064ff;
  color: white;
  font-size: 15px;
  font-weight: 600;
  border-radius: 10px;
  padding: 5px 16px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.2s ease;
  text-decoration: none; /* 밑줄 제거 */
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.preview-button{
  all: unset;
  background-color: #0066ffee;
  color: white;
  font-size: 12px;
  font-weight: bold;
  border-radius: 10px;
  padding: 6px 16px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.2s ease;
  text-decoration: none; /* 밑줄 제거 */
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
  box-shadow: 0 2px 6px 2px rgba(0, 0, 0, 0.1);
}

a,
a:visited,
a:active,
a:focus {
  text-decoration: none; /* 모든 링크 기본 밑줄 제거 */
}

.preview-button:hover,
.login-button:hover,
button:hover {
  background-color: #0053d6;
}

/* 이하 기존 스타일 유지 */
.main-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px;
  background-color: #ffffff;
  font-family: 'Pretendard', sans-serif;
  /* overflow: hidden; */
  box-sizing: border-box;
}

.content-wrapper {
  display: flex;
  gap: 24px;
  height: 100%;
}

.chat-area {
  flex: 3;
  background-color: #f9f9f9;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  height: 100%;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.chatbot-content {
  background: #e6f0ff;
  border-radius: 12px;
  padding: 18px;
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;   /* ✅ 고정 높이 유지 */
}

.chatbot-chatbox {
  position: relative;
  flex: 1;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 10px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  max-height: 100%; /* ✅ 스크롤 영역이 부모 높이 이내로 유지되도록 */
}

.chatbot-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(200, 200, 200, 0.7);
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  animation: fadeIn 0.4s ease-in-out;
}

.overlay-text {
  font-size: 15px;
  color: #333;
  font-weight: bold;
  padding: 16px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  text-align: center;
}

.right-area {
  flex: 2;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.box {
  background-color: #f9f9f9;
  border-radius: 16px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  padding: 24px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.box-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.box-title {
  font-size: 16px;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.preview-list {
  list-style: none;
  padding: 0;
  margin: 0;
  
}

.preview-item {
  padding: 12px 16px;
  border-radius: 8px;
  background-color: #f9f9f9;
  margin-bottom: 8px;
  transition: background-color 0.2s ease;
  box-shadow: 0 2px 4px 2px rgba(0, 0, 0, 0.1);
}

.preview-item:hover {
  background-color: #f1f5ff;
}

.policy-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.policy-label {
  font-size: 13px;
  color: #0064ff;
  font-weight: 600;
}

.policy-title {
  font-size: 15px;
  font-weight: 500;
  color: #111;
  white-space: nowrap;
  /* overflow: hidden; */
  text-overflow: ellipsis;
}

.login-text {
  font-size: 14px;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin: 10px 0;
}

.signup-link {
  font-size: 14px;
  color: #888;
  text-decoration: none;
  
}

.highlight {
  color: #0064ff;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.subtitle {
  font-size: 14px;
  color: #666;
  margin-bottom: 16px;
}

.links {
  display: flex;
  justify-content: center;
  gap: 12px;
  font-size: 13px;
  font-weight: bold;
  color: #666;
}

.links a,
.links a:visited {
  color: #666;
  text-decoration: none; /* 필요 시 밑줄 제거 */
}


.welcome-message {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  text-align: center;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.welcome-icon {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 6px;
}
.login-actions {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px; /* 로그인 버튼과 회원가입 링크 간격 */
  margin-top: 10px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>