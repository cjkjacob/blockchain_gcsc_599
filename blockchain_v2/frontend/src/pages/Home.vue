<template>
    <div class="px-4 py-10 max-w-3xl mx-auto text-center">
      <h1 class="text-4xl font-extrabold mb-4 text-white">🧱 Proof of Effort</h1>
      <p class="text-lg text-gray-700 dark:text-gray-300 mb-8">
        A decentralized system that rewards real work — learning, creating, and growing.
        Submit your effort. Validate others. Earn tokens.
      </p>
  
      <div class="grid gap-6 sm:grid-cols-2 text-left">
        <FeatureCard
          icon="📤"
          title="Submit Effort"
          description="Prove you've completed a meaningful task. Upload evidence and submit it to the chain." />
  
        <FeatureCard
          icon="🧑‍⚖️"
          title="Validate Others"
          description="As a validator, review and approve effort submitted by learners and peers." />
  
        <FeatureCard
          icon="🎁"
          title="Earn Tokens"
          description="Receive EFF tokens based on your validated effort — a new kind of recognition." />
  
        <FeatureCard
          icon="🔐"
          title="Own Your Work"
          description="Each block you earn is secured by your wallet, making your growth verifiable and immutable." />
      </div>
  
      <router-link to="/profile" class="inline-block mt-10 bg-sky-600 hover:bg-sky-950 text-white px-6 py-3 rounded">
        🚀 Go to My Profile
      </router-link>
    </div>
  </template>
  
  <script setup>
  import FeatureCard from '../components/FeatureCard.vue'
  </script>
  