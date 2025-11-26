import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import ProjectListView from '../views/ProjectListView.vue'
import ProjectCreateView from '../views/ProjectCreateView.vue'
import TrainingView from '../views/TrainingView.vue' // ★ 학습 화면 복구
import ResultView from '../views/ResultView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'login', component: LoginView },
    { path: '/projects', name: 'projectList', component: ProjectListView },
    { path: '/create', name: 'projectCreate', component: ProjectCreateView },
    
    // ★ 학습 화면 경로 복구 (여기서 1초 동안 게이지 참)
    { 
      path: '/project/:id/train', 
      name: 'training', 
      component: TrainingView 
    },
    
    // 결과 화면
    { 
      path: '/project/:id/result', 
      name: 'result', 
      component: ResultView 
    }
  ]
})

export default router