import axios from 'axios'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import { useAccountStore } from './accounts'


export const useCommunityStore = defineStore('community', () => {
  const accountStore = useAccountStore()
  // accountStore의 token이 이미 ref이기 때문에 그냥 가져와서 쓰기만 하면됨
  // 다시 ref나 computed를 쓰면 이중참조..? 근데 됐음.. 뭥미
  // token은 객체로 넘어옴.. token.value를 token에 넣고, token은 반응형이니까
  // token.value.. 로 해야..
  // 모르겟다.. 
  const token = computed(()=> accountStore.token)
  const articles = ref([])
  // 게시글 디테일
  const article = ref([])
  const router = useRouter()

  const comments = ref([])
  const isScrapped = ref(false)

  console.log(token.value)
  const COMMUNITY_API_URL = 'http://127.0.0.1:8000/community'
  // 게시글 전체 조회
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${COMMUNITY_API_URL}/list/`
    })
    .then(res => {
      console.log(res)
      articles.value = res.data}
    )
  }
  // 게시글 create
  const createArticle = function(payload){
    axios({
      method: 'post',
      url: `${COMMUNITY_API_URL}/article_create/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: payload
    })
    .then(res => {
      console.log(res)
      router.push({name:'community'})
    })
    .catch(err => console.log(err.data))
  }
  // 게시글 디테일 조회
  const getArticle = function(article_id){
    axios({
      method: 'get',
      url: `${COMMUNITY_API_URL}/article_detail/${article_id}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
    .then(res => {
      console.log(res)
      article.value = res.data

    })
    .catch(err => console.log(err))
  }
  
  //게시글 수정
  const updateArticle = function(payload, article_id){
    axios({
      method:'put',
      url: `${COMMUNITY_API_URL}/article_detail/${article_id}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: payload
    })
    .then(res => {
      console.log(res)
      article.value = res.data
      router.push({name:'article_detail', params:{'article_id': article_id}})
    })
    .catch(err => console.log(err.data))
  }

  // 게시글 댓글 가져오기 
  const getComments = function(article_id) {
    axios ({
      method : 'get',
      url : `${COMMUNITY_API_URL}/article_detail/${article_id}/comments/`,
      headers : {
        Authorization: `Token ${token.value}`
      }
    })
    .then(res => {
      console.log('댓글 가져오기 성공')
      console.log(res)
      comments.value = res.data
    })
    .catch(err => console.log(err.data))
  }
  
  // 게시글 삭제
  const deleteArticles = function(article_id){
    axios({
      method: 'delete',
      url: `${COMMUNITY_API_URL}/article_detail/${article_id}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
    .then(res => {
      console.log('게시글 삭제 완료')
      router.push({name: 'community'})
    })
    .catch(err => console.log(err.data))
  }



  // 게시글 댓글 작성하기
  const createComment = async function(payload, article_id) {
    try {
      await axios({
        method: 'post',
        url: `${COMMUNITY_API_URL}/article_detail/${article_id}/comments/`,
        headers: {
          Authorization: `Token ${token.value}`
        },
        data: payload
      })
      console.log('댓글 작성 성공')
      // 댓글 push하지 않고 목록을 새로 가져오세요 (상위에서 호출)
    } catch (err) {
      console.error(err)
    }
  }


  // # 댓글 삭제하기
  //   path('article_detail/<int:article_id>/comment_delete/<int:comment_id>/'
  const deleteComment = async function(article_id, comment_id) {
    try {
      await axios({
        method : 'delete',
        url : `${COMMUNITY_API_URL}/article_detail/${article_id}/comment_delete/${comment_id}/`,
        headers : {
          Authorization: `Token ${token.value}`
        }
      })
      console.log('댓글 삭제 성공')

      // 삭제 후 리스트 갱신
      await getComments(article_id)

    } catch (err) {
      console.error('댓글 삭제 실패', err)
    }
  }

  // 게시글 스크랩 
  const scrapArticle = function(article_id){
    axios({
      method: 'post',
      url : `${COMMUNITY_API_URL}/article_detail/${article_id}/scrap/`,
      headers : {
          Authorization: `Token ${token.value}`
        },
    })
    .then(res => {
      console.log('스크랩 성공')
      console.log(res)
      isScrapped.value = true
    })
    .catch(err => console.log(err))
  }

  // 게시글 스크랩 취소
  const unscrapArticle = function(article_id){
    axios({
      method: 'delete',
      url : `${COMMUNITY_API_URL}/article_detail/${article_id}/scrap/`,
      headers : {
          Authorization: `Token ${token.value}`
        },
    })
    .then(res => {
      console.log('스크랩 취소')
      isScrapped.value = false
    })
    .catch(err => console.log(err.data))
  }

  // scrap 여부 확인
  const checkIfScrapped = async (article_id) => {
    try {
      const res = await axios.get(`${COMMUNITY_API_URL}/article_detail/${article_id}/is_scrapped/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      isScrapped.value = res.data.is_scrapped
    } catch (err) {
      console.error('스크랩 여부 확인 실패', err)
      isScrapped.value = false
    }
  }

  return { 
    articles, article, 
    comments,
    isScrapped,
    getArticles, createArticle, getArticle, updateArticle, deleteArticles,
    getComments, createComment, deleteComment,
    scrapArticle, unscrapArticle, checkIfScrapped,
    
  }
})
