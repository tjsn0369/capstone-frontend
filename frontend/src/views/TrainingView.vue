<template>
  <div class="page-container">
    <div class="glow-bg"></div>
    
    <div class="window-card">
      
      <div class="window-header">
        <div class="window-title">
          <span class="status-dot pulsing"></span>
          AI MODEL TRAINING
        </div>
        <button class="btn-close-window" @click="closeWindow">✖</button>
      </div>

      <div class="window-body">
        <h2 class="status-message">{{ statusText }}</h2>
        
        <div class="progress-wrapper">
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: progress + '%' }">
              <div class="progress-light"></div>
            </div>
          </div>
          <div class="percent-number">{{ progress }}<span class="small">%</span></div>
        </div>

        <div class="data-grid">
          <div class="data-item">
            <span class="label">EPOCH</span>
            <span class="value">{{ currentEpoch }} / {{ totalEpoch }}</span>
          </div>
          <div class="data-item">
            <span class="label">LOSS</span>
            <span class="value red">{{ currentLoss }}</span>
          </div>
          <div class="data-item">
            <span class="label">ACCURACY</span>
            <span class="value green">{{ currentAcc }}%</span>
          </div>
        </div>
        
        <div class="window-footer">
           <p class="logs">Log: Optimizing weights with AdamW...</p>
           <button class="btn-abort" @click="closeWindow">ABORT</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const progress = ref(0);
const currentEpoch = ref(0);
const totalEpoch = ref(100);
const currentLoss = ref(1.0);
const currentAcc = ref(0.0);
const statusText = ref("INITIALIZING...");
let polling = null;

// 창 닫기 / 나가기 기능
const closeWindow = () => {
  stopPolling();
  if(confirm("학습을 중단하고 나가시겠습니까?")) {
    router.push('/projects');
  }
};

const checkStatus = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/status');
    const data = res.data;

    progress.value = data.progress;
    currentEpoch.value = data.epoch;
    totalEpoch.value = data.total_epoch;
    currentLoss.value = data.loss;
    currentAcc.value = data.accuracy;
    
    statusText.value = data.is_training ? "PROCESSING DATA..." : "COMPLETED";

    // 완료 시 자동 이동
    if (!data.is_training && data.progress >= 100) {
      stopPolling();
      setTimeout(() => router.push('/project/1/result'), 800);
    }
  } catch (e) {
    console.error("Server Error");
  }
};

const startPolling = () => {
  polling = setInterval(checkStatus, 100); // 0.1초마다 갱신
};

const stopPolling = () => {
  if (polling) clearInterval(polling);
};

onMounted(startPolling);
onUnmounted(stopPolling);
</script>

<style scoped>
.page-container { height: 100vh; display: flex; justify-content: center; align-items: center; background: #050505; position: relative; overflow: hidden; font-family: 'Inter', sans-serif; }
.glow-bg { position: absolute; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #1a237e 0%, #000000 80%); z-index: 0; opacity: 0.6; }

/* 윈도우 창 디자인 (고급 Glassmorphism) */
.window-card { 
  z-index: 10; width: 650px; 
  background: rgba(20, 30, 40, 0.6); 
  backdrop-filter: blur(20px); 
  border-radius: 16px; 
  border: 1px solid rgba(255, 255, 255, 0.1); 
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5); 
  overflow: hidden;
  display: flex; flex-direction: column;
}

.window-header { 
  height: 50px; background: rgba(255, 255, 255, 0.03); 
  border-bottom: 1px solid rgba(255, 255, 255, 0.05); 
  display: flex; justify-content: space-between; align-items: center; padding: 0 20px;
}
.window-title { color: #a5b4fc; font-weight: bold; font-size: 0.9rem; display: flex; align-items: center; gap: 10px; letter-spacing: 1px; }
.status-dot { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 10px #4ade80; }
.pulsing { animation: pulse 1.5s infinite; }

.btn-close-window { background: transparent; border: none; color: #64748b; font-size: 1.2rem; cursor: pointer; transition: 0.2s; }
.btn-close-window:hover { color: #f87171; transform: scale(1.1); }

.window-body { padding: 40px; text-align: center; }
.status-message { color: white; font-size: 1.8rem; letter-spacing: 2px; margin-bottom: 40px; text-shadow: 0 0 20px rgba(59, 130, 246, 0.5); font-weight: 300; }

/* 게이지 바 */
.progress-wrapper { position: relative; margin-bottom: 40px; }
.progress-track { height: 12px; background: #1e293b; border-radius: 6px; overflow: hidden; position: relative; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #3b82f6, #8b5cf6); width: 0%; transition: width 0.1s linear; position: relative; }
.progress-light { position: absolute; right: 0; top: 0; height: 100%; width: 20px; background: white; filter: blur(4px); opacity: 0.7; }

.percent-number { position: absolute; right: 0; top: -35px; color: white; font-size: 2rem; font-weight: bold; font-family: monospace; }
.small { font-size: 1rem; color: #94a3b8; }

/* 데이터 그리드 */
.data-grid { display: flex; justify-content: space-between; gap: 15px; margin-bottom: 30px; }
.data-item { flex: 1; background: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05); }
.label { display: block; color: #64748b; font-size: 0.75rem; letter-spacing: 1px; margin-bottom: 5px; }
.value { font-size: 1.2rem; color: white; font-weight: bold; font-family: monospace; }
.value.green { color: #4ade80; } .value.red { color: #f87171; }

.window-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 20px; }
.logs { color: #475569; font-size: 0.8rem; margin: 0; }
.btn-abort { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); padding: 8px 16px; border-radius: 4px; cursor: pointer; font-size: 0.8rem; transition: 0.2s; }
.btn-abort:hover { background: rgba(239, 68, 68, 0.2); }

@keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
</style>