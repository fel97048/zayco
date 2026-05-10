<template>
  <div class="container">
    <div class="header-row">
      <h1 class="page-title">買い物リスト</h1>
      <RouterLink to="/shopping-list/add" class="btn btn-primary">+ 手動追加</RouterLink>
    </div>

    <div class="card">
      <p>買い物リスト機能はまだ実装されていません。</p>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style scoped>
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
