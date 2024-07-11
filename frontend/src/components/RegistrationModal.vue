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
          required
          title="Navnet kan bare inneholde bokstaver og mellomrom"
        />
      </div>

      <!-- Input form for email -->
      <div class="mb-3">
        <label for="epost-input" class="form-label">Epost</label>
        <input
          type="email"
          class="form-control"
          id="epost-input"
          v-model="newUser.email"
          pattern=".+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*\.[a-zA-Z]+$"
          placeholder="Oppgi Epost"
        />
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
          title="Passordet må være minst 8 tegn og inneholde minst én bokstav og ett siffer"
        />
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
          title="Passordet må være minst 8 tegn og inneholde minst én bokstav og ett siffer"
        />
      </div>

      <!-- Input for uploading profile picture -->
      <div class="mb-3 image-upload">
        <label for="image-upload-input" class="form-label">Last opp profilbilde (valgfritt)</label>
        <input
          type="file"
          class="form-control"
          id="image-upload-input"
          @change="handleFileUpload"
        />
      </div>

      <!-- Checkbox for staying logged in -->
      <div class="mb-3 form-check">
        <input
          type="checkbox"
          class="form-check-input"
          id="stay-logged-in-checkbox"
          v-model="newUser.stayLoggedIn"
          checked
        />
        <label class="form-check-label" for="stay-logged-in-checkbox"> Forbli innlogget </label>
      </div>

      <div class="btn-group" role="group">
        <button type="submit" class="btn btn-primary btn-md">Opprett Bruker</button>
        <button type="button" class="btn btn-secondary btn-md" @click="handleClose('login')">
          Logg Inn
        </button>
      </div>
    </form>
  </ModalComponent>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, computed } from "vue"
import ModalComponent from "../components/ModalComponent.vue"
import { useAuthStore } from "../stores/authStore"
import { klimagassreferanser } from "../utils/breeam.js"
import { initializeUser } from "../utils/initializers"
import { postForm } from "../utils/http-requests"
import { displaySuccessToast, displayErrorToast, displayWarningToast } from "../utils/toasts"
import { ServerResponse, User, UserFormInput } from "../interfaces/interfaces"

const authStore = useAuthStore()
const props = defineProps<{ isActive: Boolean }>()
const emit = defineEmits<(event: string) => void>()
const logIn = authStore.logIn

const title = "Opprett bruker"
const enheter = ["tonn", "m3"]
const bygningskategorier = Object.keys(klimagassreferanser)

let newUser: UserFormInput = initializeUser()

// TODO: Sjekk om jeg har lov til å passe eventName på denne måten. Splitt evt dette opp.
const handleClose = (eventName: string): void => {
  emit(eventName)
  setTimeout(() => (newUser = initializeUser()), 1000)
}

/**
 * Handles the submission of new user data.
 * validates data and creates a FormData object which is posted to server
 * If the request is successfull, it calls the global logIn() to log in the user.
 */
async function handleSubmit(): Promise<void> {
  const dataValidation = validateData()
  if (dataValidation !== "ok") {
    displayWarningToast(dataValidation)
    return
  }

  // Create a FormData object to store data and image-file (if it exists)
  const formData = createFormData()
  if (!formData) return

  const db_response: ServerResponse = await postForm(formData, "/users/register")

  // If request was successful, log in and close the modal
  if (db_response.status == "success") {
    newUser = db_response.data as User
    displaySuccessToast(`Velkommen ${newUser.name}`)
    logIn(newUser)
    handleClose("close")
    return
  }

  // Otherwise flash an error message
  const errorMessage = db_response.message ?? "En feil har oppstått"
  displayErrorToast(errorMessage)
}

/**
 * Returns a FormData object containing
 * name: string, email: string, password: string, stayloggedIn: boolean, photo?: image file
 */
function createFormData(): FormData | null {
  const stayLoggedIn = newUser.stayLoggedIn ? "true" : "false"
  const formData = new FormData()

  formData.append("name", newUser.name)
  formData.append("email", newUser.email)
  formData.append("password", newUser.password)
  formData.append("stayLoggedIn", stayLoggedIn)

  // Append photo if it exists and is valid, otherwise return null
  if (newUser.photo) {
    if (!validatePhoto(newUser.photo)) return null
    formData.append("photo", newUser.photo, newUser.photo.name)
  }

  return formData
}

function handleFileUpload(event: Event): void {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    newUser.photo = target.files[0]
  }
}

function validateData(): string {
  const obligatoryInputs = ["name", "email", "password", "confirmPassword"]
  const isMissing = (key: string, value: string) => obligatoryInputs.includes(key) && value === ""

  if (Object.entries(newUser).some(([key, value]) => isMissing(key, value))) {
    return "Venligst fyll ut alle obligatoriske felt"
  } else if (newUser.password !== newUser.confirmPassword) {
    return "Passordene macher ikke"
  } else {
    return "ok"
  }
}

function validatePhoto(photo: File): boolean {
  // Check file type and file size
  if (photo === null) return false

  const allowedTypes = ["image/jpeg", "image/png", "image/gif"]
  if (!allowedTypes.includes(photo.type)) {
    displayWarningToast("Feil Bildeformat. Bruk JPEG, PNG, eller GIF.")
    return false
  }

  const maxSize = 5 * 1024 * 1024 // 5 Megabytes
  if (photo.size > maxSize) {
    displayWarningToast("Maksimum filstørrelse er 5MB.")
    return false
  }
  return true
}
</script>
<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "RegistrationModal",
})
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
