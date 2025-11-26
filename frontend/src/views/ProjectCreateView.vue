<template>
  <div class="page-container">
    <div class="glow-bg"></div>
    <div class="center-wrapper">
      <div class="glass-card">
        <header class="card-header">
          <h1 class="title">New Experiment</h1>
          <p class="subtitle">Optuna Hyperparameter Tuning</p>
        </header>

        <div class="card-body">
          <div class="section-title">1. Project Info</div>
          <div class="form-group row">
            <input v-model="form.name" placeholder="Project Name" class="half" />
            <select v-model="form.modelType" class="half">
              <option value="YOLOv8">YOLOv8</option>
              <option value="ResNet50">ResNet-50</option>
              <option value="EfficientNet">EfficientNet</option>
            </select>
          </div>

          <div class="section-title">2. Optuna Search Space (Range)</div>
          
          <div class="range-group">
            <label>Epochs Range</label>
            <div class="inputs">
              <input v-model.number="form.epochMin" type="number" placeholder="Min (e.g. 50)" />
              <span class="tilde">~</span>
              <input v-model.number="form.epochMax" type="number" placeholder="Max (e.g. 200)" />
            </div>
          </div>

          <div class="range-group">
            <label>Batch Size Candidates (comma separated)</label>
            <input v-model="form.batchSizeList" placeholder="e.g. 16, 32, 64" />
          </div>

          <div class="range-group">
            <label>Learning Rate (Log Scale)</label>
            <div class="inputs">
              <input v-model.number="form.lrMin" type="number" step="0.0001" placeholder="Min (e.g. 0.0001)" />
              <span class="tilde">~</span>
              <input v-model.number="form.lrMax" type="number" step="0.001" placeholder="Max (e.g. 0.01)" />
            </div>
          </div>
        </div>

        <footer class="card-footer">
          <button class="btn-secondary" @click="$router.push('/projects')">Cancel</button>
          <button class="btn-primary" @click="createProject">Start Tuning 🚀</button>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

const form = reactive({
  name: '',
  modelType: 'YOLOv8',
  epochMin: 50,
  epochMax: 200,
  batchSizeList: '16, 32, 64',
  lrMin: 0.0001,
  lrMax: 0.01
});

const createProject = async () => {
  if (!form.name) return alert("프로젝트 이름을 입력하세요!");

  try {
    const payload = {
      ...form,
      id: Date.now(),
      status: 'Ready',
      date: new Date().toLocaleDateString()
    };

    // FastAPI로 전송
    await axios.post('http://127.0.0.1:8000/create_project', payload);
    
    // 로컬 저장 후 이동
    const projects = JSON.parse(localStorage.getItem('projects') || '[]');
    projects.push(payload);
    localStorage.setItem('projects', JSON.stringify(projects));

    router.push(`/project/${payload.id}/train`); // 바로 학습 화면으로 이동
  } catch (e) {
    alert("서버 연결 실패! 백엔드를 켜주세요.");
  }
};
</script>

<style scoped>
/* 다크 모드 & 깔끔한 스타일 */
.page-container { min-height: 100vh; display: flex; justify-content: center; align-items: center; background: #0b1021; position: relative; }
.glow-bg { position: fixed; width: 100%; height: 100%; background: radial-gradient(circle at 50% -20%, rgba(59,130,246,0.15), transparent 70%); pointer-events: none; }
.center-wrapper { z-index: 1; width: 100%; max-width: 500px; padding: 20px; }
.glass-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; backdrop-filter: blur(10px); padding: 30px; }
.card-header { text-align: center; margin-bottom: 30px; }
.title { color: white; margin: 0; font-size: 1.8rem; }
.subtitle { color: #64748b; margin-top: 5px; font-size: 0.9rem; }
.section-title { color: #3b82f6; font-weight: bold; margin: 20px 0 10px 0; font-size: 0.95rem; border-bottom: 1px solid rgba(59,130,246,0.3); padding-bottom: 5px; }
.form-group.row { display: flex; gap: 10px; }
.half { flex: 1; }
input, select { width: 100%; padding: 12px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: white; outline: none; box-sizing: border-box; }
.range-group { margin-bottom: 15px; }
.range-group label { display: block; color: #94a3b8; font-size: 0.85rem; margin-bottom: 6px; }
.range-group .inputs { display: flex; align-items: center; gap: 10px; }
.tilde { color: #64748b; font-weight: bold; }
.card-footer { margin-top: 30px; display: flex; justify-content: space-between; }
.btn-secondary { background: transparent; color: #94a3b8; border: none; cursor: pointer; }
.btn-primary { background: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-weight: bold; }
</style>