<template>
  <div class="main-container">
    <h2 class="highlight">로그인</h2>
    <div class="form-box">
      <form @submit.prevent="onLogIn">
        <label for="email">이메일</label>
        <input
          type="email"
          id="email"
          placeholder="이메일 입력"
          v-model="email"
        />

        <label for="password">비밀번호</label>
        <input
          type="password"
          id="password"
          placeholder="비밀번호 입력"
          v-model="password"
        />

        <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

        <button type="submit">로그인</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const store = useAccountStore()

const onLogIn = async () => {
  if (!email.value || !password.value) {
    alert('이메일과 비밀번호를 모두 입력해주세요.')
    email.value = ''
    password.value = ''
    return
  }

  const userInfo = {
    email: email.value,
    password: password.value,
  }

  try {
    await store.logIn(userInfo)
  } catch (err) {
    if (err.response && err.response.data) {
      const data = err.response.data
      if (data.email && data.email[0].includes('존재하지 않는 이메일')) {
        alert('존재하지 않는 이메일 입니다.')
      } else if (data.non_field_errors && data.non_field_errors[0].includes('이메일 또는 비밀번호가 올바르지 않습니다.')) {
        alert('이메일/비밀번호를 확인해주세요.')
      } else {
        alert('로그인 중 오류가 발생했습니다.')
      }
    } else {
      alert('로그인 중 오류가 발생했습니다.')
    }
    // 입력창 비우기
    email.value = ''
    password.value = ''
  }
}


</script>

<style scoped>
.main-container {
  max-width: 960px;
  margin: 2rem auto;
  padding: 0 16px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

.highlight {
  font-size: 1.8rem;
  color: #0064ff;
  margin-bottom: 20px;
  text-align: center;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.05);
}

.form-box {
  max-width: 400px;
  margin: 0 auto;
  padding: 24px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

label {
  font-weight: 600;
  font-size: 14px;
  display: block;
  margin-top: 12px;
  margin-bottom: 6px;
  color: #333;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border-radius: 8px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

button {
  width: 100%;
  margin-top: 20px;
  padding: 12px;
  background-color: #0064ff;
  color: white;
  font-weight: bold;
  font-size: 15px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #0053d6;
}

.error-text {
  color: #e74c3c;
  font-size: 13px;
  margin-top: 8px;
}
</style>
