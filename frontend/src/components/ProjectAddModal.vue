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
        <button type="submit" class="btn btn-primary btn-md" style="min-width:8em">Opprett</button>
      </div>
    </form>
  </ModalComponent>
</template>
  
<script setup lang="ts">
  import { klimagassreferanser } from '../utils/breeam.js';
  import { getTodaysDate } from '../utils/misc';
  import ModalComponent from './ModalComponent.vue';
  import { displayErrorToast } from '../utils/toasts';
  import { initializeProject } from '../utils/initializers.js';
  import { Project } from '../interfaces/interfaces';
  
  const props = defineProps<{ isActive: Boolean }>();
  const emit = defineEmits(['close', 'submit-project']);

  const title = "Legg til nytt prosjekt";
  const bygningskategorier = Object.keys(klimagassreferanser);

  let newProject: Project = initializeProject();

  function handleClose(): void {
    emit('close');
    setTimeout(initializeProject, 1000);
  }

  /** 
   * Initializes created and updated date as todays date
   * Emits newProject, then resets it after a short delay
   */
  function handleSubmit(): void {
    const currentDate = getTodaysDate();
    // NB! Keep snake case to stay in sync with db
    newProject.created_date = currentDate;
    newProject.updated_date = currentDate;

    emit('submit-project', newProject);
    setTimeout(initializeProject, 1000);
  }

</script>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ProjectAddModal',
});
</script>