<template>
  <header class="container-fluid">
    <div class="header-content">

      <div class="logo-container">
        <router-link class="navbar-brand router" to="/">
          <img class="logo" src="/favicon.ico" width="40" height="40">
        </router-link>
        <router-link class="navbar-brand router" to="/">
          <h1 id="page-heading">Klimakalkulator</h1>
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
              @click="toggleLoginModal">
              Logg inn
            </li>
          </ul>
        </div>

        <!-- Drop down menu for user account if logedIn -->
        <ul class="nav justify-content-end navbar-nav">
          <li class="nav-item dropdown">
            <template v-if="isPhotoDisplayed">
              <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <img class="rounded-circle profile-picture"
                  :src="userComputed.photo_url" 
                  @error="handleImageError"
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
            <ul class="dropdown-menu">
              <li v-for="item in dropDownMenuItems" :key="item" >
                <a v-if="item.displayed" class="dropdown-item" href="#" @click="item.onClick()">{{item.title}}</a>
              </li>
            </ul>
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

      console.log(userComputed);
      console.log('isLoggedInComputed: ' + isLoggedInComputed.value);

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
        imageError: false,
      }
    },
    methods: {
      /** 
      * Toggles the state of registrationModal and closes loginModal to avoid overlap
      */
      toggleRegistrationModal() {
        this.isRegistrationModalActive = !this.isRegistrationModalActive;
        this.isLoginModalActive = false;
      },
      /** 
      * Toggles the state of loginModal and closes registrationModal to avoid overlap
      */
      toggleLoginModal() {
        this.isLoginModalActive = !this.isLoginModalActive;
        this.isRegistrationModalActive = false;
      },
      /**
       * Toggels the state of both registration and login modals.
       */
      swichModal() {
        this.isRegistrationModalActive = !this.isRegistrationModalActive;
        this.isLoginModalActive = !this.isLoginModalActive;
      },
      /** 
      * Handles errors when loading profile pictures
      */
      handleImageError() {
        console.log('Error loading user image. URL: ' + this.userComputed.photo_url);
        this.imageError = true;
      }
    },
    computed: {
      /** 
      * Boolean controlling whether to display a profile picture
      */
      isPhotoDisplayed() {
        const response = this.isLoggedInComputed && this.userComputed?.photo_url && !this.imageError;
        console.log('isPhotoDisplayed:' + response);
        console.log('isLoggedInComputed:' + this.isLoggedInComputed)
        return response;
      },
      /** 
      * List of items to be displayed in the dropdown menu.
      * format = [title:string, displayed:boolean, onClick:function]
      */
      dropDownMenuItems() { 
        return [
          // {title: 'Logg ut', displayed: this.isLoggedInComputed, onClick: () => null},
          {title: 'Logg ut', displayed: this.isLoggedInComputed, onClick: () => this.logOut()},
          {title: 'Registrer', displayed: !this.isLoggedInComputed, onClick: () => this.toggleRegistrationModal()},
          {title: 'Logg in', displayed: !this.isLoggedInComputed, onClick: () => this.toggleLoginModal(), },
        ];
      }
    }
  }
</script>

<style scoped>
  header {
    /* background-color:  rgb(246, 254, 240); */
    background-color: #f5f9ed;
    /* background-color: #C0D3C2; */
    position: fixed; 
    left: 0;
    top: 0;
    right: 0;
    margin-bottom: 1.5em;
    min-height: 4.5em;
    z-index: 1000;
    border-bottom: 0.2px solid black;
  }
  /* Adjust heading size for small screens */
  @media (max-width: 520px) {
    #page-heading {
      font-size: 22px;
    }
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
