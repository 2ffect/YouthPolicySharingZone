<template>
  <header>
    <nav class="navbar">
      <div class="nav-left">
        <RouterLink :to="{ name: 'home' }" class="logo">
          <img src="/logo.png" alt="로고" class="logo-img" />
        </RouterLink>
        <RouterLink class="nav-item" :to="{ name: 'finance_policy' }">청년정책</RouterLink>
        <RouterLink class="nav-item" :to="{ name: 'map' }">청년센터찾기</RouterLink>
        <span class="nav-item nav-link" @click="goToCommunity">커뮤니티</span>
      </div>
      <div class="nav-right">
        <template v-if="accountStore.isLogin">
          <button @click.prevent="userinfo">마이페이지</button>|
          <button @click.prevent="logout">로그아웃</button>
        </template>
        <template v-else>
          <RouterLink :to="{ name: 'signup' }">
            <button>회원가입</button></RouterLink>|
          <RouterLink :to="{ name: 'login' }">
            <button>로그인</button>
          </RouterLink>
        </template>
      </div>
    </nav>
  </header>
  <RouterView />
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts.js'

const accountStore = useAccountStore()
const router = useRouter()

const logout = () => accountStore.logOut()

const userinfo = () => {
  const shouldRedirect = true
  accountStore.getUserInfo(shouldRedirect)
}

const goToCommunity = () => {
  if (!accountStore.isLogin) {
    alert('로그인해야 이용 가능합니다.')
    return
  }
  router.push({ name: 'community' })
}
</script>

<style scoped>
a,
a:visited,
a:active,
a:focus {
  text-decoration: none; /* 모든 링크 기본 밑줄 제거 */
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 32px;
  border-bottom: 1px solid #e6eaf2;
  background-color: #ffffff;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
  max-width: 1280px;
  margin: 0 auto;
  /* border-radius: 0 0 12px 12px; */
  /* box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04); */
  box-sizing: border-box;
}

.nav-left,
.nav-right {
  display: flex;
  gap: 10px;
  align-items: center;
}

.logo-img {
  height: 60px;
  width: auto;
  display: block;
}


.nav-link,
.nav-item { 
  text-decoration: none;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
  color: #333;
  font-weight: 600;
  font-size: 18px;
  padding: 10px 10px;
  border-radius: 8px;
  transition: background-color 0.2s ease, transform 0.1s ease, box-shadow 0.1s ease;
  box-shadow: inset 0 0 0 transparent;
}

.nav-right button {
  all: unset;
  background-color: #ffffff;
  color: #333;
  font-size: 13px;
  font-weight: bold;
  border-radius: 8px;
  padding: 6px 6px;
  cursor: pointer;
  text-align: center;
  transition: transform 0.1s ease, box-shadow 0.1s ease;
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); 살짝 튀어나온 느낌 */
}

.nav-right button:hover {
  transform: translateY(1px);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.12); /* 눌리는 느낌 */
  background-color: #f0f0f0; /* 약간 눌린 느낌 강조 (선택사항) */
}

.nav-item:hover,
.nav-link:hover,
.nav-right button:hover,
.nav-right .nav-item:hover {
  background-color: #eef4ff;
  color: #0064ff;
  transform: translateY(1px);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.12);
}

button {
  all: unset;
  background-color: #0064ff;
  color: white;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  padding: 10px 18px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.2s ease, transform 0.1s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-decoration: none;
}

button:hover {
  background-color: #0053d6;
  transform: scale(0.98);
}

button:active {
  transform: scale(0.95);
}

@media (max-width: 900px) {
  .navbar {
    flex-direction: column;
    padding: 16px 12px;
  }
  .nav-left,
  .nav-right {
    flex-direction: column;
    gap: 12px;
  }
}
</style>