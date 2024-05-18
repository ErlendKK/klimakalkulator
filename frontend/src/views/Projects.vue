<template>
  <div class="layout">
    <nav-header></nav-header>

    <main class="container">
      <h2>Prosjektoversikt</h2>
      <div v-if="isLoggedInComputed">

        <button type="button" class="btn btn-primary" @click="toggleAddModal">Nytt Prosjekt</button>
        <project-add-modal
            :is-active="isAddModalActive"
            @close="isAddModalActive = false"
            @submit-project="handleAddProject">
        </project-add-modal>

        <!-- Open productUpdateModal to add new product to the project -->
        <!-- Uses v-if to trigger mounted() everytime its activated -->
        <project-update-modal
          v-if="isUpdateModalActive"
          :is-active="isUpdateModalActive"
          :projectToBeUpdated="projectToBeUpdated"
          @close="isUpdateModalActive = false"
          @submit-project="handleUpdateModalSubmit">
        </project-update-modal>
        
          <div class="form-check form-switch">
            <input 
              class="form-check-input" 
              type="checkbox" 
              role="switch" 
              id="flexSwitchCheckDefault"
              v-model="displayArchived"
              >
            <label class="form-check-label" for="flexSwitchCheckDefault">Vis arkiverte Prosjekter</label>
          </div>

        <!-- Table of projects -->
        <table class="table table-hover table-sm">
          <thead>
            <tr>
              <th v-for="entry in tableEntries" :key="entry">
                {{ entry.heading }}
                <template v-if="entry.sortable">
                  <i
                    :class="{
                      'fa-solid': true, 
                      'fa-sort': entry.body !== currentSort, 
                      'fa-sort-down': entry.body === currentSort && !sortAscending, 
                      'fa-sort-up': entry.body === currentSort && sortAscending
                    }"
                    @click="sortTable(entry)">
                  </i>
                </template>
              </th>
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

              <td>
                <div class="dropdown">
                  <a class="btn " href="#" role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
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
      </div>
      <!-- TODO: Implement page when not logged in -->
      <div v-else>
          <p>Logg inn for å se materialer</p>
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
  import { displaySuccessToast, displayErrorToast, displayWarningToast } from '../utils/toasts.js'
  import { postData, updateData, deleteData } from '../utils/http-requests'
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
        tableEntries: [
          {heading: 'Prosjektnavn', body: 'name', sortable: true},
          {heading: 'Bygningskategori', body: 'type', sortable: true},
          {heading: "Areal (BTA)", body: 'bta', sortable: true},
          {heading: "Prosjektstart", body: 'prosjektstart', sortable: true},
          {heading: "Opprettet", body: 'created_date', sortable: true},
          {heading: "Sist Endret", body: 'updated_date', sortable: true},
        ],
        displayArchived: false,
        currentSort: '',  // entry.body
        sortAscending: true,
        isAddModalActive: false,
        isUpdateModalActive: false,
        projectToBeUpdated: null
      };
    },
    methods: {
      toggleAddModal() {
        console.log(`toggleAddModal called`); // For testing
        this.isAddModalActive = !this.isAddModalActive;
      },
      toggleUpdateModal() {
        console.log(`toggleUpdateModal called`); // For testing
        this.isUpdateModalActive = !this.isUpdateModalActive;
      },
      // Update sortAscending and currentSort with the selected entry
      // Save both to local storage
      sortTable(entry) {
        console.log(entry)
        this.sortAscending = this.currentSort === entry.body ? !this.sortAscending : false;
        this.currentSort = entry.body;

        saveToLocalStorage('projectsPreferences', {
          sortAscending: this.sortAscending,
          currentSort: this.currentSort
        })
      },
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

      copyButtonHandler(project){       
        const incrementName = (name) => {
          // Look for the pattern: "(" -> digits -> ")"
          // If a match is found; extract and increment the number, and use it to replace the old number
          // Else; append "(1)" to the end of the string
          const regex = /\((\d+)\)$/; 
          const match = name.match(regex);

          if (match) {
              const num = parseInt(match[1], 10) + 1;
              return name.replace(regex, `(${num})`);
          } else {
              return `${name} (1)`;
          }
        }

        // create a deep clone to avoid entanglements
        const copiedProject = cloneDeep(project);
        copiedProject.name = incrementName(copiedProject.name);
        this.handleAddProject(copiedProject);
      },

      async handleAddProject(project) {
        project.user_id = this.userComputed.user_id;
        const db_response = await postData(project, '/register_project');

        if (db_response.status == "failed") {
          const message = db_response?.message ?? 'Registreringen av prosjektet mislyktes!';
          displayErrorToast(message);
          return;
        }

        project.project_id = db_response.project_id;
        project.products = [];
        console.log(`handleAddProject SUCCESS for ${project.name}, ID: ${project.project_id}`);
        displaySuccessToast('Prosjektet er registrert')

        this.pushToProjects(project); 
        this.isAddModalActive = false;
      },

      async handleProjectSelection(project) {
        console.log('handleProjectSelection called for: ' + project.name);
        if (!project.active) {
          displayErrorToast('Prosjektet er arkivert')
          return; 
        }

        this.setCurrentProject(project);
        this.$router.push({ path: '/products' });
      },

      async handleUpdateModalSubmit(projectData) {
        // Resets projectToBeUpdated for next time.
        this.projectToBeUpdated = null;
        console.log(projectData)
        const db_response = await updateData(projectData, '/projects/update');

        if (db_response.status === 'failed') {
          const message = db_response?.message ?? 'Prsjektet kunne ikke oppdateres!';
          displayErrorToast(message);
          return;
        }
        
        this.popFromProjects(projectData.project_id);
        this.pushToProjects(projectData);
        displaySuccessToast('Produktet er oppdatert')
        this.isUpdateModalActive = false;
      },
    },

    mounted() {
      console.log(this.projectList)
      const projectsPreferences = getFromLocalStorage('projectsPreferences');

      this.currentSort = projectsPreferences?.currentSort ?? 'Opprettet';
      this.sortAscending = projectsPreferences?.sortAscending ?? true;
    },
    computed: {
      sortedProjects() {
        // filter list by property 'active', and declare variables coding for sort-direction and data-type
        const localProjectList = this.displayArchived ? this.projectList : this.projectList.filter(p => p.active);
        const modifier = this.sortAscending ? -1 : 1;
        const dateEntries = ['created_date', 'updated_date']
        const sortByDate = dateEntries.includes(this.currentSort) ? true : false;

        // If currentSort is a date: Split the date strings into components
        // And Convert to (yyyy-mm-dd) date-format for easy comparison
        if (sortByDate) {
          return localProjectList.sort((a, b) => {

            const [dayA, monthA, yearA] = a[this.currentSort].split(".");
            const [dayB, monthB, yearB] = b[this.currentSort].split(".");
            const dateA = new Date(`${yearA}-${monthA}-${dayA}`);
            const dateB = new Date(`${yearB}-${monthB}-${dayB}`);

            return (dateA - dateB) * modifier;
          });
        }

        // Otherwise sort notmally.
        return localProjectList.sort((a, b) => {
          if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
          if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
          return 0;
        });
      }
    }
  }
</script>

<style scoped>
    button {
        margin-bottom: 1.5em;
    }
    td {
      cursor: pointer;
    }
    .archived {
      color: rgb(145, 143, 143);
      font-style: italic;
    }
</style>