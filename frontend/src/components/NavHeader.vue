<template>
  <header class="container-fluid">
    <div class="header-content">

    <div class="logo-container">
      <router-link class="navbar-brand router" to="/">
        <img class="logo" src="/favicon.ico" width="40" height="40">
      </router-link>
      <router-link class="navbar-brand router" to="/">
        <h1>Klimakalkulatoren</h1>
      </router-link>
    </div>

    <!-- Modals for registration and login -->
    <registration-modal
      :is-active="isRegistrationModalActive"
      @close="isRegistrationModalActive = false"
      @login="swichModal">
    </registration-modal>

    <login-modal
      :is-active="isLoginModalActive"
      @close="isLoginModalActive = false"
      @registrer="swichModal">
    </login-modal>

    <nav > <!-- expands to horizontal when screen >= md -->
      <div class="navbar-expand-md">
      <!-- Route links -->
      <ul class="nav justify-content-end navbar-nav">
        <li class="nav-item">
          <router-link class="router" to="/projects">Prosjekter</router-link>
        </li>
        <li class="nav-item">
          <router-link class="router" to="/products">Produkter</router-link>
        </li>
        <li class="nav-item">
          <router-link class="router" to="/results">Resultat</router-link>
        </li>

        <!-- Display name if logedIn; Otherwise ask user to login -->
        <li
          v-if="isLoggedInComputed"
          class="nav-item  user-name d-none d-md-block">
          {{ userComputed.name }}
        </li>
        <li 
          v-else 
          class="nav-item d-none d-md-block router" 
          @click="isLoginModalActive = true">
          Logg inn
        </li>
        </ul>
      </div>

      <!-- Drop down menu for user account if logedIn -->
      <ul class="nav justify-content-end navbar-nav">
        <li class="nav-item dropdown">
          <template v-if="isPhotoDisplayed">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <img
                :src="userComputed.photo_url"
                @error="handleImageError"
                class="rounded-circle profile-picture"
                height="45"
                loading="lazy"
              />
            </a>
          </template>
          <template v-else>
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="bi bi-person-circle rounded-circle profile-picture"></i>
            </a>
          </template>
          <template
            v-if="isLoggedInComputed">
            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
              <li><a class="dropdown-item" href="#">Profil</a></li>
              <li><a class="dropdown-item" href="#">Instillinger</a></li>
              <li><a class="dropdown-item" href="#" @click="logOut">Logg ut</a></li>
            </ul>
          </template>
          <template
            v-else>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
              <li><a class="dropdown-item" href="#" @click="isRegistrationModalActive = true">Registrer</a></li>
              <li><a class="dropdown-item" href="#" @click="isLoginModalActive = true">Logg Inn</a></li>
              <li><a class="dropdown-item" href="#">Info</a></li>
            </ul>
          </template>
        </li>
      </ul>

    </nav>
    </div>
  </header>
</template>
  
<script>
  import RegistrationModal from '../components/RegistrationModal.vue';
  import LoginModal from '../components/LoginModal.vue';
  import { useAuthStore } from '../stores/authStore';
  import { computed } from 'vue';
  
  export default {
    name: 'NavHeader',    
    setup() {
      const authStore = useAuthStore();
      const isLoggedInComputed = computed(() => authStore.isLoggedIn);
      const userComputed = computed(() => authStore.user);
      const { logIn, logOut } = authStore;
      console.log(userComputed)

      return { isLoggedInComputed, userComputed, logIn, logOut };
    },
    components: {
      RegistrationModal,
      LoginModal
    },
    data() {
      return {
        isRegistrationModalActive: false,
        isLoginModalActive: false,
        imageError: false
      }
    },
    methods: {
      swichModal() {
        this.isRegistrationModalActive = !this.isRegistrationModalActive;
        this.isLoginModalActive = !this.isLoginModalActive;
      },
      handleImageError() {
        console.log('Error loading user image. URL: ' + this.userComputed.photo_url);
        this.imageError = true;
      }
    },
    computed: {
      isPhotoDisplayed() {
        return this.isLoggedInComputed && this.userComputed?.photo_url && !this.imageError;
      }
    }
  }
</script>

<style scoped>
  header {
    background-color:  rgb(246, 254, 240);
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    margin-bottom: 1.5em;
    min-height: 4.5em;
    z-index: 1000;
    border-bottom: 0.2px solid black;
  }

  .header-content {
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    height: 4.5em;
    display: flex;
    align-items: center;
    justify-content: space-between;
    display: flex;
    align-items: center;
    width: 90%;
    margin: auto;
  }

  .logo-container, .navbar-nav, nav {
    display: flex;
    align-items: center;
  }

  .logo {
    margin-right: 0.8em;
  }

  li {
    margin-left: 0.7em;
  }

  h1 {
    padding-top: 0.3em;
    font-size: 40px;
  }

  .router {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }

  .router:hover {
    text-decoration: underline;
  }

  .navbar-brand:hover {
    text-decoration: none;
  }

  .user-name {
    margin-left: 1em;
  }

  .bi-person-circle {
    font-size: 40px;
  }

</style>
