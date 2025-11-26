import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router/index.js' // ★ 1. 이 줄이 있는지 확인!

const app = createApp(App)

app.use(router) // ★ 2. 이 줄이 있는지 확인! (이게 없으면 화면 안 나옴)

app.mount('#app')