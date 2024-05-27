<template>
  <ModalComponent :isActive="isActive" :title="title" @close="handleClose('close')">
    <form @submit.prevent="handleSubmit">

      <!-- Input form for email -->
      <div class="mb-3">
        <label for="login-email-input" class="form-label">Epost</label>
        <input 
          type="email" 
          class="form-control" 
          id="login-email-input" 
          v-model="loginInfo.email" 
          placeholder="Oppgi Epost">
      </div>

      <!-- Input form for password -->
      <div class="mb-3">
        <label for="login-passord-input" class="form-label">Passord</label>
        <input 
          type="password" 
          class="form-control" 
          id="login-passord-input" 
          v-model="loginInfo.password" 
          placeholder="Oppgi Passord">
      </div>

      <!-- Checkbox for staying logged in -->
      <div class="mb-3 form-check">
        <input 
          type="checkbox" 
          class="form-check-input" 
          id="login-stay-logged-in-checkbox" 
          v-model="loginInfo.stayLoggedIn" 
          checked>
        <label class="form-check-label" for="login-stay-logged-in-checkbox">
          Forbli innlogget
        </label>
      </div>

      <div class="btn-group" role="group">
        <button type="submit" class="btn btn-primary btn-md">Logg Inn</button>
        <button type="button" class="btn btn-secondary btn-md" @click="handleClose('registrer')">Opprett Bruker</button>
      </div>

    </form>
  </ModalComponent>
</template>

<script>
  import ModalComponent from '../components/ModalComponent.vue';
  import { useAuthStore } from '../stores/authStore';
  import { postData } from '../utils/http-requests.js'
  import { displaySuccessToast, displayWarningToast } from '../utils/toasts.js'

  export default {
    name: 'LoginModal',
    props: {
      isActive: Boolean,
    },
    components: {
      ModalComponent
    },
    setup() {
      const authStore = useAuthStore();
      const { logIn } = authStore;
      return { logIn };
    },
    data() {
      return {
        title: "Logg inn",
        loginInfo: {
          email: '',
          password: '',
          stayLoggedIn: true,
        },
      }
    },

    methods: {
      handleClose(eventName) {
        this.$emit(eventName);
        this.resetLoginInfo();
      },
      // Ensures that newProduct is refreshed everytime the Modal is opened.
      resetLoginInfo() {
        this.loginInfo = {
          email: '',
          password: '',
          stayLoggedIn: true,
        };
      },
      async handleSubmit() {
        if (!this.validateInput()) {
          displayWarningToast("Venligst fyll ut alle obligatoriske felt");
          return;
        }

        const user = await postData(this.loginInfo, '/login');
        if (user.status != 'success') {
          displayWarningToast("Feil epost eller passord");
          return;
        }

        displaySuccessToast(`Velkommen ${user.name}`);
        this.logIn(user);
        this.handleClose('close');
      },

      // make sure inputs are non-empty
      validateInput() {
        return this.loginInfo.email.length && this.loginInfo.password.length;
      },
    }
  };
</script>


<style scoped>
  .close {
    display:flex;
    align-items: center;
    justify-content: center;
  }
  .modal-header {
    display: flex;
    justify-content: space-between;
  }
</style>
