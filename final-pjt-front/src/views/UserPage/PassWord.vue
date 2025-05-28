<template>
  <div class="main-container">
    <h2 class="highlight">비밀번호 변경</h2>

    <div class="form-box">
      <form @submit.prevent="updatePW">
        <label for="password1">새 비밀번호</label>
        <input
          type="password"
          id="password1"
          placeholder="8자 이상 입력하세요"
          v-model="password1"
        />
        <label for="password2">비밀번호 확인</label>
        <input
          type="password"
          id="password2"
          placeholder="다시 한 번 입력하세요"
          v-model="password2"
        />
        <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>
        <button type="submit">비밀번호 변경</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()
const password1 = ref('')
const password2 = ref('')
const errorMsg = ref('')

const updatePW = () => {
  errorMsg.value = ''

  if (password1.value.length < 8) {
    errorMsg.value = '비밀번호는 최소 8자 이상이어야 합니다.'
    return
  }

  if (password1.value !== password2.value) {
    errorMsg.value = '비밀번호가 일치하지 않습니다.'
    return
  }

  const userInfo = {
    new_password1: password1.value,
    new_password2: password2.value,
  }

  accountStore.updatePassword(userInfo)
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
