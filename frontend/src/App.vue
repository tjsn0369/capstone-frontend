<script setup>
// 스크립트는 그대로 둠
</script>

<template>
  <RouterView />
</template>

<style>
/* 화면 초기화 및 전체 배경 설정 */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden; /* 스크롤 없애기 */
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
}

#app {
  width: 100%;
  height: 100vh;
  /* 핵심: 블루블랙 그라데이션 배경 */
  background: linear-gradient(135deg, #0a0a0a 0%, #0b1021 50%, #1b2735 100%);
  color: #ffffff;
}

/* 모든 입력창과 버튼의 기본 폰트 설정 */
input, button, textarea {
  font-family: inherit;
}
</style>