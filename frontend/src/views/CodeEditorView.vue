<template>
  <div class="editor-container">
    <header class="top-bar">
      <div class="left-panel">
        <span class="project-name">{{ project?.name || 'Loading...' }}</span>
        <span class="separator">/</span>
        <span class="file-name active">{{ project?.fileName || 'model.py' }}</span>
      </div>
      <div class="right-panel">
        <button class="btn-save" @click="saveCode">Save Changes</button>
      </div>
    </header>

    <div class="main-layout">
      <aside class="sidebar">
        <div class="sidebar-title">EXPLORER</div>
        <ul class="file-list">
          <li class="file-item active"><span class="icon">📄</span> model.py</li>
          <li class="file-item"><span class="icon">📄</span> train.py</li>
          <li class="file-item"><span class="icon">⚙️</span> config.yaml</li>
        </ul>
      </aside>

      <main class="code-area">
        <textarea v-model="codeContent" class="code-input" spellcheck="false"></textarea>
      </main>
    </div>

    <footer class="bottom-bar">
      <button class="btn-back" @click="$router.push('/projects')">← Projects</button>
      <button class="btn-train" @click="goToTraining">Start Training 🚀</button>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const projectId = route.params.id;
const project = ref(null);
const codeContent = ref(`import torch\nimport torch.nn as nn\n\nclass CustomModel(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.conv1 = nn.Conv2d(1, 32, 3, 1)\n\n    def forward(self, x):\n        return self.conv1(x)`);

onMounted(() => {
  const all = JSON.parse(localStorage.getItem('projects') || '[]');
  project.value = all.find(p => p.id == projectId);
});

const saveCode = () => alert("Saved!");
const goToTraining = () => router.push(`/project/${projectId}/train`);
</script>

<style scoped>
/* 기존 다크 디자인 유지 */
.editor-container { display: flex; flex-direction: column; height: 100vh; background-color: #0d1117; color: #c9d1d9; font-family: monospace; }
.top-bar { height: 50px; background: #161b22; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }
.project-name { font-weight: bold; color: #58a6ff; }
.main-layout { display: flex; flex: 1; }
.sidebar { width: 250px; background: #0d1117; border-right: 1px solid #30363d; }
.sidebar-title { padding: 10px; color: #8b949e; font-weight: bold; }
.file-item { padding: 8px 20px; cursor: pointer; color: #8b949e; }
.file-item.active { background: #161b22; color: #58a6ff; }
.code-area { flex: 1; background: #0d1117; display: flex; }
.code-input { flex: 1; background: transparent; color: #c9d1d9; border: none; padding: 20px; outline: none; resize: none; }
.bottom-bar { height: 40px; background: #161b22; border-top: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; padding: 0 10px; }
.btn-save { background: #238636; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
.btn-train { background: #1f6feb; color: white; border: none; padding: 6px 15px; border-radius: 4px; cursor: pointer; }
.btn-back { background: transparent; border: none; color: #8b949e; cursor: pointer; }
</style>