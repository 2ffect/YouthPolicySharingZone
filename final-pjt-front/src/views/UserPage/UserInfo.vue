<template>
  <div class="main-container">
    <h2 class="highlight">개인 정보 수정</h2>

    <div class="form-box">
      <form @submit.prevent="updateinfo">
        <label for="email">이메일</label>
        <input type="email" id="email" :value="user.email" disabled />

        <label for="username">이름</label>
        <input type="text" id="username" :value="user.username" disabled />

        <label for="nickname">닉네임</label>
        <input type="text" id="nickname" v-model="nickname" />
        <p v-if="nicknameError" class="error-text">{{ nicknameError }}</p>

        <label for="phonenum">전화번호</label>
        <input type="text" id="phonenum" v-model="phonenum" />
        <p v-if="phonenumError" class="error-text">{{ phonenumError }}</p>

        <label for="birthdate">생년월일</label>
        <input type="date" id="birthdate" :value="user.birthdate" disabled />

        <label>성별</label>
        <select :value="user.gender" disabled>
          <option disabled value="">성별 선택</option>
          <option value="M">남자</option>
          <option value="F">여자</option>
        </select>

        <button type="submit">정보 수정 하기</button>
      </form>

      <button @click.prevent="goUpdatePw" class="secondary-btn">비밀번호 변경</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAccountStore } from '@/stores/accounts'

const accountStore = useAccountStore()
const user = computed(() => accountStore.userInfo)

const nickname = ref('')
const phonenum = ref('')
const password = ref('')

const nicknameError = ref('')
const phonenumError = ref('')

const updateinfo = () => {
  nicknameError.value = ''
  phonenumError.value = ''

  // 닉네임 검사
  if (!nickname.value.trim()) {
    nicknameError.value = '닉네임을 입력해주세요.'
    return
  }

  // 전화번호 검사
  const phonePattern = /^[0-9]{10,11}$/
  if (!phonePattern.test(phonenum.value)) {
    phonenumError.value = '전화번호는 숫자만 입력하며 10~11자리여야 합니다.'
    return
  }

  const userInfo = {
    nickname: nickname.value,
    password: password.value,
    phonenum: phonenum.value
  }
  accountStore.updateInfo(userInfo)
}

const goUpdatePw = () => {
  accountStore.goUpdatePwPage()
}

onMounted(() => {
  nickname.value = user.value.nickname
  phonenum.value = user.value.phonenum
  password.value = user.value.password
})
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

.secondary-btn {
  background-color: #888;
  margin-top: 12px;
}

.secondary-btn:hover {
  background-color: #666;
}

.error-text {
  color: #e74c3c;
  font-size: 13px;
  margin-top: 4px;
}
</style>
