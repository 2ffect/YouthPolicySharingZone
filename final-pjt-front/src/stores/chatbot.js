import axios from 'axios'
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAccountStore } from './accounts'

export const useChatbotStore = defineStore('chatbot', () => {
  const accountStore = useAccountStore()
  const token = computed(() => accountStore.token)
  const CHATBOT_API_URL = 'http://localhost:8000/chatbot/'  // Django 백엔드 API 주소

  // 메시지 전송 함수
  const sendMessage = function (messages) {
    // 잘못된 메시지 필터링
    const filteredMessages = messages.filter((msg) => {
      return msg.role && (msg.content || (msg.reply && typeof msg.reply === 'string'))
    }).map((msg) => {
      return {
        role: msg.role,
        content: msg.content || msg.reply || ''  // reply fallback 허용
      }
    })

    return axios({
      method: 'post',
      url: CHATBOT_API_URL,
      headers: {
        Authorization: `Token ${token.value}`,
        'Content-Type': 'application/json'
      },
      data: {
        messages: filteredMessages
      }
    })
    .then(res => ({
      type: res.data.type,
      reply: res.data.reply
    }))
    .catch(err => {
      console.error('챗봇 응답 오류', err)
      throw err
    })
  }

  const checkProfileInfo = async () => {
    try {
      const res = await axios.get(`${CHATBOT_API_URL}profile/`, {
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      return res.data.is_complete === true
    } catch (err) {
      console.error('프로필 정보 확인 실패', err)
      return false
    }
  }


  return { 
    sendMessage,
    checkProfileInfo,
  }
})
