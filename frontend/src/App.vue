<template>
  <RouterView />
</template>

<script setup>
  import { onMounted } from 'vue';
  import { RouterView } from 'vue-router'
  import { useAuthStore } from './stores/authStore';

  const authStore = useAuthStore();

  // check session every time this component mounts
  onMounted( async () => {
    await authStore.checkSession();
    console.log(authStore.isLoggedIn)
  });
</script>