<template>
  <div class="main">
    <!-- 상단 버튼 (목록 + 스크랩) -->
    <div class="top-actions">
      <RouterLink :to="{ name: 'community' }">
        <button class="btn">목록 보기</button>
      </RouterLink>
      <div class="scrap-btn">
        <button class="btn" v-if="communityStore.isScrapped" @click.prevent="onUnscrapArticle">스크랩 취소</button>
        <button class="btn" v-else @click.prevent="onScrapArticle">스크랩 하기</button>
      </div>
    </div>

    <!-- 게시글 영역 -->
    <div class="article-area">
      <div class="article-card">
        <div class="article-header">
          <h2 class="article-title">{{ communityStore.article.title }}</h2>
          <div class="article-meta">
            <div>
              <span>작성자: {{ communityStore.article.nickname }}</span>
              <span class="meta-divider">|</span>
              <span>작성일: {{ formatDateTime(communityStore.article.created_at) }}</span>
            </div>
          </div>
        </div>

        <div class="article-content">
          <p>{{ communityStore.article.content }}</p>
        </div>

        <div v-if="isArticleAuthor" class="author-controls">
          <RouterLink :to="{ name: 'article_update', params: { article_id: communityStore.article.id }}">
            <button class="btn auth">수정</button>
          </RouterLink>
          <button class="btn auth" @click.prevent="onDeleteArticle">삭제</button>
        </div>
      </div>
    </div>

    <!-- 댓글 -->
    <div class="comment-section">
      <h3>댓글</h3>
      <div v-for="comment in communityStore.comments" :key="comment.id" class="comment-card">
        <p>
          <strong>{{ comment.nickname }}</strong> : {{ comment.content }}
          <span class="comment-date">{{ formatDateTime(comment.created_at) }}</span>
          <span v-if="isCommentAuthor(comment)">
            <button class="comment-delete" @click.prevent="onDeleteComment(comment.id)">삭제</button>
          </span>
        </p>
      </div>

      <!-- 댓글 작성 -->
      <form class="comment-form" @submit.prevent="onCreateComment">
        <div class="comment-input-row">
          <textarea v-model="commentContent" placeholder="댓글을 입력하세요"></textarea>
          <button type="submit" class="comment-btn">댓글 작성</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'
import { useCommunityStore } from '@/stores/community.js'

const route = useRoute()
const communityStore = useCommunityStore()
const accountStore = useAccountStore()
const commentContent = ref('')

// 날짜 포맷 함수
const formatDateTime = (isoString) => {
  const date = new Date(isoString)
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const min = String(date.getMinutes()).padStart(2, '0')
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`
}

// 게시글 작성자 여부
const isArticleAuthor = computed(() => {
  return (
    accountStore.userInfo &&
    communityStore.article &&
    accountStore.userInfo.id === communityStore.article.user_id
  )
})

// 게시글 삭제
const onDeleteArticle = function () {
  communityStore.deleteArticles(route.params.article_id)
}

// 댓글 작성자 여부
const isCommentAuthor = (comment) => {
  return accountStore.userInfo && comment.nickname === accountStore.userInfo.nickname
}

// 댓글 작성
const onCreateComment = async () => {
  const commentInfo = { content: commentContent.value }
  await communityStore.createComment(commentInfo, route.params.article_id)
  commentContent.value = ''
  await communityStore.getComments(route.params.article_id)
}

// 댓글 삭제
const onDeleteComment = async (comment_id) => {
  const article_id = route.params.article_id
  await communityStore.deleteComment(article_id, comment_id)
  await communityStore.getComments(article_id)
}

// 스크랩/스크랩 취소
const onScrapArticle = () => {
  communityStore.scrapArticle(route.params.article_id)
}
const onUnscrapArticle = () => {
  communityStore.unscrapArticle(route.params.article_id)
}

// 페이지 진입 시 데이터 로딩
onMounted(() => {
  communityStore.getArticle(route.params.article_id)
  communityStore.getComments(route.params.article_id)
  communityStore.checkIfScrapped(route.params.article_id)
})
</script>

<style scoped>
.main {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px;
  font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}

/* ✅ 상단 버튼 (목록 + 스크랩) 같은 줄 정렬 */
.top-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.top-actions a{
  text-decoration: none;
}
.article-area {
  /* width: 100%; */
  display: flex;
  background-color: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin-bottom: 32px;
}

.article-card {
  width: 100%;
}

.article-header {
  margin-bottom: 16px;
}

.article-title {
  font-size: 22px;
  color: #333;
  margin-bottom: 8px;
}

.article-meta {
  font-size: 14px;
  color: #777;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.meta-divider {
  margin: 0 8px;
  color: #ccc;
}

.article-content {
  font-size: 16px;
  line-height: 1.6;
  color: #444;
  margin-bottom: 20px;
  margin-top: 20px;
}

.author-controls {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  margin-top: 10px;
}

.author-controls a {
  text-decoration: none;
}

.scrap-btn {
  display: flex;
  gap: 8px;
}

.btn {
  all: unset;
  background-color: #0064ff;
  color: white;
  font-size: 14px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  margin-right: 8px;
}

.btn:hover {
  background-color: #0053d6;
}

.btn.auth {
  background-color: #999;
}

.btn.auth:hover {
  background-color: #666;
}

.btn.delete:hover {
  background-color: #c0392b;
}

/* 댓글 영역 */
.comment-section {
  padding: 0px;
  background-color: #ffffff;
  width: 100%;
  border-radius: 12px;
  margin-bottom: 32px;
}

.comment-card {
  padding: 3px 0;
  border-bottom: 1px solid #ddd;
}

.comment-date {
  font-size: 12px;
  color: #999;
  margin-left: 10px;
}

.comment-delete {
  all: unset;
  margin-left: 10px;
  color: #e74c3c;
  cursor: pointer;
  font-size: 13px;
}

/* 댓글 입력 */
.comment-form {
  margin-top: 20px;
  width: 100%;
}

.comment-input-row {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  width: 100%;
}

.comment-input-row textarea {
  flex: 1;
  min-height: 80px;
  resize: vertical;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.comment-input-row .comment-btn {
  white-space: nowrap;
  /* height: 100%; */
  min-height: 100px;
  background-color: #0064ff;
  color: white;
  font-size: 14px;
  font-weight: 600;
  padding: 0 16px;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  align-self: flex-start;
  padding-top: 10;
}
</style>
