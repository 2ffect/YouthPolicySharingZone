
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
  const token = ref('')
  const userInfo = ref('')
  const scrappedPolicy = ref('')
  const scrappedArticle = ref('')
  const mustLoginRedirect = ref(false)

  const ACCOUNT_API_URL = 'http://127.0.0.1:8000/accounts'
  const isLogin = computed(() =>{
    return token.value ? true : false
  })
  const router = useRouter()

  // 로그인 필요 alert 상태 설정
  const setMustLoginRedirect = (value) => {
    mustLoginRedirect.value = value
  }

  const createUser = async function (payload) {
    try {
      const res = await axios({
        method: 'post',
        url: `${ACCOUNT_API_URL}/signup/`,
        data: payload
      })
      console.log(res.data)
      console.log('가입 완료')
      router.push({ name: 'home' })
    } catch (err) {
      // 콘솔에 찍고 반드시 throw로 에러를 상위로 전달
      console.log(err)
      throw err
    }
  }

  const logIn = async function (payload) {
    try {
      const res = await axios({
        method: 'post',
        url: `${ACCOUNT_API_URL}/login/`,
        data: { ...payload }
      })
      token.value = res.data.key
      getUserInfo()
      router.push({ name: 'home' })
    } catch (err) {
      // 콘솔에 찍고 에러를 throw해서 상위에서 catch 가능하게!
      console.log(err)
      throw err
    }
  }


  const logOut = function () {
    axios({
      method: 'post',
      url : `${ACCOUNT_API_URL}/logout/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((res) => {
      console.log('로그아웃 성공')
      token.value = ''
      userInfo.value = null
      router.push({name:'home'})
    })
    .catch(err => console.log(err.data))
  }

  // 마이페이지 클릭 시 유저 정보 가져오기
  const getUserInfo = function (shouldRedirect = false) {
    axios({
      method: 'get',
      url: `${ACCOUNT_API_URL}/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((res) => {
      console.log('유저정보 가져옴')
      console.log(res)
      userInfo.value = res.data

      if (shouldRedirect) {
        router.push({ name: 'user_info' })
      }
    })
    .catch(err => console.log(err))
  }


  // 내가 스크랩 한 정책 클릭 시 스크랩한 정책 가져오기
  const getScrappedPolicy = function(){
    axios({
      method: 'get',
      url : `${ACCOUNT_API_URL}/policy_scrap/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((res)=>{
      console.log('스크랩 정책 가져옴')
      console.log(res)
      scrappedPolicy.value = res.data
      console.log(scrappedPolicy)
    })
    .catch(err => console.log(err))
  }
 
  
  // 내가 스크랩 한 게시글 클릭 시 스크랩한 게시글 가져오기
  const getScrappedArticle = function(){
    axios({
      method: 'get',
      url : `${ACCOUNT_API_URL}/article_scrap/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((res)=>{
      console.log('스크랩 게시글 가져옴')
      console.log(res)
      scrappedArticle.value = res.data
      console.log(scrappedArticle)
    })
    .catch(err => console.log(err))
  }

  const updateInfo = function (payload) {
    axios ({
      method : 'put',
      url: `${ACCOUNT_API_URL}/user/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data : payload
    })
    .then((res) => {
      console.log('유저정보 업데이트 성공')
      console.log(res)
      userInfo.value = res.data
      router.push({name:'user_info'})
    })
    .catch(err => console.log(err))
  }

  const goUpdatePwPage = function () {
    router.push({name:'password_update'})
  }

  const updatePassword = function (payload) {
    axios ({
      method : 'post',
      url : `${ACCOUNT_API_URL}/password/change/`,
      headers : {
        Authorization: `Token ${token.value}`
      },
      data : payload
    })
    .then((res) => {
      console.log('비밀번호 변경 성공')
      console.log(res)
      alert('비밀번호가 변경되었습니다 ! 다시 로그인 해주세요.')
      token.value = ''
      router.push('/login')
    })
    .catch(err => console.log(err))
  }

  return {
    ACCOUNT_API_URL, token, isLogin, userInfo, 
    scrappedPolicy, scrappedArticle,
    createUser, logIn, logOut,
    getUserInfo, updateInfo, goUpdatePwPage, updatePassword, 
    getScrappedPolicy, getScrappedArticle,
    mustLoginRedirect, setMustLoginRedirect,

  }
}, { persist: true })
