<template>
  <div class="layout">
    <nav-header></nav-header>
    <main class="container">
      <h2>Prosjektoversikt</h2>
      <div v-if="isLoggedInComputed">
        <button type="button" class="btn btn-primary toggle-modal-button" @click="toggleAddModal">
          Nytt Prosjekt
        </button>
        <project-add-modal
          :is-active="isAddModalActive"
          @close="isAddModalActive = false"
          @submit-project="handleAddProject"
        >
        </project-add-modal>

        <!-- Open productUpdateModal to add new product to the project -->
        <project-update-modal
          v-if="isUpdateModalActive"
          :is-active="isUpdateModalActive"
          :projectToBeUpdated="projectToBeUpdated"
          @close="isUpdateModalActive = false"
          @submit-project="handleUpdateModalSubmit"
        >
        </project-update-modal>

        <div class="form-check form-switch">
          <input
            class="form-check-input"
            type="checkbox"
            role="switch"
            id="flexSwitchCheckDefault"
            v-model="displayArchived"
          />
          <label class="form-check-label" for="flexSwitchCheckDefault"
            >Vis arkiverte Prosjekter</label
          >
        </div>

        <!-- Table of projects -->
        <div class="table-responsive-md">
          <table class="table table-hover table-sm">
            <thead class="table-light">
              <tr>
                <!-- For sortable columns display sort-icon and listen for click -->
                <th v-for="entry in tableEntries" :key="entry">
                  <template v-if="entry.sortable">
                    <button
                      type="button"
                      class="btn btn-default heading text-start text-nowrap"
                      @click="sortTable(entry)"
                    >
                      {{ entry.heading }}
                      <i
                        :class="{
                          'fa-solid': true,
                          'fa-sort': entry.body !== currentSort,
                          'fa-sort-down': entry.body === currentSort && sortAscending,
                          'fa-sort-up': entry.body === currentSort && !sortAscending,
                          'faded-icon': true,
                        }"
                      >
                      </i>
                    </button>
                  </template>
                  <template v-else>
                    <button
                      type="button"
                      disabled
                      class="btn btn-default border border-0 heading"
                      style="padding-left: 0; font-weight: bold"
                    >
                      {{ entry.heading }}
                    </button>
                  </template>
                </th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(project, index) in sortedProjects" :key="index">
                <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">
                  {{ project.name }}
                </td>
                <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">
                  {{ project.type }}
                </td>
                <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">
                  {{ project.bta }}
                </td>
                <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">
                  {{ project.prosjektstart }}
                </td>
                <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">
                  {{ project.created_date }}
                </td>
                <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">
                  {{ project.updated_date }}
                </td>

                <!-- Dropdown menu for project-rows -->
                <td>
                  <div class="dropdown">
                    <a
                      class="btn ellipsis-container"
                      href="#"
                      role="button"
                      id="dropdownMenuLink"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    >
                      <i class="fa-solid fa-ellipsis"></i>
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                      <li>
                        <a class="dropdown-item" href="#" @click="editButtonHandler(project)"
                          >Rediger</a
                        >
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="copyButtonHandler(project)"
                          >Lag kopi</a
                        >
                      </li>
                      <template v-if="project.active">
                        <li>
                          <a class="dropdown-item" href="#" @click="toggleActive(project)"
                            >Arkiver</a
                          >
                        </li>
                      </template>
                      <template v-else>
                        <li>
                          <a class="dropdown-item" href="#" @click="toggleActive(project)"
                            >Aktiver</a
                          >
                        </li>
                      </template>
                      <div class="dropdown-divider"></div>
                      <li>
                        <a class="dropdown-item" href="#" @click="deleteButtonHandler(project)"
                          >Slett</a
                        >
                      </li>
                    </ul>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <p class="placeholder-glow if-copying-active" v-if="isCopyInProgress">
            <span class="placeholder col-12 if-copying-active"></span>
          </p>
        </div>
      </div>
      <div v-else>
        <p>Logg inn for å opprette et prosjekt</p>
      </div>
    </main>
    <nav-footer></nav-footer>
  </div>
</template>

<script setup lang="ts">
import NavFooter from "../components/NavFooter.vue"
import NavHeader from "../components/NavHeader.vue"
import ProjectAddModal from "../components/ProjectAddModal.vue"
import ProjectUpdateModal from "../components/ProjectUpdateModal.vue"
import cloneDeep from "lodash/cloneDeep"
import { displaySuccessToast, displayErrorToast } from "../utils/toasts"
import { postData, updateData, deleteData } from "../utils/http-requests"
import { saveToLocalStorage, getFromLocalStorage } from "../utils/local-storage"
import { useAuthStore } from "../stores/authStore"
import { computed, ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { sortByDate, sortByField, getNextId } from "../utils/misc"
import {
  ServerResponse,
  User,
  Product,
  Project,
  TableEntry,
  SortPreference,
} from "../interfaces/interfaces"

const authStore = useAuthStore()
const router = useRouter()

const isLoggedInComputed = computed<boolean>(() => authStore.isLoggedIn)
const userComputed = computed<User | null>(() => authStore.user)
const projectList = computed<Project[]>(() => authStore.projects)
const setCurrentProject = authStore.setCurrentProject
const pushToProjects = authStore.pushToProjects
const popFromProjects = authStore.popFromProjects

/************************************
 ***********DISPLAY TABLE*************
 ************************************/

// variables for sorting and displaying table rows
let displayArchived = ref<boolean>(false)
let currentSort = ref<string>("")
let sortAscending = ref<boolean>(true)

const tableEntries: TableEntry[] = [
  { heading: "Prosjektnavn", body: "name", sortable: true },
  { heading: "Bygningskategori", body: "type", sortable: true },
  { heading: "Areal (BTA)", body: "bta", sortable: true },
  { heading: "Prosjektstart", body: "prosjektstart", sortable: true },
  { heading: "Opprettet", body: "created_date", sortable: true },
  { heading: "Sist Endret", body: "updated_date", sortable: true },
]

// Update sortAscending and currentSort with the selected entry
// Save both to local storage
function sortTable(entry: TableEntry): void {
  sortAscending.value = currentSort.value === entry.body ? !sortAscending : false
  currentSort.value = entry.body

  saveToLocalStorage("projectsPreferences", {
    sortAscending: sortAscending,
    currentSort: currentSort,
  })
}

// When the page loads; get currentSort and sortAscending from localeStorage
onMounted(() => {
  console.log("projectList")
  console.log(projectList)
  const projectsPreferences: SortPreference = getFromLocalStorage("projectsPreferences")

  currentSort.value = projectsPreferences?.currentSort ?? "Opprettet"
  sortAscending.value = projectsPreferences?.sortAscending ?? true
})

const sortedProjects = computed(() => {
  // filter list by property 'active', and declare variables coding for sort-direction and data-type
  const activeProjects: Project[] = projectList.value?.filter((p) => p.active) ?? []
  const localProjectList: Project[] = displayArchived.value ? projectList.value : activeProjects
  const modifier = sortAscending ? -1 : 1

  // Select sorting-function based on data-format
  const isSortByDate = (): boolean => {
    const dateEntries = ["created_date", "updated_date"]
    return dateEntries.includes(currentSort.value)
  }

  if (isSortByDate()) {
    return sortByDate(localProjectList, currentSort.value, modifier)
  } else {
    return sortByField(localProjectList, currentSort.value, modifier)
  }
})

// Handler for clicking a project => this project is now active
async function handleProjectSelection(project: Project): Promise<void> {
  console.log("handleProjectSelection called for: " + project.name)
  if (!project.active) {
    displayErrorToast("Prosjektet er arkivert")
    return
  }

  setCurrentProject(project)
  await router.push({ path: "/products" })
}

/************************************
 **********DROPDOWN MENU**************
 ************************************/

let isCopyInProgress = ref<boolean>(false)

async function deleteButtonHandler(project: Project): Promise<void> {
  console.log(`deleteButtonHandler called for ${project.project_id}`)
  // Handles logged-in users
  if (isLoggedInComputed) {
    const db_response: ServerResponse = await deleteData(`/projects/delete/${project.project_id}`)

    if (db_response.status !== "success") {
      const message: string = db_response?.message ?? "Prosjektet kunne ikke slettes!"
      displayErrorToast(message)
      return
    }
  }

  // Handles all users
  displaySuccessToast("Prosjektet er slettet!")
  popFromProjects(project.project_id)
}

async function copyButtonHandler(project: Project): Promise<void> {
  console.log("isCopyInProgress:", isCopyInProgress.value)
  if (isCopyInProgress.value) {
    displayErrorToast("Kopiering pågår, venligst vent.")
    return
  }
  isCopyInProgress.value = true

  const incrementName = (name: string): string => {
    // Look for the pattern: "(", digits, ")"
    // If found; extract and increment the number, and use it to replace the old number
    // Else; append "(1)" to the end of the string
    const regex = /\((\d+)\)$/
    const match = name.match(regex)

    if (!match) return `${name} (1)`

    const num: number = parseInt(match[1]) + 1
    return name.replace(regex, `(${num})`)
  }

  // create a deep clone to avoid entanglements
  const copiedProject: Project = cloneDeep(project)
  copiedProject.name = incrementName(copiedProject.name)
  copiedProject.products.forEach((p) => {
    delete p.project_id
    delete p.product_id
  })

  await handleAddProject(copiedProject)
  isCopyInProgress.value = false
}

/**
 * For logged-in users: send the update to the server for validation
 * For Guests: directly update global state
 */
async function toggleActive(project: Project): Promise<void> {
  project.active = project.active === 1 ? 0 : 1 // reverse the value

  // Handles logged-in users
  if (isLoggedInComputed) {
    const db_response: ServerResponse = await updateData(project, "/projects/update")

    if (db_response.status === "failed") {
      const message: string = db_response?.message ?? "Prosjektet kunne ikke oppdateres"
      displayErrorToast(message)
      return
    }
  }

  // Handles all users
  const message: string = project.active ? "Prosjektet er aktivert" : "Prosjektet er arkivert"
  displaySuccessToast(message)
}

/************************************
 ***********ADD PRODUCT***************
 ************************************/

let isAddModalActive = ref<boolean>(false)

function toggleAddModal(): void {
  console.log(`toggleAddModal called`)
  isAddModalActive.value = !isAddModalActive.value
}

/**
 * Logged-in users: send the project data to the server for validation
 * Guests: directly add the new project to global state
 */
async function handleAddProject(project: Project) {
  project.user_id = userComputed.value.user_id
  console.log(project)
  // Handles guests
  if (!isLoggedInComputed) {
    handleAddGuestProject(project)
    return
  }

  // Handles logged-in users
  const db_response: ServerResponse = await postData(project, "/projects/register")
  if (db_response.status == "failed") {
    const message = db_response?.message ?? "Registreringen av prosjektet mislyktes!"
    displayErrorToast(message)
    return
  }

  const projectData = db_response.data as Project
  project.project_id = projectData.project_id
  project.products = projectData.products
  console.log(`handleAddProject SUCCESS for ${project.name}, ID: ${project.project_id}`)
  displaySuccessToast("Prosjektet er registrert")

  pushToProjects(project)
  isAddModalActive.value = false
}

function handleAddGuestProject(project: Project): void {
  project.project_id = getNextId("project")
  project.products = []
  console.log(`handleAddProject SUCCESS for ${project.name}, ID: ${project.project_id}`)
  displaySuccessToast("Prosjektet er registrert. Logg inn for å lagre prosjektdata på serveren")

  pushToProjects(project)
  isAddModalActive.value = false
}

/************************************
 ***********UPDATE PRODUCT************
 ************************************/

let isUpdateModalActive = ref<boolean>(false)
let projectToBeUpdated = ref<Project | null>(null)

function toggleUpdateModal(): void {
  console.log(`toggleUpdateModal called`)
  isUpdateModalActive.value = !isUpdateModalActive.value
}

function editButtonHandler(project: Project): void {
  console.log("Editing project:", project.name)
  console.log("projectToBeUpdated.value:", projectToBeUpdated.value)
  console.log("project:", project)
  if (!project.active) {
    displayErrorToast("Prosjektet er arkivert")
    return
  }
  projectToBeUpdated.value = project
  console.log(projectToBeUpdated.value)
  toggleUpdateModal()
}

/**
 * Logged-in users: send the projectData to the server for validation
 * Guests: directly replace the exisiting project in global state
 */
async function handleUpdateModalSubmit(projectData: Project): Promise<void> {
  console.log(projectData)
  if (isLoggedInComputed) {
    const db_response = await updateData(projectData, "/projects/update")

    if (db_response.status === "failed") {
      const message = db_response?.message ?? "Prsjektet kunne ikke oppdateres!"
      displayErrorToast(message)
      return
    }
  }

  projectToBeUpdated = null // Resets modal
  popFromProjects(projectData.project_id)
  pushToProjects(projectData)
  displaySuccessToast("Produktet er oppdatert")
  setTimeout(() => (isUpdateModalActive.value = false), 1000)
}
</script>

<style scoped>
.heading {
  width: 100%;
  padding: 0.1em;
  padding-left: 0;
  font-weight: bold;
}
.faded-icon {
  opacity: 0.6;
}
.toggle-modal-button {
  margin-bottom: 1.5em;
}
td {
  cursor: pointer;
}
.archived {
  color: rgb(145, 143, 143);
  font-style: italic;
}
.ellipsis-container {
  padding-top: 0.1em;
  padding-bottom: 0.1em;
  margin: 0;
}
.if-copying-active {
  margin-top: -0.5em;
  padding-top: 0;
  height: 2em;
}

/* Thanks to leocaseiro https://dcblog.dev/stop-bootstrap-drop-menus-being-cut-off-in-responsive-tables  */
@media (max-width: 767px) {
  .table-responsive-md .dropdown-menu {
    position: static !important;
    -webkit-overflow-scrolling: touch;
  }
}
@media (min-width: 768px) {
  .table-responsive {
    overflow: visible;
  }
}
</style>
