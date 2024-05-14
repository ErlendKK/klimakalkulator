<template>
    <div>
      <div ref="ProjectModal" class="modal fade" :class="{ show: isActive, 'd-block': isActive }" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Legg til nytt prosjekt</h5>
              <button 
                type="button" 
                class="close" 
                data-dismiss="modal" 
                aria-label="Close" 
                @click="closeModal">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
  
            <div class="modal-body">
              <form @submit.prevent="handleSubmit">

                <div class="mb-3 row">
                    <!-- Input form for prosjektnavn -->
                    <div class="col-md-6">
                        <label for="prosjektnavn-input" class="form-label">Prosjektnavn</label>
                        <input 
                            type="text" 
                            class="form-control" 
                            id="prosjektnavn-input" 
                            v-model="newProject.name" 
                            placeholder="Oppgi Prosjektnavn"
                            required>
                    </div>
                     <!-- Input form for addresse -->
                    <div class="col-md-6">
                        <label for="prosjektaddress-input" class="form-label">Adresse</label>
                        <input 
                            type="text" 
                            class="form-control" 
                            id="prosjektaddress-input" 
                            v-model="newProject.address" 
                            placeholder="Oppgi Addresse"
                            required>
                    </div>
                </div>

                <div class="mb-3 row">
                    <!-- Input form for areal (BTA) -->
                    <div class="col-md-6 col-sm-4">
                    <label for="prosjektbta-input" class="form-label">Bruttoareal (BTA)</label>
                    <input 
                        type="number" 
                        class="form-control" 
                        id="prosjektbta-input" 
                        v-model="newProject.bta" 
                        placeholder="Oppgi BTA"
                        min="1"
                        required>
                    </div>
                    <!-- Dropdown menu for selecting bygningskategori -->
                    <div class="col-md-6">
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
                    <div class="col-md-6">
                    <label for="prosjektstart-input" class="form-label">Prosjektstart (år)</label>
                    <input 
                        type="text" 
                        class="form-control" 
                        id="prosjektstart-input" 
                        v-model="newProject.prosjektstart" 
                        min="2000"
                        required>
                    </div>
                    <!-- Input form for Analyseperiode -->
                    <div class="col-md-6 col-sm-4">
                    <label for="analyseperiode-input" class="form-label">Analyseperiode (år)</label>
                    <input 
                        type="number" 
                        class="form-control" 
                        id="analyseperiode-input" 
                        v-model="newProject.analyseperiode" 
                        min="1"
                        required>
                    </div>
                </div>
                
                <div class="btn-group" role="group">
                    <button type="submit" class="btn btn-primary btn-sm">Legg til</button>
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
    import { klimagassreferanser } from '../utils/breeam.js'
    import { getTodaysDate } from '../utils/misc.js'

    export default {
        name: 'ProjectModal',
        props: {
            isActive: Boolean,
        },       
        data() {
            return {
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
            closeModal() {
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
