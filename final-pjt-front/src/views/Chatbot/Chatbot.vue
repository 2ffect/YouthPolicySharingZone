<template>
  <div class="chatbot-container">
    <div class="messages" ref="messagesContainer">
      <div v-for="(msg, idx) in messages" :key="idx" :class="['message', msg.role]">
        <span>{{ msg.role === 'user' ? '🙋' : '🤖' }}</span>

        <!-- 일반 텍스트 응답 -->
        <div v-if="msg.type === 'text'" v-html="formatGPTText(msg.content || msg.reply)" />

        <!-- 정책 추천 응답 -->
        <template v-else-if="msg.type === 'recommend' && msg.reply">
          <div>
            <strong>• DB 기반 추천 정책:</strong>
            <ul>
              <li v-for="(title, i) in msg.reply.db_policies" :key="i">- {{ title }}</li>
            </ul>
          </div>
          <div>
            <strong>• AI 추가 추천:</strong>
            <p v-html="formatGPTText(msg.reply.gpt_supplement)" />
          </div>
        </template>
      </div>

      <div ref="bottomRef"></div>

      <div v-if="loading" class="message assistant loading">
        <span>🤖</span><span class="skeleton"></span>
      </div>
    </div>

    <form @submit.prevent="handleSend" class="input-area">
      <input
        :value="input"
        @input="updateInput($event)"
        type="text"
        placeholder="질문을 입력하세요"
        :disabled="loading"
        @keydown.enter.exact.prevent="handleSend"
      />
      <button type="submit" :disabled="loading || !input.trim()">전송</button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import { useChatbotStore } from '@/stores/chatbot'
import { useRouter } from 'vue-router'

const store = useChatbotStore()
const messages = ref([])
const input = ref('')
const loading = ref(false)
const router = useRouter()
const bottomRef = ref(null)

// GPT 응답 줄바꿈 처리
const formatGPTText = (text) => {
  return text
    .replace(/([^\n])\.(\s|$)/g, '$1.<br>')       // 마침표 후 줄바꿈
    .replace(/([^\n]):(\s|$)/g, '$1:<br>')         // 콜론 후 줄바꿈
    .replace(/•/g, '<br>•')                        // • 항목 줄바꿈
    .replace(/^- /gm, '<br>- ')                    // - 항목 줄바꿈
    .replace(/\n/g, '<br>')                        // 기타 줄바꿈
}

// 입력 값 갱신
const updateInput = (e) => {
  input.value = e.target.value
}

// 메시지 전송
const handleSend = async () => {
  const trimmed = input.value.trim()
  if (!trimmed) return alert('메시지를 입력하세요.')
  if (loading.value) return

  const userInput = trimmed
  input.value = ''
  messages.value.push({ role: 'user', type: 'text', content: userInput })
  loading.value = true

  try {
    const response = await store.sendMessage(messages.value)

    if (response.type === 'recommend') {
      messages.value.push({
        role: 'assistant',
        type: 'recommend',
        reply: response.reply
      })
    } else {
      messages.value.push({
        role: 'assistant',
        type: 'text',
        content: response.reply || '응답이 비어 있습니다.'
      })
    }

  } catch (err) {
    const msg = err.response?.data?.error
    if (msg?.includes('신상정보')) {
      alert(msg)
      router.push('/chatbot/profile')
    } else {
      messages.value.push({ role: 'assistant', type: 'text', content: '오류가 발생했습니다.' })
    }
  } finally {
    loading.value = false
  }
}

// 스크롤 자동 이동
watch(messages, async () => {
  await nextTick()
  bottomRef.value?.scrollIntoView({ behavior: 'smooth' })
}, { deep: true })
</script>

<style scoped>
.chatbot-container {
  display: flex;
  flex-direction: column;
  height: 750px;
  max-height: 750px; /* 부모 크기 안에서 제한되게 함 */
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  padding: 0;
  overflow: hidden; /* 자식이 넘치지 않게 */
}

.messages {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
  overscroll-behavior: contain;
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
  max-height: 100%; /* 내부에서만 스크롤 발생 */
}

.message {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 15px;
  padding: 6px 10px;
  border-radius: 8px;
  max-width: 90%;
  word-break: break-word;
}

.message.user {
  align-self: flex-end;
  background: #e6f0ff;
}

.message.assistant {
  align-self: flex-start;
  background: #f5f5f5;
}

.input-area {
  flex-shrink: 0;
  display: flex;
  gap: 8px;
  padding: 12px 16px 16px 16px;
  border-top: 1px solid #f0f0f0;
  background: #fff;
}

.input-area input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  font-size: 15px;
}

.input-area button {
  background: #0064ff;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0 18px;
  cursor: pointer;
  font-size: 15px;
}

.skeleton {
  display: inline-block;
  width: 80px;
  height: 16px;
  background: linear-gradient(90deg, #eee 25%, #ddd 50%, #eee 75%);
  background-size: 200% 100%;
  animation: loading 1.2s infinite linear;
  border-radius: 4px;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
