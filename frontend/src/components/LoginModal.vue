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
          pattern=".+@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*\.[a-zA-Z]+$"
          placeholder="Oppgi Epost"
        />
      </div>

      <!-- Input form for password -->
      <div class="mb-3">
        <label for="login-passord-input" class="form-label">Passord</label>
        <input
          type="password"
          class="form-control"
          id="login-passord-input"
          v-model="loginInfo.password"
          minlength="8"
          placeholder="Oppgi Passord"
        />
      </div>

      <!-- Checkbox for staying logged in -->
      <div class="mb-3 form-check">
        <input
          type="checkbox"
          class="form-check-input"
          id="login-stay-logged-in-checkbox"
          v-model="loginInfo.stayLoggedIn"
          minlength="8"
          checked
        />
        <label class="form-check-label" for="login-stay-logged-in-checkbox">
          Forbli innlogget
        </label>
      </div>

      <div class="btn-group" role="group">
        <button type="submit" class="btn btn-primary btn-md">Logg Inn</button>
        <button type="button" class="btn btn-secondary btn-md" @click="handleClose('registrer')">
          Opprett Bruker
        </button>
      </div>
    </form>
  </ModalComponent>
</template>

<script setup lang="ts">
import ModalComponent from "../components/ModalComponent.vue"
import { defineProps, defineEmits, ref, computed } from "vue"
import { useAuthStore } from "../stores/authStore"
import { postData } from "../utils/http-requests"
import { initializeUser } from "../utils/initializers"
import { displaySuccessToast, displayWarningToast } from "../utils/toasts"
import { ServerResponse, User, UserFormInput } from "../interfaces/interfaces"

const authStore = useAuthStore()
const props = defineProps<{ isActive: Boolean }>()
const logIn = authStore.logIn

const title = "Logg inn"
const initialLoginInfo: { email: string; password: string; stayLoggedIn: boolean } = {
  email: "",
  password: "",
  stayLoggedIn: false,
}

let loginInfo = initialLoginInfo
const emit = defineEmits<(event: string) => void>()

// TODO: Sjekk om jeg har lov til å passe eventName på denne måten. Splitt evt dette opp.
const handleClose = (eventName: string): void => {
  emit(eventName)
  setTimeout(() => (loginInfo = initialLoginInfo), 1000)
}

/**
 * Sends a login request to the server.
 * If the request is successfuls; call the global logIn() to log in the user.
 */
async function handleSubmit(): Promise<void> {
  console.log(loginInfo)
  const db_response = await postData(loginInfo, "/login")
  if (db_response.status != "success") {
    displayWarningToast("Feil epost eller passord")
    return
  }

  const newUser = db_response.data as User
  displaySuccessToast(`Velkommen ${newUser.name}`)
  logIn(newUser)
  handleClose("close")
}
</script>
<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "LoginModal",
})
</script>
<style scoped>
.close {
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-header {
  display: flex;
  justify-content: space-between;
}
</style>
