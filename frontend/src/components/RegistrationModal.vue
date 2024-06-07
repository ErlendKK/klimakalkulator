<template>
  <ModalComponent :isActive="isActive" :title="title" @close="handleClose('close')">
    <form @submit.prevent="handleSubmit">

      <!-- Input form for user name -->
        <div class="mb-3">
          <label for="navn-input" class="form-label">Navn</label>
          <input 
            type="text" 
            class="form-control" 
            id="navn-input" 
            v-model="newUser.name" 
            placeholder="Oppgi Navn"
            title="Navn mangler"
            required>
        </div>

        <!-- Input form for email -->
        <div class="mb-3">
          <label for="epost-input" class="form-label">Epost</label>
          <input 
            type="email" 
            class="form-control" 
            id="epost-input" 
            v-model="newUser.email" 
            pattern="^.+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*\.[a-zA-Z]+$"
            title="Svaret må formateres som epost (eks. navn@firma.no)"
            placeholder="Oppgi Epost"
            required>
        </div>

      <!-- Input form for password -->
      <div class="mb-3">
        <label for="passord-input" class="form-label">Passord</label>
        <input 
          type="password" 
          class="form-control" 
          id="passord-input" 
          v-model="newUser.password" 
          placeholder="Oppgi Passord"
          pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
          title="Passordet må bestå av minst 8 tegn og inneholde minst én bokstav og ett siffer"
          required>
      </div>

      <!-- Input form for repeating password -->
      <div class="mb-3">
        <input 
          type="password" 
          class="form-control" 
          id="gjenta-passord-input" 
          v-model="newUser.confirmPassword" 
          placeholder="Gjenta Passord"
          pattern="^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
          title="Passordet må bestå av minst 8 tegn og inneholde minst én bokstav og ett siffer"
          required>
      </div>

      <!-- Input for uploading profile picture -->
      <div class="mb-3 image-upload">
      <label for="image-upload-input" class="form-label">Last opp profilbilde (valgfritt)</label>
      <input 
          type="file" 
          class="form-control" 
          id="image-upload-input" 
          @change="handleFileUpload">
      </div>

      <!-- Checkbox for staying logged in -->
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
        <button type="submit" class="btn btn-success btn-md">Opprett Bruker</button>
        <button type="button" class="btn btn-secondary btn-md" @click="handleClose('login')">Logg Inn</button>
      </div>
    </form>
  </ModalComponent>
</template>
  
<script>
  import ModalComponent from '../components/ModalComponent.vue';
  import { useAuthStore } from '../stores/authStore';
  import { klimagassreferanser } from '../utils/breeam.js'
  import { postForm } from '../utils/http-requests.js'
  import { displaySuccessToast, displayErrorToast, displayWarningToast } from '../utils/toasts.js'

  export default {
    name: 'RegistrationModal',
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
        title: "Opprett bruker",
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
      handleClose(eventName) {
        this.$emit(eventName);
        this.resetNewUser();
      },
      /**
       * Ensures that input fields are empty the next time the modal opens.
       */
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
      /**
       * Handles the submission of new user data. 
       * validates data and creates a FormData object which is posted to server
       * If the request is successfull, it calls the global logIn() to log in the user.
       */
      async handleSubmit() {
        const dataValidation = this.validateData()
        if (dataValidation !== 'ok') {
          displayWarningToast(dataValidation);
          return;
        }
        console.log(this.newUser)

        // Create a FormData object to store data and image-file
        const formData = new FormData();
        formData.append('name', this.newUser.name);
        formData.append('email', this.newUser.email);
        formData.append('password', this.newUser.password);
        formData.append('stayLoggedIn', this.newUser.stayLoggedIn);
        
        // Handle photo if uploaded
        if (this.newUser.photo){
          if (this.validatePhoto(this.newUser.photo)) {
            formData.append('photo', this.newUser.photo, this.newUser.photo.name);
          } else {
            return; // cancel registration if the photo is invalid
          }
        }

        // Send userdata to server and call login 
        const db_response = await postForm(formData, '/users/register');
        if (db_response.status == 'success') {
          this.newUser = db_response.user_data;
          displaySuccessToast(`Velkommen ${this.newUser.name}`);
          this.logIn(this.newUser);
          this.handleClose('close')

        } else {
          const errorMessage = db_response.message ?? "En feil har oppstått";
          displayErrorToast(errorMessage);
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
          displayWarningToast('Feil Bildeformat. Bruk JPEG, PNG, eller GIF.')
          return false;
        }

        const maxSize = 5 * 1024 * 1024; // 5 Megabytes
        if (photo.size > maxSize) {
          displayWarningToast('Maksimum filstørrelse er 5MB.');
          return false;
        }
        return true;
      },
    }
  };
</script>

<style scoped>
  .image-upload {
    margin-top: 2.5em;
  }
  .modal-header {
    display: flex;
    justify-content: space-between;
  }
</style>
