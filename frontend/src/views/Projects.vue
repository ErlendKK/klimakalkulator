<template>
  <div class="layout">
    <nav-header></nav-header>
    <main class="container">
      <h2>Prosjektoversikt</h2>
      <div class="card mb-3">
        <div class="card-body">

          <div v-if="isLoggedInComputed">
            <button type="button" class="btn btn-success toggle-modal-button" @click="toggleAddModal">Nytt Prosjekt</button>
            <project-add-modal
              :is-active="isAddModalActive"
              @close="isAddModalActive = false"
              @submit-project="handleAddProject">
            </project-add-modal>

            <!-- Open productUpdateModal to add new product to the project -->
            <project-update-modal
              v-if="isUpdateModalActive"
              :is-active="isUpdateModalActive"
              :projectToBeUpdated="projectToBeUpdated"
              @close="isUpdateModalActive = false"
              @submit-project="handleUpdateModalSubmit">
            </project-update-modal>
        
            <div class="form-check form-switch">
              <input 
                class="form-check-input custom-switch" 
                type="checkbox" 
                role="switch" 
                id="flexSwitchCheckDefault"
                v-model="displayArchived"
                >
              <label class="form-check-label" for="flexSwitchCheckDefault">Vis arkiverte Prosjekter</label>
            </div>

        <!-- Table of projects -->
            <div class="table-responsive-lg">
            <table class="table table-hover table-sm" >
              <thead class="table-light">
                <tr>
                  <!-- For sortable columns display sort-icon and listen for click -->
                  <th v-for="entry in tableEntries" :key="entry">
                    <template  v-if="entry.sortable">
                      <button type="button" class="btn btn-default heading text-start text-nowrap"
                        @click="sortTable(entry)">
                        {{ entry.heading }}
                        <i
                          :class="{
                            'fa-solid': true, 
                            'fa-sort': entry.body !== currentSort, 
                            'fa-sort-down': entry.body === currentSort && sortAscending, 
                            'fa-sort-up': entry.body === currentSort && !sortAscending,
                            'faded-icon': true 
                          }">
                        </i>
                      </button>
                    </template>
                    <template  v-else>
                      <button type="button" disabled class="btn btn-default border border-0 heading" style="padding-left: 0; font-weight: bold;">
                      {{ entry.heading }}
                      </button>
                    </template>
                  </th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(project, index) in sortedProjects" :key="index">
                  <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">{{ project.name }}</td>
                  <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">{{ project.type }}</td>
                  <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">{{ project.bta }}</td>
                  <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">{{ project.prosjektstart }}</td>
                  <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">{{ project.created_date }}</td>
                  <td :class="{ archived: !project.active }" @click="handleProjectSelection(project)">{{ project.updated_date }}</td>

                  <!-- Dropdown menu for project-rows -->
                  <td>
                    <div class="dropdown">
                      <a class="btn ellipsis-container" href="#" role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
                        <i class="fa-solid fa-ellipsis"></i>
                      </a>
                      <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                        <li><a class="dropdown-item" href="#" @click="editButtonHandler(project)">Rediger</a></li>
                        <li><a class="dropdown-item" href="#" @click="copyButtonHandler(project)">Lag kopi</a></li>
                        <template v-if="project.active">
                          <li><a class="dropdown-item" href="#" @click="toggleActive(project)">Arkiver</a></li>
                        </template>
                        <template v-else>
                          <li><a class="dropdown-item" href="#" @click="toggleActive(project)">Aktiver</a></li>
                        </template>
                        <div class="dropdown-divider"></div>
                        <li><a class="dropdown-item" href="#" @click="deleteButtonHandler(project)">Slett</a></li>
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

          <!-- Placeholder if logged out -->
          <div v-else>
            <p>Logg inn for å se prosjekter</p>
          </div>

        </div>
      </div>
    </main>
    <nav-footer></nav-footer>
  </div>
</template>
  
<script>
  import NavFooter from '../components/NavFooter.vue';
  import NavHeader from '../components/NavHeader.vue';
  import ProjectAddModal from '../components/ProjectAddModal.vue';
  import ProjectUpdateModal from '../components/ProjectUpdateModal.vue';
  import cloneDeep from 'lodash/cloneDeep';
  import { displaySuccessToast, displayErrorToast } from '../utils/toasts.js'
  import { postData, updateData, deleteData } from '../utils/http-requests.js'
  import { sortByDate, sortByField } from '../utils/misc.js'
  import { saveToLocalStorage, getFromLocalStorage } from '../utils/local-storage.js'
  import { useAuthStore } from '../stores/authStore';
  import { computed } from 'vue';
  
  export default {
      name: 'Projects',
      components: {
        NavHeader,
        NavFooter,
        ProjectAddModal,
        ProjectUpdateModal
      },
      setup() {
      const authStore = useAuthStore();
      const isLoggedInComputed = computed(() => authStore.isLoggedIn);
      const userComputed = computed(() => authStore.user);
      const projectList = computed(() => authStore.projects);
      const setCurrentProject = authStore.setCurrentProject;
      const pushToProjects = authStore.pushToProjects;
      const popFromProjects = authStore.popFromProjects;

      return { isLoggedInComputed, userComputed, projectList, 
        setCurrentProject, pushToProjects, popFromProjects
      };
    },
    data() {
      return {
        // Table content
        tableEntries: [
          {heading: 'Prosjektnavn', body: 'name', sortable: true},
          {heading: 'Bygningskategori', body: 'type', sortable: true},
          {heading: "Areal (BTA)", body: 'bta', sortable: true},
          {heading: "Prosjektstart", body: 'prosjektstart', sortable: true},
          {heading: "Opprettet", body: 'created_date', sortable: true},
          {heading: "Sist Endret", body: 'updated_date', sortable: true},
        ],
        // Modal data
        isAddModalActive: false,
        isUpdateModalActive: false,
        projectToBeUpdated: null,
        // Table data
        currentSort: '',
        sortAscending: true,
        displayArchived: false,
        isCopyInProgress: false
      };
    },
    methods: {
      /**
       * Toggle modales
       */
      toggleAddModal() {
        console.log(`toggleAddModal called`); // For testing
        this.isAddModalActive = !this.isAddModalActive;
      },
      toggleUpdateModal() {
        console.log(`toggleUpdateModal called`); // For testing
        this.isUpdateModalActive = !this.isUpdateModalActive;
      },
      /**
       * Sort the table by the heading indicated by currentSort and direction indicated by sortAscending
       * Store the updated preferenses in locale storeage
       */
      sortTable(entry) {
        this.sortAscending = this.currentSort === entry.body ? !this.sortAscending : false;
        this.currentSort = entry.body;

        saveToLocalStorage('projectsPreferences', {
          sortAscending: this.sortAscending,
          currentSort: this.currentSort
        })
      },
      /**
       * Set selected project as "current project", and update global state.
       */
      async handleProjectSelection(project) {
        console.log('handleProjectSelection called for: ' + project.name);
        if (!project.active) {
          displayErrorToast('Prosjektet er arkivert')
          return; 
        }

        this.setCurrentProject(project);
        this.$router.push({ path: '/products' });
      },
      /**
       * Handlers for click events from the drop-down menu
       * Submit to server and update global state
       */
      async toggleActive(project) {
        project.active = !project.active;
        const db_response = await updateData(project, '/projects/update');

        if (db_response.status === 'failed') {
          const message = db_response?.message ?? 'Prosjektet kunne ikke oppdateres';
          displayErrorToast(message);
          return;
        }
        const message = project.active ? 'Prosjektet er aktivert' : 'Prosjektet er arkivert';
        displaySuccessToast(message);
      },
      editButtonHandler(project) {
        if (!project.active) {
          displayErrorToast('Prosjektet er arkivert');
          return;
        }
        console.log('Editing project:', project.name);
        this.projectToBeUpdated = project;
        console.log(this.projectToBeUpdated)
        this.toggleUpdateModal();
      },
      async deleteButtonHandler(project) {
        console.log('deleteButtonHandler called');
        const project_id = project.project_id
        console.log(`${project.project_id}`)
        const db_response = await deleteData(`/projects/delete/${project_id}`)
        
        if (db_response.status !== 'success') {
          const message = db_response?.message ?? 'Prosjektet kunne ikke slettes!';
          displayErrorToast(message);
          return;
        }

        displaySuccessToast('Prosjektet er slettet!')
        this.popFromProjects(project_id);
      },
      async copyButtonHandler(project){
        if (this.isCopyInProgress) {
            displayErrorToast('Kopiering pågår, venligst vent.');
            return;
        }
        this.isCopyInProgress = true;   

        const incrementName = (name) => {
          // Look for the pattern: "(", digits, ")"
          // If found; extract and increment the number, and use it to replace the old number
          // Else; append "(1)" to the end of the string
          const regex = /\((\d+)\)$/; 
          const match = name.match(regex);

          if (!match) return `${name} (1)`;

          const num = parseInt(match[1]) + 1;
          return name.replace(regex, `(${num})`);
        }

        // create a deep clone to avoid entanglements
        const copiedProject = cloneDeep(project);
        copiedProject.name = incrementName(copiedProject.name);
        copiedProject.products.forEach(p => {
          delete p.project_id
          delete p.product_id
        });

        await this.handleAddProject(copiedProject);
        this.isCopyInProgress = false;   
      },
      async handleUpdateModalSubmit(projectData) {
        console.log(projectData)
        const db_response = await updateData(projectData, '/projects/update');

        if (db_response.status === 'failed') {
          const message = db_response?.message ?? 'Prsjektet kunne ikke oppdateres!';
          displayErrorToast(message);
          return;
        }
        
        this.projectToBeUpdated = null; // Resets modal
        this.popFromProjects(projectData.project_id);
        this.pushToProjects(projectData);
        displaySuccessToast('Produktet er oppdatert');
        this.isUpdateModalActive = false;
      },
      async handleAddProject(project) {
        project.user_id = this.userComputed.user_id;
        console.log(project);
        const db_response = await postData(project, '/projects/register');

        if (db_response.status == "failed") {
          const message = db_response?.message ?? 'Registreringen av prosjektet mislyktes!';
          displayErrorToast(message);
          return;
        }
        console.log('db_response')
        console.log(db_response)

        project.project_id = db_response.project_id;
        project.products = db_response?.data?.products ?? [];
        console.log(`handleAddProject SUCCESS for ${project.name}, ID: ${project.project_id}`);
        displaySuccessToast('Prosjektet er registrert')

        this.pushToProjects(project); 
        this.isAddModalActive = false;
      },
    },
    /**
     * When the page loads; get sort-preferences from local storage andsort the project-table
     */
    mounted() {
      console.log(this.projectList);
      const projectsPreferences = getFromLocalStorage('projectsPreferences');

      this.currentSort = projectsPreferences?.currentSort ?? 'Opprettet';
      this.sortAscending = projectsPreferences?.sortAscending ?? true;
    },
    computed: {
      sortedProjects() {
        // filter list by property 'active', and declare variables coding for sort-direction and data-type
        const activeProjects = this.projectList?.filter(p => p.active) ?? [];
        const localProjectList = this.displayArchived ? this.projectList : activeProjects;
        const modifier = this.sortAscending ? -1 : 1;
        
        // Select sorting-function based on data-format
        const isSortByDate = () => {
          const dateEntries = ['created_date', 'updated_date'];
          return dateEntries.includes(this.currentSort);
        };

        if (isSortByDate()) {
          return sortByDate(localProjectList, this.currentSort, modifier);
        } else {
          return sortByField(localProjectList, this.currentSort, modifier);
        }
      }
    }
  }
</script>

<style scoped>
  h2 {
    margin-bottom: 1.4rem;
    margin-top: 0.2rem;
  }
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
  /* Set check box color */
  .custom-switch:checked {
    background-color: #28a745;
    border-color: #28a745;
  }
  .custom-switch:checked:focus {
    box-shadow: 0 0 0 0.25rem rgba(40, 167, 69, 0.25);
  }
  /* 
    Alows dropdown menus inside table-responsive-md elements to work properly on small screens
    - For small screens (width <= 767px): dropdown menus have a static position
    - For small screens (width >= 768px): table-responsive elements overflow visibly => full content display

    Thanks to leocaseiro https://dcblog.dev/stop-bootstrap-drop-menus-being-cut-off-in-responsive-tables  
  */
  @media (max-width: 991px) {
    .table-responsive-lg .dropdown-menu {
      position: static !important;
      -webkit-overflow-scrolling: touch; /* Enables smooth scrolling on touch screens*/
    }
  }
  @media (min-width: 992px) {
    .table-responsive {
        overflow: visible;
    }
  }
</style>