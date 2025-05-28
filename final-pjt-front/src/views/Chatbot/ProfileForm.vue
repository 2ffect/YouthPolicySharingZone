<template>
  <div class="profile-form">
    <h2>추가정보 입력</h2>
    <form @submit.prevent="submitProfile">
      <label>
        나이:
        <input type="number" v-model.number="age" required />
      </label>

      <label>
        지역:
        <select v-model="region" required>
          <option disabled value="">-- 선택하세요 --</option>
          <option v-for="(name, code) in REGION_MAP" :key="code" :value="code">{{ name }}</option>
        </select>
      </label>

      <label>
        학력:
        <select v-model="education" required>
          <option disabled value="">-- 선택하세요 --</option>
          <option v-for="(name, code) in SCHOOL_CD_MAP" :key="code" :value="code">{{ name }}</option>
        </select>
      </label>

      <label>
        취업 상태:
        <select v-model="job_status" required>
          <option disabled value="">-- 선택하세요 --</option>
          <option v-for="(name, code) in JOB_CD_MAP" :key="code" :value="code">{{ name }}</option>
        </select>
      </label>

      <label>
        결혼 여부:
        <select v-model="marital_status" required>
          <option disabled value="">-- 선택하세요 --</option>
          <option v-for="(name, code) in MRG_STTS_CD_MAP" :key="code" :value="code">{{ name }}</option>
        </select>
      </label>

      <button type="submit">저장</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

const router = useRouter()
const store = useAccountStore()

// 입력 폼
const age = ref('')
const region = ref('')
const education = ref('')
const job_status = ref('')
const marital_status = ref('')


// 코드 → 라벨 매핑
const REGION_MAP = {
  '11': '서울특별시', '26': '부산광역시', '27': '대구광역시', '28': '인천광역시',
  '29': '광주광역시', '30': '대전광역시', '31': '울산광역시', '36': '세종특별자치시',
  '41': '경기도', '51': '강원도', '43': '충청북도', '44': '충청남도',
  '52': '전라북도', '46': '전라남도', '47': '경상북도', '48': '경상남도', '50': '제주특별자치도'
}

const SCHOOL_CD_MAP = {
  '0049001': '고졸 미만', '0049002': '고교 재학', '0049003': '고졸 예정',
  '0049004': '고교 졸업', '0049005': '대학 재학', '0049006': '대졸 예정',
  '0049007': '대학 졸업', '0049008': '석·박사',
}

const JOB_CD_MAP = {
  '0013001': '재직자', '0013002': '자영업자', '0013003': '미취업자',
  '0013004': '프리랜서', '0013005': '일용근로자', '0013006': '(예비)창업자',
  '0013007': '단기근로자', '0013008': '영농종사자'
}

const MRG_STTS_CD_MAP = {
  '0055001': '기혼', '0055002': '미혼'
}


// 제출 요청
const submitProfile = async () => {
  const payload = {
    age: age.value,
    region: region.value,
    education: education.value,
    employment_status: job_status.value,
    marital_status: marital_status.value
  }

  // 입력값 누락 여부 검사
  if (!payload.age || payload.age <= 0) {
    alert('나이를 올바르게 입력해주세요.')
    return
  }
  if (!payload.region) {
    alert('지역을 선택해주세요.')
    return
  }
  if (!payload.education) {
    alert('학력을 선택해주세요.')
    return
  }
  if (!payload.employment_status) {
    alert('취업 상태를 선택해주세요.')
    return
  }
  if (!payload.marital_status) {
    alert('결혼 여부를 선택해주세요.')
    return
  }

  try {
    await axios.post('http://localhost:8000/chatbot/profile/', payload, {
      headers: { Authorization: `Token ${store.token}` }
    })
    alert('신상정보가 저장되었습니다.')
    router.push('/')
  } catch (err) {
    alert('신상정보 저장 중 오류가 발생했습니다.')
    console.error(err)
  }
}

</script>

<style scoped>
.profile-form {
  max-width: 500px;
  margin: 0 auto;
  padding: 24px;
  background: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
label {
  display: block;
  margin-bottom: 12px;
  font-size: 14px;
}
input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
}
button {
  margin-top: 16px;
  background: #0064ff;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
}
</style>
