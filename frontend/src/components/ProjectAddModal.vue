<template>
  <ModalComponent :isActive="isActive" :title="title" @close="handleClose">
    <form @submit.prevent="handleSubmit">

      <div class="mb-3 row">
        <!-- Input form for prosjektnavn -->
        <div class="col-sm-6">
          <label for="prosjektnavn-input" class="form-label">Prosjektnavn</label>
          <input 
            type="text" 
            class="form-control" 
            id="prosjektnavn-input" 
            v-model="newProject.name" 
            placeholder="Oppgi Prosjektnavn"
            maxlength="100"
            required>
        </div>

        <!-- Input form for addresse -->
        <div class="col-sm-6">
          <label for="prosjektaddress-input" class="form-label">Adresse</label>
          <input 
            type="text" 
            class="form-control" 
            id="prosjektaddress-input" 
            v-model="newProject.address" 
            placeholder="Oppgi Addresse"
            maxlength="100"
            required>
        </div>
      </div>

      <div class="mb-3 row">
        <!-- Input form for areal (BTA) -->
        <div class="col-sm-6">
          <label for="prosjektbta-input" class="form-label">Bruttoareal (BTA)</label>
          <input 
            type="number" 
            class="form-control" 
            id="prosjektbta-input" 
            v-model="newProject.bta" 
            placeholder="Oppgi BTA"
            maxlength="100"
            min="1"
            required>
        </div>

        <!-- Dropdown menu for selecting bygningskategori -->
        <div class="col-sm-6">
          <label for="bygningskategori-dropdown" class="form-label">Bygningskategori</label>
          <select id="bygningskategori-dropdown" class="form-control" v-model="newProject.type" required>
            <option disabled value="">Velg Kategori</option>
            <option 
              v-for="bygningskategori in bygningskategorier" 
              :key="bygningskategori" 
              :value="bygningskategori">
              {{ bygningskategori }}
            </option>
          </select>
        </div>
      </div>

      <div class="mb-3 row">
        <!-- Input form for Prosjektstart -->
        <div class="col-sm-6">
          <label for="prosjektstart-input" class="form-label">Prosjektstart (år)</label>
          <input 
            type="text" 
            class="form-control" 
            id="prosjektstart-input" 
            v-model="newProject.prosjektstart" 
            min="2000"
            maxlength="100"
            pattern="^\d+$"
            required>
        </div>
        
        <!-- Input form for Analyseperiode -->
        <div class="col-sm-6">
          <label for="analyseperiode-input" class="form-label">Analyseperiode (år)</label>
          <input 
            type="number" 
            class="form-control" 
            id="analyseperiode-input" 
            v-model="newProject.analyseperiode" 
            min="1"
            maxlength="100"
            required>
        </div>
      </div>
      
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary btn-md" style="min-width:5em" @click="handleClose">Avbryt</button>
        <button type="submit" class="btn btn-success btn-md" style="min-width:8em">Opprett</button>
      </div>
    </form>
  </ModalComponent>
</template>
  
<script>
  import { klimagassreferanser } from '../utils/breeam.js'
  import { getTodaysDate } from '../utils/misc.js'
  import ModalComponent from './ModalComponent.vue';
  import { displayErrorToast } from '../utils/toasts.js'

  export default {
    name: 'ProjectUpdateModal',
    props: {
      isActive: Boolean,
    },
    components: {
      ModalComponent
    },       
    data() {
      return {
        title: "Legg til nytt prosjekt",
        bygningskategorier: Object.keys(klimagassreferanser),
        newProject: {
          'name': '',
          'type': '',
          'bta': 0,
          'analyseperiode': 50,
          'prosjektstart': 2024,
          'address': '',
          "created_date": '',
          "updated_date": '',
          "active": true,
        },
      }
    },
    methods: {
      handleClose() {
        this.$emit('close');
        this.resetNewProject();
      },
      // Ensures that newProduct is refreshed everytime the Modal is opened.
      resetNewProject() {
        this.newProject = {
          'name': '',
          'type': '',
          'bta': 0,
          'analyseperiode': 50,
          'prosjektstart': 2024,
          'address': '',
          "created_date": '',
          "updated_date": '',
          "active": true,
        }
      },
      handleSubmit() {
        const currentDate = getTodaysDate();
        // NB! Keep snake case to stay in sync with db
        this.newProject.created_date = currentDate;
        this.newProject.updated_date = currentDate;

        this.$emit('submit-project', this.newProject);
        setTimeout(this.resetNewProject, 1000);
      }
    }
  };
</script>
