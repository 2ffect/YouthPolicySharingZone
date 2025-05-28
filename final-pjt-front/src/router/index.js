import SignUpView from '@/views/UserPage/SignUpView.vue'
import LogInView from '@/views/UserPage/LogInView.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/accounts'

import Home from '@/components/Home.vue'
import Policy from '@/components/Policy.vue'
import Map from '@/components/Map.vue'
import Community from '@/components/Community.vue'
import User from '@/components/User.vue'
import UserInfo from '@/views/UserPage/UserInfo.vue'
import PolicyScrap from '@/views/UserPage/PolicyScrap.vue'
import ArticleScrap from '@/views/UserPage/ArticleScrap.vue'
import PassWord from '@/views/UserPage/PassWord.vue'
import ArticleDetail from '@/views/Community/ArticleDetail.vue'
import ArticleCreate from '@/views/Community/ArticleCreate.vue'
import ArticleUpdate from '@/views/Community/ArticleUpdate.vue'
// import PolicyMain from '@/views/Policy/PolicyMain.vue'
import FinancePolicy from '@/views/Policy/FinancePolicy.vue'
import JobPolicy from '@/views/Policy/JobPolicy.vue'
import GlobalPolicy from '@/views/Policy/GlobalPolicy.vue'
import Deposit from '@/views/Policy/Finance/Deposit.vue'
import Saving from '@/views/Policy/Finance/Saving.vue'
import Info from '@/views/Policy/Finance/Info.vue'
import FinanceMain from '@/views/Policy/Finance/FinanceMain.vue'
import Chatbot from '@/views/Chatbot/Chatbot.vue'
import PolicyDetail from '@/views/Policy/PolicyDetail.vue'
import ProfileForm from '@/views/Chatbot/ProfileForm.vue'
import Exchange from '@/views/Policy/Finance/Exchange.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
    {
      path: '/policy',
      name: 'policy',
      component: Policy,
      children: [
        // {
        //   path: '',
        //   name: 'policy_main',
        //   component: PolicyMain
        // },
        {
          path: '/finance_policy',
          name: 'finance_policy',
          component: FinancePolicy,
        },
        {
          path: '/job_policy',
          name: 'job_policy',
          component: JobPolicy
        },
        {
          path: '/global_policy',
          name: 'global_policy',
          component: GlobalPolicy
        },
        {
          path: '/finance',
          name: 'financemain',
          component: FinanceMain,
          children: [
            {
              path: '',
              name: 'deposit',
              component: Deposit
            },
            {
              path: '/finance_saving',
              name: 'saving',
              component: Saving,
            },
            {
              path: '/finance_info',
              name: 'info',
              component: Info,
            },
            {
              path: '/exchange',
              name: 'exchange',
              component: Exchange
            }
          ]
        },
      ]
    },
    // detail 경로 하나로 합치기
    {
      path: '/policy_detail/:policy_keyword/:policy_id',
      name: 'policy_detail',
      component: PolicyDetail
    },
    {
      path: '/map',
      name: 'map',
      component: Map
    },
    {
      path: '/community',
      name: 'community',
      component: Community,
      // children: [
      //   {
      //     path: '/article_create',
      //     name: 'article_create',
      //     component: ArticleDetail
      //   }
      // ]
    },
    {
      path: '/article_create',
      name: 'article_create',
      component: ArticleCreate
    },
    {
      path: '/article_detail/:article_id',
      name: 'article_detail',
      component: ArticleDetail
    },
    {
      path: '/article_update/:article_id',
      name: 'article_update',
      component: ArticleUpdate
    },
    {
      path: '/user',
      component: User,
      children: [
        {
          path: '/user',
          name: 'user_info',
          component: UserInfo
        },
        {
          path: '/policy_scrap',
          name: 'policy_scrap',
          component: PolicyScrap
        },
        {
          path: '/article_scrap',
          name: 'article_scrap',
          component: ArticleScrap
        },
        {
          path: '/user_pw',
          name: 'password_update',
          component: PassWord
        }
      ]
    },
    {
      path: '/chatbot',
      name: 'chatbot',
      component: Chatbot
    },
    {
      path: '/chatbot/profile',
      name: 'chatbot_profile',
      component: ProfileForm
    }
  ],
  
})

// 비로그인 상태로 커뮤니티 접근 시 홈으로 돌려보내기
router.beforeEach((to, from, next) => {
  const store = useAccountStore()
  // 커뮤니티 메인 접근 차단
  if (to.name === 'community' && !store.isLogin) {
    store.setMustLoginRedirect(true)
    return next({ name: 'login' })
  }
  // 게시글 상세(예: article_detail) 접근 차단
  if (to.name === 'article_detail' && !store.isLogin) {
    store.setMustLoginRedirect(true)
    return next({ name: 'login' })
  }
  next()
})

export default router
