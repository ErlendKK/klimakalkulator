<template>
    <div class="layout">
      <nav-header />
  
      <!-- TODO: Implement Main page for logged in/ not logged in -->
      <main class="container">
        <img src="../assets/stockphoto.jpg" loading="lazy"/>
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
          NavFooter,
        },        
        setup() {
          const authStore = useAuthStore();
          const isLoggedInComputed = computed(() => authStore.isLoggedIn);
          const userComputed = computed(() => authStore.user);

          return { isLoggedInComputed, userComputed };
        },

        data() {
          return {
              selectedOption: null,
              options: [
                  { name: 'Option 1', value: 1 },
                  { name: 'Option 2', value: 2 },
                  { name: 'Option 3', value: 3 }
              ]
          };
        }
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