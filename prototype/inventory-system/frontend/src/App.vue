<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

#app {
  min-height: 100vh;
}

button {
  cursor: pointer;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
}

button.primary {
  background-color: #4CAF50;
  color: white;
}

button.primary:hover {
  background-color: #45a049;
}

button.secondary {
  background-color: #2196F3;
  color: white;
}

button.secondary:hover {
  background-color: #0b7dda;
}

button.danger {
  background-color: #f44336;
  color: white;
}

button.danger:hover {
  background-color: #da190b;
}

input, select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
}

input:focus, select:focus {
  outline: none;
  border-color: #4CAF50;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
}

tr:hover {
  background-color: #f5f5f5;
}
</style>
