<template>
  <header class="container-fluid">
    <div class="header-content">
      <div class="logo-container">
        <router-link class="navbar-brand router" to="/">
          <img class="logo" src="/favicon.ico" width="40" height="40" />
        </router-link>
        <router-link class="navbar-brand router" to="/">
          <h1 id="page-heading">Klimakalkulator</h1>
        </router-link>
      </div>

      <!-- Modals for registration and login -->
      <registration-modal
        :is-active="isRegistrationModalActive"
        @close="isRegistrationModalActive = false"
        @login="swichModal"
      >
      </registration-modal>

      <login-modal
        :is-active="isLoginModalActive"
        @close="isLoginModalActive = false"
        @registrer="swichModal"
      >
      </login-modal>

      <nav>
        <!-- expands to horizontal when screen >= md -->
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
            <li v-if="isLoggedInComputed" class="nav-item user-name d-none d-md-block">
              {{ userComputed.name }}
            </li>
            <li v-else class="nav-item d-none d-md-block router" @click="toggleLoginModal">
              Logg Inn
            </li>
          </ul>
        </div>

        <!-- Drop down menu for user account if logedIn -->
        <ul class="nav justify-content-end navbar-nav">
          <li class="nav-item dropdown">
            <template v-if="isPhotoDisplayed">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdownMenuLink"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <img
                  class="rounded-circle profile-picture"
                  :src="userComputed.photo_url"
                  @error="handleImageError"
                  height="45"
                  loading="lazy"
                />
              </a>
            </template>
            <template v-else>
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdownMenuLink"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <i class="bi bi-person-circle rounded-circle profile-picture"></i>
              </a>
            </template>
            <ul class="dropdown-menu">
              <li v-for="item in dropDownMenuItems" :key="item">
                <a v-if="item.displayed" class="dropdown-item" href="#" @click="item.onClick()">{{
                  item.title
                }}</a>
              </li>
            </ul>
          </li>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import RegistrationModal from "../components/RegistrationModal.vue"
import LoginModal from "../components/LoginModal.vue"
import { useAuthStore } from "../stores/authStore"
import { computed, ref } from "vue"
import { User } from "../interfaces/interfaces"

const authStore = useAuthStore()
const isLoggedInComputed = computed<boolean>(() => authStore.isLoggedIn)
const userComputed = computed<User | null>(() => authStore.user)
const { logIn, logOut } = authStore

console.log("isLoggedInComputed: ", isLoggedInComputed.value)

const isRegistrationModalActive = ref<boolean>(false)
const isLoginModalActive = ref<boolean>(false)
const imageError = ref<boolean>(false)

function toggleRegistrationModal(): void {
  isRegistrationModalActive.value = !isRegistrationModalActive.value
  isLoginModalActive.value = false
}

function toggleLoginModal(): void {
  isLoginModalActive.value = !isLoginModalActive.value
  isRegistrationModalActive.value = false
}

function swichModal(): void {
  isRegistrationModalActive.value = !isRegistrationModalActive.value
  isLoginModalActive.value = !isLoginModalActive.value
}

function handleImageError(): void {
  console.log("Error loading user image. URL: " + userComputed.value.photo_url)
  imageError.value = true
}

/**
 * Controls whether to display a profile picture or a default icon.
 */
const isPhotoDisplayed = computed(() => {
  const response = isLoggedInComputed.value && userComputed.value?.photo_url && !imageError.value
  console.log("isPhotoDisplayed:" + response)
  console.log("isLoggedInComputed:" + isLoggedInComputed.value)
  return response
})

/**
 * List of items to be displayed in the dropdown menu.
 * format = [title:string, displayed:boolean, onClick:function]
 */
const dropDownMenuItems = computed(() => {
  return [
    { title: "Logg ut", displayed: isLoggedInComputed.value, onClick: () => logOut() },
    {
      title: "Registrer",
      displayed: !isLoggedInComputed.value,
      onClick: () => toggleRegistrationModal(),
    },
    { title: "Logg in", displayed: !isLoggedInComputed.value, onClick: () => toggleLoginModal() },
  ]
})
</script>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "NavHeader",
})
</script>

<style scoped>
header {
  background-color: rgb(246, 254, 240);
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
.logo-container,
.navbar-nav,
nav {
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
