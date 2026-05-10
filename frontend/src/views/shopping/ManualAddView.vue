<template>
  <div class="container">
    <div class="header-row">
      <RouterLink to="/shopping-list" class="back-link">← 買い物リストに戻る</RouterLink>
      <h1 class="page-title">買い物リスト - 手動追加</h1>
    </div>

    <div class="card">
      <div class="form-group">
        <label for="name">商品名 *</label>
        <input id="name" type="text" class="input-field" />
      </div>
      <div class="form-group">
        <label for="quantity">数量 *</label>
        <input id="quantity" type="number" class="input-field" />
      </div>
      <div class="form-group">
        <label for="unit">単位 *</label>
        <select id="unit" class="select-field">
          <option>個</option>
          <option>本</option>
          <option>袋</option>
          <option>ml</option>
          <option>g</option>
          <option>kg</option>
          <option>L</option>
        </select>
      </div>
      <div class="form-actions">
        <RouterLink to="/shopping-list" class="btn btn-secondary">キャンセル</RouterLink>
        <button class="btn btn-primary">追加</button>
      </div>
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
