<template>
    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow">
      <div class="text-3xl mb-2">{{ icon }}</div>
      <h3 class="text-lg font-semibold mb-1">{{ title }}</h3>
      <p class="text-sm text-gray-600 dark:text-gray-300">{{ description }}</p>
    </div>
  </template>
  
  <script setup>
  defineProps(['icon', 'title', 'description'])
  </script>
  