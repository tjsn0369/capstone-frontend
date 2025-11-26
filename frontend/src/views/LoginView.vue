<template>
  <div class="center-container">
    <div class="glow-bg"></div>
    <div class="login-card">
      <h1 class="title">CV-DLOps</h1>
      <p class="subtitle">AI Project Management System</p>
      
      <div class="form-group">
        <label>Email ID</label>
        <div class="input-wrapper">
          <input v-model="email" type="text" placeholder="user@dlops.com" />
        </div>
      </div>

      <div class="form-group">
        <label>Password</label>
        <div class="input-wrapper">
          <input v-model="password" type="password" placeholder="••••••••" @keyup.enter="handleLogin" />
        </div>
      </div>

      <button @click="handleLogin" class="btn-primary">Sign In</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const email = ref('');
const password = ref('');

const handleLogin = () => {
  if (!email.value || !password.value) return alert("Please enter ID & Password");
  router.push('/projects');
};
</script>

<style scoped>
.center-container { display: flex; justify-content: center; align-items: center; height: 100vh; background: #0b1021; position: relative; overflow: hidden; }
.glow-bg { position: absolute; width: 600px; height: 600px; background: radial-gradient(circle, rgba(59,130,246,0.15) 0%, transparent 70%); top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 0; }
.login-card { background: rgba(255,255,255,0.03); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); padding: 50px 40px; border-radius: 16px; width: 100%; max-width: 380px; text-align: center; z-index: 1; }
.title { color: white; font-size: 2rem; margin-bottom: 5px; font-weight: bold; }
.subtitle { color: #94a3b8; font-size: 0.9rem; margin-bottom: 40px; }
.form-group { text-align: left; margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-size: 0.85rem; color: #cbd5e1; }
.input-wrapper input { width: 100%; padding: 14px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: white; outline: none; box-sizing: border-box; }
.input-wrapper input:focus { border-color: #3b82f6; }
.btn-primary { width: 100%; padding: 14px; background: linear-gradient(90deg, #3b82f6, #2563eb); color: white; border: none; border-radius: 8px; font-size: 1rem; font-weight: bold; cursor: pointer; margin-top: 10px; }
</style>