
<template>
    <div>
      <div ref="ProjectModal" class="modal fade" :class="{ show: isActive, 'd-block': isActive }" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
  
            <!-- Header -->
            <div class="modal-header">
              <h5 class="modal-title">Logg Inn</h5>
              <button 
                type="button" 
                class="close" 
                data-dismiss="modal" 
                @click="closeModal('close')">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
  
            <div class="modal-body">
              <form @submit.prevent="handleSubmit">

                <!-- Input forms -->
                <div class="mb-3">
                <label for="login-navn-input" class="form-label">Epost</label>
                <input 
                    type="email" 
                    class="form-control" 
                    id="login-navn-input" 
                    v-model="loginInfo.email" 
                    placeholder="Oppgi Epost">
                </div>
  
                <div class="mb-3">
                  <label for="login-passord-input" class="form-label">Passord</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="login-passord-input" 
                    v-model="loginInfo.password" 
                    placeholder="Oppgi Passord">
                </div>
  
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
                  <button type="button" class="btn btn-secondary btn-md" @click="closeModal('registrer')">Opprett Bruker</button>
                </div>

              </form>
            </div>
          </div>
        </div>
      </div>
      <div v-if="isActive" class="modal-backdrop fade show"></div>
    </div>
  </template>

<script>
    import { useAuthStore } from '../stores/authStore';
    import { klimagassreferanser } from '../utils/breeam.js'
    import { useToast } from "vue-toastification";

    export default {
        name: 'LoginModal',
        props: {
            isActive: Boolean,
        },
        setup() {
            const authStore = useAuthStore();
            const { logIn } = authStore;

            const toast = useToast();

            function displaySuccessToast(message="Suksess!") {
              toast.success(message);
            }

            function displayErrorToast(message="Error!") {
              toast.error(message);
            }

            function displayWarningToast(message="Obs!") {
              toast.warning(message);
            }

            return { logIn, displaySuccessToast, displayErrorToast, displayWarningToast  };
        },
        data() {
            return {
                loginInfo: {
                    email: '',
                    password: '',
                    stayLoggedIn: true,
                },
            }
        },
        methods: {
            closeModal(eventName) {
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
            handleSubmit() {
                // TODO validate input
                if (!this.validateInput()) {
                    this.displayWarningToast("Venligst fyll ut alle obligatoriske felt");
                    return;
                }

                this.logIn(this.loginInfo);
                this.closeModal('close')
            },

            // TODO: Replace placeholder with actual validation
            validateInput() {
              if (this.loginInfo.email && this.loginInfo.password) {
                  return true;
              }
              return false;
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
  button {
        margin-right: 0.5em;
  }
  .modal-header {
      display: flex;
      justify-content: space-between;
    }
</style>
