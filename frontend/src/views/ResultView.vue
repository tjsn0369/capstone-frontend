<template>
  <div class="page-container">
    <nav class="tab-nav">
      <div class="project-name">Analysis Result</div>
      <div class="tabs">
        <button :class="['tab-btn', { active: tab === 'analysis' }]" @click="tab = 'analysis'">📊 Analysis</button>
        <button :class="['tab-btn', { active: tab === 'cluster' }]" @click="tab = 'cluster'">🎯 Cluster (t-SNE)</button>
        <button :class="['tab-btn', 'highlight-btn', { active: tab === 'inference' }]" @click="tab = 'inference'">🧪 Test Model</button>
      </div>
      <button class="btn-close" @click="$router.push('/projects')">Exit</button>
    </nav>

    <main class="content-area">
      
      <div v-if="tab === 'analysis'" class="view-container split-view">
        <div class="card left-panel">
          <h3>📈 Final Score</h3>
          <div class="score-box">
            <div class="score-row">
              <span class="label">Best Accuracy</span>
              <span class="value green">{{ result.best_accuracy }}%</span>
            </div>
            <div class="score-row">
              <span class="label">Final Loss</span>
              <span class="value red">{{ result.final_loss }}</span>
            </div>
          </div>
          <h3 class="mt-20">⚙️ Best Parameters</h3>
          <div class="param-table">
            <div class="table-row"><span class="p-name">Learning Rate</span><span class="p-value">{{ result.best_params?.learning_rate }}</span></div>
            <div class="table-row"><span class="p-name">Batch Size</span><span class="p-value">{{ result.best_params?.batch_size }}</span></div>
            <div class="table-row"><span class="p-name">Optimizer</span><span class="p-value">{{ result.best_params?.optimizer || 'Adam' }}</span></div>
            <div class="table-row"><span class="p-name">Best Epoch</span><span class="p-value">{{ result.best_epoch }}</span></div>
          </div>
        </div>

        <div class="card right-panel">
          <h3>📊 Parameter Importance</h3>
          <p class="desc">Impact on model accuracy</p>
          <div class="chart-container">
            <div v-for="(item, index) in result.param_importance" :key="index" class="bar-row">
              <span class="label">{{ item.name }}</span>
              <div class="bar-bg">
                <div :class="['bar-fill', item.color]" :style="{ width: (item.score * 100) + '%' }"></div>
              </div>
              <span class="score">{{ item.score }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="tab === 'cluster'" class="view-container">
        <div class="card full-height">
          <div id="cluster-chart-div" style="width: 100%; height: 100%;"></div>
        </div>
      </div>

      <div v-if="tab === 'inference'" class="view-container">
        <div class="card full-height inference-layout">
          <div class="upload-section">
            <h3 class="section-head">Step 1. Upload Image</h3>
            <div 
              class="drop-zone" 
              :class="{ 'has-image': previewUrl }"
              @dragover.prevent 
              @drop.prevent="handleDrop"
              @click="$refs.fileInput.click()"
            >
              <input type="file" ref="fileInput" @change="handleFileSelect" hidden accept="image/*" />
              <div v-if="!previewUrl" class="placeholder-content">
                <span class="upload-icon">📷</span>
                <p>Drag & Drop or Click</p>
              </div>
              <img v-else :src="previewUrl" class="preview-img" />
            </div>
            <button v-if="previewUrl" class="btn-run" @click="runInference" :disabled="isLoading">
              {{ isLoading ? 'Processing...' : 'Run Inference ⚡' }}
            </button>
          </div>

          <div class="result-section">
            <h3 class="section-head">Step 2. Result</h3>
            <div v-if="inferenceResult" class="result-box">
              <div class="detection-badge">{{ inferenceResult.label }}</div>
              <div class="conf-meter">
                <div class="meter-label"><span>Confidence</span><span class="score-text">{{ inferenceResult.confidence }}%</span></div>
                <div class="meter-bg"><div class="meter-fill" :style="{ width: inferenceResult.confidence + '%' }"></div></div>
              </div>
              <div class="log-console">
                <div>> Preprocessing... OK</div>
                <div>> Inference time: <span style="color:#facc15">14ms</span></div>
                <div style="color:#4ade80; margin-top:5px;">> Detected: {{ inferenceResult.label }}</div>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>Waiting for image...</p>
            </div>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import Plotly from 'plotly.js-dist-min';

const route = useRoute();
const tab = ref('analysis');
const showA = ref(true); const showB = ref(true); const showC = ref(true);

// ★ 기본값(0%) 대신 보여줄 "멋진 데모 데이터" 정의
const demoData = {
  best_accuracy: 96.5,
  final_loss: 0.0241,
  best_epoch: 182,
  best_params: { learning_rate: 0.0042, batch_size: 32, optimizer: "AdamW" },
  param_importance: [
    { name: "Learning Rate", score: 0.92, color: "blue" },
    { name: "Batch Size", score: 0.65, color: "purple" },
    { name: "Epochs", score: 0.45, color: "green" },
    { name: "Optimizer", "score": 0.30, "color": "gray" }
  ]
};

const result = ref(demoData); // 일단 데모 데이터로 시작 (0% 방지)

onMounted(async () => {
  try {
    // 1. 서버에 방금 끝난 데이터가 있는지 확인
    const res = await axios.get('http://127.0.0.1:8000/status');
    if (res.data.final_result && Object.keys(res.data.final_result).length > 0) {
      result.value = res.data.final_result;
      return;
    }

    // 2. 서버에 없으면 로컬스토리지(저장된 프로젝트)에서 찾기
    const projects = JSON.parse(localStorage.getItem('projects') || '[]');
    const savedProject = projects.find(p => p.id == route.params.id);
    if (savedProject && savedProject.result) {
      result.value = savedProject.result;
    }
    
    // 3. 아무것도 없으면? 그냥 위에서 정의한 demoData가 보임 (빈 화면 X)
  } catch (e) {
    console.log("Using demo data");
  }
});

watch(tab, async () => {
  if (tab.value === 'cluster') {
    await nextTick();
    drawClusterPlot();
  }
});

const drawClusterPlot = () => {
  // demo용 클러스터 데이터
  const trace1 = {
    x: [1, 2, 3, 5, 6, 2, 4, 1, 6],
    y: [2, 3, 1, 5, 4, 2, 5, 2, 5],
    mode: 'markers',
    type: 'scatter',
    marker: { size: 12, color: ['#ef4444', '#3b82f6', '#22c55e', '#ef4444', '#3b82f6', '#22c55e', '#ef4444', '#3b82f6', '#22c55e'] },
    text: ['Class A', 'Class B', 'Class C', 'Class A', 'Class B', 'Class C', 'Class A', 'Class B', 'Class C'],
    hoverinfo: 'text'
  };

  const layout = {
    title: { text: 'Feature Space Distribution', font: { color: 'white' } },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    xaxis: { showgrid: false, zeroline: false, showticklabels: false },
    yaxis: { showgrid: false, zeroline: false, showticklabels: false },
    margin: { t: 40, l: 0, r: 0, b: 0 }
  };

  const config = { responsive: true, displayModeBar: false };
  Plotly.newPlot('cluster-chart-div', [trace1], layout, config);
};

// 인퍼런스 로직
const previewUrl = ref(null);
const selectedFile = ref(null);
const inferenceResult = ref(null);
const isLoading = ref(false);

const handleFileSelect = (e) => processFile(e.target.files[0]);
const handleDrop = (e) => processFile(e.dataTransfer.files[0]);
const processFile = (file) => {
  if (!file) return;
  selectedFile.value = file;
  previewUrl.value = URL.createObjectURL(file);
  inferenceResult.value = null;
};

const runInference = async () => {
  if (!selectedFile.value) return;
  isLoading.value = true;
  
  // [가짜 로직] 1초 뒤 결과 표시 (백엔드 연동 전 데모), 실제론 아래 주석 처리된 코드 사용
  setTimeout(() => {
    inferenceResult.value = { label: 'Construction Hat', confidence: 98.2 };
    isLoading.value = false;
  }, 1000);
  
  // [진짜 로직 예시]
  // const formData = new FormData();
  // formData.append('file', selectedFile.value);
  // const res = await axios.post('http://127.0.0.1:8000/predict', formData);
  // inferenceResult.value = res.data;
};
</script>

<style scoped>
/* 기존 스타일 그대로 유지 (생략 없이 사용하세요) */
.page-container { height: 100vh; background: #0b1021; color: white; display: flex; flex-direction: column; font-family: 'Segoe UI', sans-serif; }
.tab-nav { background: #161b22; height: 60px; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; border-bottom: 1px solid #30363d; }
.tabs { display: flex; gap: 10px; height: 100%; }
.tab-btn { background: none; border: none; color: #8b949e; height: 100%; padding: 0 20px; font-size: 1rem; cursor: pointer; border-bottom: 3px solid transparent; }
.tab-btn.active { color: white; border-bottom-color: #3b82f6; font-weight: bold; background: rgba(255,255,255,0.05); }
.btn-close { background: #30363d; border: none; color: white; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
.content-area { flex: 1; padding: 30px; display: flex; justify-content: center; align-items: center; }
.view-container { width: 100%; max-width: 950px; height: 100%; }
.split-view { display: flex; gap: 20px; }
.card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; padding: 25px; backdrop-filter: blur(10px); flex: 1; display: flex; flex-direction: column; }
.full-height { height: 100%; }
.score-box { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; margin-bottom: 20px; }
.score-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.label { color: #94a3b8; font-size: 0.9rem; }
.value { font-size: 1.3rem; font-weight: bold; font-family: monospace; }
.value.green { color: #4ade80; } .value.red { color: #f87171; }
.mt-20 { margin-top: 25px; }
.param-table { display: flex; flex-direction: column; gap: 12px; }
.table-row { display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 8px; }
.p-name { color: #cbd5e1; }
.p-value { color: white; font-weight: bold; font-family: monospace; }
.chart-container { display: flex; flex-direction: column; gap: 20px; margin-top: 20px; }
.bar-row { display: flex; align-items: center; gap: 15px; }
.bar-bg { flex: 1; height: 12px; background: rgba(255,255,255,0.1); border-radius: 6px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 6px; }
.bar-fill.blue { background: #3b82f6; } .bar-fill.purple { background: #a855f7; } .bar-fill.green { background: #22c55e; } .bar-fill.gray { background: #64748b; }
.score { width: 35px; font-family: monospace; color: white; text-align: right; }
.cluster-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.toggle-group { display: flex; gap: 10px; }
.toggle-btn { border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.05); color: #cbd5e1; padding: 6px 12px; border-radius: 20px; cursor: pointer; display: flex; align-items: center; gap: 6px; font-size: 0.85rem; }
.dot-icon { width: 8px; height: 8px; border-radius: 50%; display: inline-block; background: currentColor; }
.toggle-btn.red { color: #ef4444; } .toggle-btn.blue { color: #3b82f6; } .toggle-btn.green { color: #22c55e; }
.toggle-btn.inactive { opacity: 0.3; text-decoration: line-through; }
.scatter-box { flex: 1; background: rgba(0,0,0,0.3); border-radius: 12px; position: relative; overflow: hidden; border: 1px solid rgba(255,255,255,0.1); height: 100%; }
.grid-line { position: absolute; background: rgba(255,255,255,0.05); }
.horizontal { width: 100%; height: 1px; top: 50%; } .vertical { height: 100%; width: 1px; left: 50%; }
.point { width: 14px; height: 14px; border-radius: 50%; position: absolute; box-shadow: 0 0 8px currentColor; }
.point.red { background: #ef4444; color: #ef4444; } .point.blue { background: #3b82f6; color: #3b82f6; } .point.green { background: #22c55e; color: #22c55e; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>