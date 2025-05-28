<template>
  <div class="main-container">
    <h2 class="highlight">회원가입</h2>
    <div class="form-box">
      <form @submit.prevent="signup">
        <label for="email">이메일</label>
        <input type="email" id="email" placeholder="이메일" v-model="email" />
        
        <label for="username">이름</label>
        <input type="text" id="username" placeholder="이름" v-model="username" />

        <label for="nickname">닉네임</label>
        <input type="text" id="nickname" placeholder="닉네임" v-model="nickname" />

        <label for="password1">비밀번호</label>
        <input type="password" id="password1" placeholder="8자 이상 입력" v-model="password1" />

        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" placeholder="비밀번호 확인" v-model="password2" />

        <label for="phonenum">전화번호</label>
        <input type="text" id="phonenum" placeholder="숫자만 입력" v-model="phonenum" />

        <label for="birthdate">생년월일</label>
        <input type="date" id="birthdate" v-model="birthdate" />

        <label>성별</label>
        <select v-model="gender">
          <option disabled value="">성별 선택</option>
          <option value="M">남자</option>
          <option value="F">여자</option>
        </select>

        <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>

        <button type="submit">회원가입</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/accounts.js'

const email = ref('')
const username = ref('')
const nickname = ref('')
const password1 = ref('')
const password2 = ref('')
const phonenum = ref('')
const birthdate = ref('')
const gender = ref('')
const errorMsg = ref('')

const store = useAccountStore()

const signup = async () => {
  errorMsg.value = ''

  // 프론트 유효성 검사
  if (!email.value || !username.value || !nickname.value || !password1.value || !password2.value || !phonenum.value || !birthdate.value || !gender.value) {
    errorMsg.value = '모든 항목을 입력해주세요.'
    return
  }
  if (password1.value.length < 8) {
    errorMsg.value = '비밀번호는 최소 8자 이상이어야 합니다.'
    return
  }
  if (password1.value !== password2.value) {
    errorMsg.value = '비밀번호가 일치하지 않습니다.'
    return
  }
  if (!/^\d{10,11}$/.test(phonenum.value)) {
    errorMsg.value = '전화번호는 숫자만 입력하며 10~11자리여야 합니다.'
    return
  }

  const userInfo = {
    email: email.value,
    username: username.value,
    nickname: nickname.value,
    password1: password1.value,
    password2: password2.value,
    phonenum: phonenum.value,
    birthdate: birthdate.value,
    gender: gender.value,
  }

  try {
    await store.createUser(userInfo)
  } catch (err) {
    // 서버 응답 에러 처리
    if (err.response && err.response.data) {
      const data = err.response.data
      if (data.email) {
        errorMsg.value = data.email[0]   // "이미 사용 중인 이메일입니다."
      } else if (data.username) {
        errorMsg.value = data.username[0] // "이미 사용 중인 이름입니다."
      } else if (data.nickname) {
        errorMsg.value = data.nickname[0]
      } else if (data.phonenum) {
        errorMsg.value = data.phonenum[0]
      } else if (data.password1) {
        errorMsg.value = data.password1[0]
      } else if (data.non_field_errors) {
        errorMsg.value = data.non_field_errors[0]
      } else {
        errorMsg.value = '회원가입 중 오류가 발생했습니다.'
      }
    } else {
      errorMsg.value = '서버와의 통신에 실패했습니다.'
    }
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

input,
select {
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
  margin-top: 10px;
}
</style>
