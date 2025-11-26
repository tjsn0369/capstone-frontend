<template>
  <div class="page-container">
    <div class="glow-bg"></div>
    <header class="header">
      <div class="brand"><span class="logo-dot"></span><h2>MY EXPERIMENTS</h2></div>
      <div class="header-actions">
        <button @click="resetDemoData" class="btn-action">🔄 Reset Demo</button>
        <button @click="router.push('/create')" class="btn-new">+ New Project</button>
        <button @click="logout" class="btn-logout">Logout</button>
      </div>
    </header>

    <div class="project-grid">
      <div v-if="projects.length === 0" class="empty-state">
        <p>No experiments found.</p>
        <button @click="resetDemoData" class="btn-link">Load Demo Data</button>
      </div>
      <div v-else v-for="p in projects" :key="p.id" class="project-card" @click="goToResult(p.id)">
        <button class="btn-delete" @click.stop="deleteProject(p.id)">✖</button>
        <div class="card-top">
          <span class="status-badge" :class="p.status?.toLowerCase() || 'done'">{{ p.status || 'Done' }}</span>
          <span class="date">{{ p.date }}</span>
        </div>
        <h3 class="p-name">{{ p.name }}</h3>
        <p class="p-model">{{ p.modelType }} Model</p>
        <div class="p-info">
          <div class="info-item"><span class="label">Epochs</span><span class="val">{{ p.epochMax || p.epochs }}</span></div>
        </div>
        <div class="card-footer"><span>View Result</span><span class="arrow">→</span></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const projects = ref([]);

onMounted(loadProjects);

function loadProjects() {
  const saved = localStorage.getItem('projects');
  if (saved) projects.value = JSON.parse(saved);
  else resetDemoData();
}

// ★ [핵심] 빵빵한 데모 데이터 (ResultView가 이걸 읽어서 화면에 뿌려줌)
function resetDemoData() {
  const demoData = [
    {
      id: 1, name: 'YOLOv8 Traffic Sign', date: '2025-11-25', status: 'Done', modelType: 'YOLOv8',
      epochMin: 50, epochMax: 200, lrMin: 0.001, lrMax: 0.01,
      // 가짜지만 진짜 같은 결과 데이터 삽입
      result: {
        best_accuracy: 94.2, final_loss: 0.031, best_epoch: 188,
        best_params: { learning_rate: 0.0051, batch_size: 64, optimizer: "SGD" },
        param_importance: [{ name: "Learning Rate", score: 0.88, color: "blue" }, { name: "Batch Size", score: 0.60, color: "purple" }]
      }
    },
    {
      id: 2, name: 'ResNet50 Face ID', date: '2025-11-24', status: 'Done', modelType: 'ResNet50',
      epochMin: 100, epochMax: 300, lrMin: 0.0001, lrMax: 0.005,
      result: {
        best_accuracy: 98.1, final_loss: 0.012, best_epoch: 290,
        best_params: { learning_rate: 0.0004, batch_size: 32, optimizer: "Adam" },
        param_importance: [{ name: "Epochs", score: 0.95, color: "green" }, { name: "Optimizer", score: 0.50, color: "gray" }]
      }
    }
  ];
  localStorage.setItem('projects', JSON.stringify(demoData));
  projects.value = demoData;
}

function deleteProject(id) {
  if (confirm("Delete?")) {
    projects.value = projects.value.filter(p => p.id !== id);
    localStorage.setItem('projects', JSON.stringify(projects.value));
  }
}
const logout = () => router.push('/');
const goToResult = (id) => router.push(`/project/${id}/result`);
</script>

<style scoped>
/* 기존 스타일과 동일 */
.page-container { min-height: 100vh; padding: 40px 60px; background: #02040a; position: relative; color: white; font-family: 'Inter', sans-serif; }
.glow-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 10% 10%, #111827 0%, #000 100%); pointer-events: none; z-index: 0; }
.header { position: relative; z-index: 10; display: flex; justify-content: space-between; align-items: center; margin-bottom: 50px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 20px; }
.brand { display: flex; align-items: center; gap: 10px; }
.logo-dot { width: 10px; height: 10px; background: #3b82f6; border-radius: 50%; box-shadow: 0 0 10px #3b82f6; }
.brand h2 { font-size: 1.5rem; letter-spacing: 1px; color: white; margin: 0; }
.header-actions { display: flex; gap: 10px; }
.btn-action, .btn-logout { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #cbd5e1; padding: 8px 16px; border-radius: 6px; cursor: pointer; transition: 0.2s; }
.btn-action:hover { background: rgba(255,255,255,0.1); color: white; }
.btn-logout:hover { border-color: #f87171; color: #f87171; }
.btn-new { background: #2563eb; color: white; border: none; padding: 8px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; box-shadow: 0 0 15px rgba(37,99,235,0.4); }
.btn-new:hover { background: #1d4ed8; }
.project-grid { position: relative; z-index: 10; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; }
.project-card { background: rgba(20, 25, 35, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 25px; cursor: pointer; transition: transform 0.2s, border-color 0.2s; position: relative; }
.project-card:hover { transform: translateY(-5px); border-color: #3b82f6; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.btn-delete { position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.5); border-radius: 50%; width: 24px; height: 24px; border: none; color: #94a3b8; cursor: pointer; z-index: 20; display: flex; justify-content: center; align-items: center; }
.btn-delete:hover { background: #ef4444; color: white; }
.card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; margin-top: 5px; }
.status-badge { font-size: 0.7rem; padding: 4px 8px; border-radius: 4px; text-transform: uppercase; font-weight: bold; }
.status-badge.done { background: rgba(16,185,129,0.1); color: #34d399; border: 1px solid rgba(16,185,129,0.2); }
.date { color: #64748b; font-size: 0.8rem; margin-right: 25px; }
.p-name { color: white; font-size: 1.2rem; margin: 0 0 5px 0; }
.p-model { color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; }
.p-info { background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px; margin-bottom: 20px; }
.info-item { display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 0.85rem; }
.info-item .label { color: #64748b; }
.info-item .val { color: #cbd5e1; font-family: monospace; }
.card-footer { display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px; color: #3b82f6; font-size: 0.9rem; font-weight: bold; }
.arrow { transition: transform 0.2s; }
.project-card:hover .arrow { transform: translateX(5px); }
.empty-state { grid-column: 1 / -1; text-align: center; color: #64748b; padding: 50px; }
.btn-link { background: none; border: none; color: #3b82f6; text-decoration: underline; cursor: pointer; margin-top: 10px; }
</style>