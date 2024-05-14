<template>
    <div>
      <div ref="ProjectModal" class="modal fade" :class="{ show: isActive, 'd-block': isActive }" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
  
            <!-- Header -->
            <div class="modal-header">
              <h5 class="modal-title">Opprett bruker</h5>
              <button 
                type="button" 
                class="close" 
                data-dismiss="modal" 
                aria-label="Close" 
                @click="closeModal('close')">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
  
            <div class="modal-body">
              <form @submit.prevent="handleSubmit">

                <!-- Input forms -->
                  <div class="mb-3">
                    <label for="navn-input" class="form-label">Navn</label>
                    <input 
                      type="text" 
                      class="form-control" 
                      id="navn-input" 
                      v-model="newUser.name" 
                      placeholder="Oppgi Navn"
                      pattern="[A-Za-zæøåÆØÅ ]+"
                      title="Navnet kan bare inneholde bokstaver og mellomrom">
                  </div>
  
                  <div class="mb-3">
                    <label for="epost-input" class="form-label">Epost</label>
                    <input 
                      type="email" 
                      class="form-control" 
                      id="epost-input" 
                      v-model="newUser.email" 
                      placeholder="Oppgi Epost">
                  </div>

  
                <div class="mb-3">
                  <label for="passord-input" class="form-label">Passord</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    id="passord-input" 
                    v-model="newUser.password" 
                    placeholder="Oppgi Passord"
                    pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
                    title="Passordet må være minst 8 tegn og inneholde minst én bokstav og ett siffer">

                </div>
  
                <div class="mb-3">
                  <input 
                    type="password" 
                    class="form-control" 
                    id="gjenta-passord-input" 
                    v-model="newUser.confirmPassword" 
                    placeholder="Gjenta Passord"
                    pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
                    title="Passordet må være minst 8 tegn og inneholde minst én bokstav og ett siffer">
                </div>

                <div class="mb-3 image-upload">
                <label for="image-upload-input" class="form-label">Last opp profilbilde (valgfritt)</label>
                <input 
                    type="file" 
                    class="form-control" 
                    id="image-upload-input" 
                    @change="handleFileUpload">
                </div>
  
                <div class="mb-3 form-check">
                  <input 
                    type="checkbox" 
                    class="form-check-input" 
                    id="stay-logged-in-checkbox" 
                    v-model="newUser.stayLoggedIn" 
                    checked>
                  <label class="form-check-label" for="stay-logged-in-checkbox">
                    Forbli innlogget
                  </label>
                </div>
  
                <div class="btn-group" role="group">
                  <button type="submit" class="btn btn-primary btn-md">Opprett Bruker</button>
                  <button type="button" class="btn btn-secondary btn-md" @click="closeModal('login')">Logg Inn</button>
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
    import { postData, postForm } from '../utils/http-requests.js'

    export default {
        name: 'RegistrationModal',
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

            return { logIn, displaySuccessToast, displayErrorToast, displayWarningToast };
        },
        data() {
            return {
                enheter: ['tonn', 'm3'], 
                bygningskategorier: Object.keys(klimagassreferanser),
                newUser: {
                    name: '',
                    email: '',
                    password: '',
                    confirmPassword: '',
                    stayLoggedIn: true,
                    photo: null
                },
            }
        },
        methods: {
            closeModal(eventName) {
                this.$emit(eventName);
                this.resetNewUser();
            },
            // Ensures that input fields are empty the next time the modal opens.
            resetNewUser() {
                this.newUser = {
                    name: '',
                    email: '',
                    password: '',
                    confirmPassword: '',
                    stayLoggedIn: true,
                    photo: null
                };
            },
            async handleSubmit() {
                const dataValidation = this.validateData()
                if (dataValidation !== 'ok') {
                    this.displayWarningToast(dataValidation);
                    return;
                }

                // Create a FormData object to store data and image-file
                const formData = new FormData();
                formData.append('name', this.newUser.name);
                formData.append('email', this.newUser.email);
                formData.append('password', this.newUser.password);
                if (this.newUser.photo && this.validatePhoto(this.newUser.photo)) {
                    formData.append('photo', this.newUser.photo, this.newUser.photo.name);
                }

                const data = await postForm(formData, '/users');
                if (data.status == 'success') {
                  // TODO: handle logIn call backend to avoid this extra http-request, return userdata
                  this.displaySuccessToast(`Velkommen ${this.newUser.name}`);
                  this.logIn(this.newUser);
                  this.closeModal('close')
                }

                else {
                  const errorMessage = data.message ?? "En feil har oppstått";
                  this.displayErrorToast(errorMessage);
                  return;
                }
            },

            handleFileUpload(event) {
                const file = event.target.files[0];
                this.newUser.photo = file;
            },
            validateData() {
                if (Object.values(this.newUser).some(value => value === '')) {
                  return "Venligst fyll ut alle obligatoriske felt";
                } else if (this.newUser.password !== this.newUser.confirmPassword) {
                  return "Passordene macher ikke";
                } else {
                  return "ok";
                }
            },
            validatePhoto(photo) {
              // Check file type and file size
              if (photo === null) return false; 
              
              const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
              if (!allowedTypes.includes(photo.type)) {
                  this.displayWarningToast('Feil Bildeformat. Bruk JPEG, PNG, eller GIF.')
                  return false;
              }

              const maxSize = 5 * 1024 * 1024; // 5 Megabytes
              if (photo.size > maxSize) {
                  this.displayWarningToast('Maksimum filstørrelse er 5MB.');
                  return false;
              }
              return true;
            },
        }
    };
</script>

<style>
    button {
        margin-right: 0.5em;
    }
    .image-upload {
        margin-top: 2.5em;
    }
    .modal-header {
      display: flex;
      justify-content: space-between;
    }
</style>
