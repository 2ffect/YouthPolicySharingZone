import axios from 'axios'
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const FINANCE_API_URL = 'http://localhost:8000/finances'

// 데이터 저장 요청 함수
export function saveDepositData() {
  return axios.get(`${FINANCE_API_URL}/deposit-products/save/`)
    .then(res => {
      console.log('예금 상품 데이터 저장 완료', res.data)
      return res
    })
    .catch(err => {
      console.error('예금 상품 데이터 저장 오류', err)
      throw err
    })
}

export function saveSavingData() {
  return axios.get(`${FINANCE_API_URL}/saving-products/save/`)
    .then(res => {
      console.log('적금 상품 데이터 저장 완료', res.data)
      return res
    })
    .catch(err => {
      console.error('적금 상품 데이터 저장 오류', err)
      throw err
    })
}

// 전체 은행 목록 조회
export function fetchBanks() {
  return axios.get(`${FINANCE_API_URL}/banks/`)
}

// 예금 상품 조회 (은행 필터 적용 가능)
export function fetchDepositProducts(bank = '') {
  return saveDepositData().then(() => {
    const url = bank ? `${FINANCE_API_URL}/deposit-products/?bank=${bank}` : `${FINANCE_API_URL}/deposit-products/`
    return axios.get(url)
  })
}

// 적금 상품 조회 (은행 필터 적용 가능)
export function fetchSavingProducts(bank = '') {
  return saveSavingData().then(() => {
    const url = bank ? `${FINANCE_API_URL}/saving-products/?bank=${bank}` : `${FINANCE_API_URL}/saving-products/`
    return axios.get(url)
  })
}

export const useExchangeStore = defineStore('exchange',()=>{
  const exchange = ref('')
  const saveExchangeRate = function(){
    axios({
      method: 'get',
      url: `${FINANCE_API_URL}/exchange/save/`
    })
    .then(res => { 
      console.log(res)
      console.log('환율정보 저장완료')
    })
    .catch(err => console.log(err))
  }

  const getExchange = function(){
    axios({
      method: 'get',
      url: `${FINANCE_API_URL}/exchange/`
    })
    .then(res => {
      console.log(res)
      exchange.value = res.data
      console.log('환율 정보 불러오기 완료')
    })
  }

  return {
    exchange,
    saveExchangeRate, getExchange,
  }
}, {persist: true})