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
            min="1"
            maxlength="100"
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
        <button type="submit" class="btn btn-success btn-md" style="min-width:8em">Oppdater</button>
      </div>
    </form>
  </ModalComponent>
</template>
    
<script>
  import { klimagassreferanser } from '../utils/breeam.js'
  import { getTodaysDate } from '../utils/misc.js'
  import ModalComponent from '../components/ModalComponent.vue';
  import cloneDeep from 'lodash/cloneDeep';

  export default {
    name: 'ProjectUpdateModal',
    props: {
      isActive: Boolean,
      projectToBeUpdated: Object,
    },
    components: {
      ModalComponent
    },       
    data() {
      return {
        title: "Oppdater prosjektet",
        bygningskategorier: Object.keys(klimagassreferanser),
        newProject: cloneDeep(this.projectToBeUpdated)
      }
    },
    mounted() {
      console.log(this.newProject)
    },
    methods: {  
      handleClose() {
        this.$emit('close');
      },
      handleSubmit() {
        console.log(this.newProject);
        // NB! Keep snake case to stay in sync with db
        this.newProject.updated_date = getTodaysDate();
        this.$emit('submit-project', this.newProject);
      }
    }
  }
</script>
