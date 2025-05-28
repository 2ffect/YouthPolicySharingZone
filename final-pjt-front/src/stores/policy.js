import axios from 'axios'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import { useAccountStore } from './accounts'


export const usePolicyStore = defineStore('policy', () => {
  const accountStore = useAccountStore()
  const policies = ref([])
  const policy = ref([])
  const token = computed(()=> accountStore.token)
  console.log(token.value)
  const isPolicyScrapped = ref(false)

  const POLICY_API_URL = 'http://127.0.0.1:8000/policy'
  const getAllPolicies = function(){
    axios({
        method: 'post',
        url: `${POLICY_API_URL}/save/`,
    })
    .then(res => {
        console.log(res)
        console.log('정책 저장 완료')
    })

  }
  const getPolicies = function(keyword){
    axios({
        method: 'get',
        url: `${POLICY_API_URL}/${keyword}/`,
    })
    .then(res => {
        console.log(res)
        console.log('정책 불러오기 완료')
        policies.value = res.data
    })
    .catch(err => console.log(err))
  }

  const getPolicy = function(policy_id){
    axios({
      method: 'get',
      url: `${POLICY_API_URL}/policy_detail/${policy_id}/`,
    })
    .then(res => {
      console.log(res)
      console.log('정첵 디테일 가져오기 성공')
      policy.value = res.data
    })
    .catch( err => console.log(err.data))
  }

  const scrapPolicy = function(policy_id){
    axios({
      method: 'post',
      url: `${POLICY_API_URL}/policy_detail/${policy_id}/scrap/`,
      headers: {
          Authorization: `Token ${token.value}`
        }
    })
    .then(res => {
      console.log(res)
      console.log('스크랩 성공')
      isPolicyScrapped.value = true

    })
    .catch(err => console.log(err.data))
  }

  const unscrapPolicy = function(policy_id){
    axios({
      method: 'delete',
      url: `${POLICY_API_URL}/policy_detail/${policy_id}/scrap/`,
      headers: {
          Authorization: `Token ${token.value}`
        }
    })
    .then(res => {
      console.log(res)
      console.log('스크랩 취소')
      isPolicyScrapped.value = false
    })
    .catch(err => console.log(err))
  }

  // scrap 여부 확인
  const checkIfScrapped = async (policy_id) => {
    try {
      const res = await axios.get(`${POLICY_API_URL}/policy_detail/${policy_id}/is_scrapped/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      isPolicyScrapped.value = res.data.is_scrapped
      
    } catch (err) {
      console.error('스크랩 여부 확인 실패', err)
      isPolicyScrapped.value = false
    }
  }

  return { 
    policies, policy, isPolicyScrapped,
    getAllPolicies,
    getPolicies, getPolicy,
    scrapPolicy, unscrapPolicy, checkIfScrapped,
  }
}, { persist: true })
