import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/AboutView.vue')
  },
  {
    path: '/test',
    name: 'test',
    component: () => import('../views/test.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/General/Login.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/General/Register.vue')
  },
  {
    path: '/xuanke',
    name: 'xuanke',
    component: () => import('../views/XuanKe/thomas.vue')
  },
  {
    path: '/rili',
    name: 'rili',
    component: () => import('../views/RiLi/RiLi.vue')
  },
  {
    path: '/fudao',
    name: 'fudao',
    component: () => import('../views/FuDao/FuDao.vue')
  },
  {
    path: '/fudao/teacherlist',
    name: 'teacherlist',
    component: () => import('../views/FuDao/TeacherList.vue')
  },
  {
    path: '/fudao/appointmentlist',
    name: 'appointmentlist',
    component: () => import('../views/FuDao/AppointmentList.vue')
  },

  //论坛
  {
    path: '/luntan',
    name: 'luntan',
    component: () => import('../views/LunTan/LunTan.vue')
  },
  {
    path: '/topic/:id',
    name: 'TopicDetail',
    component: () => import('../views/LunTan/TopicDetail.vue')
  },
  //评教系统
  {
    path: '/pingjiao',
    name: 'pingjiao',
    component: () => import('../views/PingJiao/PingJiao.vue')
  },
  {
    path: '/course-detail/:id',
    name: 'coursedetail',
    component: () => import('../views/PingJiao/CourseDetail.vue')
  },
  // 管理员
  {
    path: '/guanli',
    name: 'guanli',
    component: () => import('../views/GuanLi/GuanLi.vue')
  },
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
