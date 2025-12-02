<template>
  <div class="page-container">
    <div class="glow-bg"></div>
    
    <div class="window-card">
      <div class="window-header">
        <div class="window-title">
          <span class="status-dot pulsing"></span>
          AI MODEL TRAINING MONITOR
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

        <div class="chart-wrapper">
          <div id="realtime-chart" style="width: 100%; height: 280px;"></div>
        </div>

        <div class="data-grid">
          <div class="data-item">
            <span class="label">EPOCH</span>
            <span class="value">{{ currentEpoch }} / {{ totalEpoch }}</span>
          </div>
          <div class="data-item">
            <span class="label">LOSS</span>
            <span class="value red">{{ currentLoss.toFixed(4) }}</span>
          </div>
          <div class="data-item">
            <span class="label">ACCURACY</span>
            <span class="value green">{{ currentAcc.toFixed(2) }}%</span>
          </div>
        </div>
        
        <div class="window-footer">
           <p class="logs">Log: {{ currentLog }}</p>
           <button class="btn-abort" @click="closeWindow">ABORT</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Plotly from 'plotly.js-dist-min'; // ★ Plotly 임포트 필수

const router = useRouter();

// 상태 변수들
const progress = ref(0);
const currentEpoch = ref(0);
const totalEpoch = ref(100);
const currentLoss = ref(2.5); // 초기 Loss 높게 설정
const currentAcc = ref(10.0); // 초기 Acc 낮게 설정
const statusText = ref("INITIALIZING...");
const currentLog = ref("Preparing data loader...");

// 그래프용 데이터 배열
const historyEpoch = [];
const historyLoss = [];
const historyAcc = [];

let polling = null;

const closeWindow = () => {
  stopPolling();
  if(confirm("학습을 중단하고 나가시겠습니까?")) router.push('/projects');
};

// ★ 차트 초기화 함수
const initChart = () => {
  const layout = {
    title: { text: 'Real-time Metrics', font: { color: '#cbd5e1', size: 14 } },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    margin: { t: 40, l: 40, r: 40, b: 30 },
    xaxis: { title: 'Epoch', color: '#94a3b8', showgrid: false },
    yaxis: { title: 'Loss', color: '#f87171', showgrid: true, gridcolor: 'rgba(255,255,255,0.1)' },
    yaxis2: { title: 'Accuracy', color: '#4ade80', overlaying: 'y', side: 'right', showgrid: false, range: [0, 100] },
    showlegend: true,
    legend: { x: 0.5, y: 1.1, xanchor: 'center', orientation: 'h', font: { color: 'white' } }
  };

  const trace1 = { x: [], y: [], name: 'Loss', mode: 'lines', line: { color: '#f87171', width: 3 } };
  const trace2 = { x: [], y: [], name: 'Accuracy', mode: 'lines', yaxis: 'y2', line: { color: '#4ade80', width: 3 } };

  Plotly.newPlot('realtime-chart', [trace1, trace2], layout, { responsive: true, displayModeBar: false });
};

// ★ 차트 업데이트 함수
const updateChart = () => {
  // 배열에 데이터 추가
  historyEpoch.push(currentEpoch.value);
  historyLoss.push(currentLoss.value);
  historyAcc.push(currentAcc.value);

  // Plotly에 새 데이터 반영 (빠른 업데이트)
  Plotly.update('realtime-chart', {
    x: [historyEpoch, historyEpoch],
    y: [historyLoss, historyAcc]
  });
};

// 가짜 데이터 생성 및 갱신 (데모용)
const simulateTraining = () => {
  if (currentEpoch.value >= totalEpoch.value) {
    stopPolling();
    statusText.value = "COMPLETED!";
    setTimeout(() => router.push('/project/1/result'), 1500);
    return;
  }

  // 데이터 변화 시뮬레이션
  currentEpoch.value += 1;
  progress.value = Math.floor((currentEpoch.value / totalEpoch.value) * 100);
  
  // Loss는 줄어들고, Acc는 늘어나는 로직
  currentLoss.value = Math.max(0.1, currentLoss.value * 0.95 + (Math.random() * 0.1 - 0.05));
  currentAcc.value = Math.min(99.9, currentAcc.value + (Math.random() * 2.5));
  
  statusText.value = "TRAINING...";
  currentLog.value = `Epoch ${currentEpoch.value}: loss=${currentLoss.value.toFixed(4)}, acc=${currentAcc.value.toFixed(2)}`;

  updateChart(); // 차트 그리기
};

const startPolling = async () => {
  await nextTick(); // DOM 생성 대기
  initChart();      // 차트 생성
  polling = setInterval(simulateTraining, 200); // 0.2초마다 갱신
};

const stopPolling = () => { if (polling) clearInterval(polling); };

onMounted(startPolling);
onUnmounted(stopPolling);
</script>

<style scoped>
/* 기존 스타일 유지 + 차트 영역 스타일 추가 */
.page-container { height: 100vh; display: flex; justify-content: center; align-items: center; background: #050505; position: relative; font-family: 'Inter', sans-serif; }
.glow-bg { position: absolute; width: 100%; height: 100%; background: radial-gradient(circle at 50% 50%, #1a237e 0%, #000000 80%); z-index: 0; opacity: 0.6; }

.window-card { 
  z-index: 10; width: 700px; /* 차트 때문에 폭 살짝 넓힘 */
  background: rgba(20, 30, 40, 0.75); 
  backdrop-filter: blur(20px); 
  border-radius: 16px; 
  border: 1px solid rgba(255, 255, 255, 0.1); 
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5); 
  display: flex; flex-direction: column;
}
.window-header { height: 50px; background: rgba(255, 255, 255, 0.03); border-bottom: 1px solid rgba(255, 255, 255, 0.05); display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }
.window-title { color: #a5b4fc; font-weight: bold; font-size: 0.9rem; display: flex; align-items: center; gap: 10px; }
.status-dot { width: 8px; height: 8px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 10px #4ade80; }
.pulsing { animation: pulse 1.5s infinite; }
.btn-close-window { background: transparent; border: none; color: #64748b; font-size: 1.2rem; cursor: pointer; }

.window-body { padding: 30px; }
.status-message { color: white; font-size: 1.5rem; text-align: center; margin-bottom: 20px; font-weight: 300; letter-spacing: 2px; }

/* 프로그레스 바 */
.progress-wrapper { position: relative; margin-bottom: 20px; }
.progress-track { height: 8px; background: #1e293b; border-radius: 4px; overflow: hidden; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #3b82f6, #8b5cf6); width: 0%; transition: width 0.2s linear; position: relative; }
.percent-number { position: absolute; right: 0; top: -25px; color: white; font-size: 1.2rem; font-weight: bold; font-family: monospace; }
.small { font-size: 0.8rem; color: #94a3b8; }

/* 차트 영역 */
.chart-wrapper { margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 10px; background: rgba(0,0,0,0.2); }

/* 데이터 그리드 */
.data-grid { display: flex; justify-content: space-between; gap: 10px; margin-bottom: 20px; }
.data-item { flex: 1; background: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 8px; text-align: center; }
.label { display: block; color: #64748b; font-size: 0.7rem; margin-bottom: 5px; }
.value { font-size: 1.1rem; color: white; font-weight: bold; font-family: monospace; }
.value.green { color: #4ade80; } .value.red { color: #f87171; }

.window-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 15px; }
.logs { color: #475569; font-size: 0.8rem; font-family: monospace; }
.btn-abort { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); padding: 6px 16px; border-radius: 4px; cursor: pointer; }

@keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
</style>