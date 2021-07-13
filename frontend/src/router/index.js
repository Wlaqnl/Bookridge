import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

//실험
import Kidding from '../views/Kidding.vue'

Vue.use(VueRouter)
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup,
    props: true,
  },
  {
    path: '/profile/:pk',
    name: 'Profile',
    component: Profile,
    props: true,
  },
  {
    path: '/main',
    name: 'Main',
    component: Main,
  },
  {
    path: '/community',
    name: 'Community',
    component: Community,
  },
  {
    path: '/search/:search_word/:search_type',
    name: 'Search',
    component: Search,
    props: true,
  },
  {
    path: '/search2',
    name: 'Search2',
    component: Search2,
  },
  {
    path: '/reviewform',
    name: 'ReviewForm',
    component: ReviewForm,
  },
  {
    path: '/phraseform',
    name: 'PhraseForm',
    component: PhraseForm
  },
  {
    path: '/bookdetail/:pk',
    name: 'BookDetail',
    component: BookDetail,
    props:true,
  },
  {
    path: '/analyze',
    name: 'Analyze',
    component: Analyze
  },
  {
    path: '/oauthgoogle',
    name: 'OauthGoogle',
    component: OauthGoogle
  },
  {
    path: '/oauthkakao',
    name: 'OauthKakao',
    component: OauthKakao
  },
  {
    path:'/kidding',
    name:'Kidding',
    component:Kidding
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
