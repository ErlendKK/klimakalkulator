<template>
    <div class="layout">
      <nav-header />
  
      <!-- TODO: Implement Main page for logged in/ not logged in -->
      <main class="container">
        <img src="../assets/stockphoto.png" loading="lazy"/>
        <h1>Velkommen til Klimakalkulatoren</h1>
        <p>text</p>
        <p>text</p>
        <p>text</p>
        <p>text</p>
        <p>text</p>
        <p>text</p>
      </main>

      <nav-footer />
    </div>
  </template>
    
  <script>
    import NavHeader from '../components/NavHeader.vue'
    import NavFooter from '../components/NavFooter.vue'
    import { useAuthStore } from '../stores/authStore';
    import { computed } from 'vue';
    
    export default {
        name: 'Home',
        components: {
          NavHeader,
          NavFooter
        },        
        setup() {
          const authStore = useAuthStore();
          const isLoggedInComputed = computed(() => authStore.isLoggedIn);
          const userComputed = computed(() => authStore.user);

          return { isLoggedInComputed, userComputed };
        },

      };

  </script>
  
  <style scoped>
      main {
          padding-top: 0;
      }
      .container img {
        width: 100%;
        height: auto;
      }
  </style>