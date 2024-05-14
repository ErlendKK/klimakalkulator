<template>
  <div>
    <div ref="ProductModal" class="modal fade" :class="{ show: isActive, 'd-block': isActive }" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Oppdater produktet</h5>
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
                  <!-- Dropdown menu for selecting bygningsdel -->
                  <div class="col-md-6 ">
                      <label for="bygningsdel-update-dropdown" class="form-label">Bygningsdel</label>
                      <select id="bygningsdel-update-dropdown" class="form-control" 
                        v-model="newProduct.bygningsdel" required>
                        <option disabled value="">Velg bygningsdel</option>
                        <option 
                          v-for="bygningsdel in bygningsdelsNavn" 
                          :key="bygningsdel.bygningsdel" 
                          :value="bygningsdel">
                          {{ bygningsdel }}
                        </option>
                      </select>
                  </div>

                  <!-- Dropdown menu for selecting produkttype -->
                  <div class="col-md-6">
                      <label for="produktgruppe-update-dropdown" class="form-label">Produktgruppe</label>
                      <select id="produktgruppe-update-dropdown" class="form-control" 
                        v-model="newProduct.produktgruppe" 
                        ref="produktgruppeDropdown" 
                        required>
                        <template v-if="newProduct.Bygningsdel !== ''">
                          <option disabled value="">Velg produktGruppe</option>
                          <option 
                            v-for="produktgruppe in produktgrupper" 
                            :key="produktgruppe" 
                            :value="produktgruppe">
                            {{ produktgruppe }}
                          </option>
                        </template>
                        <template v-else>
                          <option disabled value=""></option>
                        </template>    
                      </select>
                  </div>
              </div>

              <!-- Input form for produktnavn -->
              <!-- If ecoPortalData has been fetched; display productnames as options  -->
              <div class="mb-3 row">
                <div class="col-md-6" 
                  v-if="ecoPortalStatus === 'success' && productsForSelection.length">
                  <label for="produktvalg-update-dropdown" class="form-label">Produkt</label>
                  <select id="produktvalg-update-dropdown" class="form-control" 
                    v-model="newProduct.product" 
                    @change="fetchEmissionData(newProduct.product)" 
                    required>
                    <option 
                      :value="newProduct.product"
                      selected>
                      {{ newProduct.displayedName }}
                    </option>
                    <option 
                      v-for="entry in productsForSelection" 
                      :key="entry.uuid"
                      :value="entry">
                      {{ entry.displayedName }}
                    </option>
                  </select>
                </div>
                  <!-- Else; display placeholder -->
                <div class="col-md-6" v-else>
                  <label for="produktvalg-update-placeholder" class="form-label">Produkt</label>
                  <select id="produktvalg-update-placeholder" class="form-control">
                    <option value="" disabled selected>Laster Produktdata...</option>
                  </select>
                </div>

                <!-- Input form for materialtype -->
                <div class="col-md-6">
                  <label for="materialtypevalg-update-dropdown" class="form-label">Material</label>
                    <select id="materialtypevalg-update-dropdown" class="form-control" 
                      v-model="newProduct.type" 
                      required>
                      <option disabled value="">Velg Materialtype</option>
                      <option 
                        v-for="materialtype in materialTyper" 
                        :key="materialtype" 
                        :value="materialtype">
                        {{ materialtype }}
                      </option>
                    </select>
                  </div>
              </div>

              <div class="mb-3 row">
                <!-- Mengde Input -->
                <div class="col-sm-6">
                <label for="produktmengde-update-input" class="form-label">Mengde</label>
                <input type="number" class="form-control" id="produktmengde-update-input" 
                    v-model="newProduct.quantity"
                    required>
                </div>

                <!-- Dropdown menu for selecting unit -->
                <!-- If selectedProduct has been defined; display unit  -->
                <div class="col-sm-6"
                  v-if="ecoPortalStatus === 'success' && productsForSelection.length">
                    <label for="enhet-update-dropdown" class="form-label">Enhet</label>
                <td readonly>{{ product.unit }}</td>
                    <select id="enhet-update-dropdown" class="form-control" v-model="newProduct.unit" required readonly>
                      <option>{{ newProduct.unit }}</option>
                    </select> 
                  </div>
                <!-- Else; display placeholder -->
                <div class="col-sm-6"
                  v-else>
                  <label for="enhet-update-placeholder" class="form-label">Enhet</label>
                  <select id="enhet-update-placeholder" class="form-control">
                    <option value="" disabled selected>Laster Produktdata...</option>
                  </select> 
                </div>
              </div>

              <div class="mb-3 row">
                    <!-- Input form for utskiftingsintervall -->
                    <div class="col-md-6">
                        <label for="utskiftingsintervall-update-input" class="form-label">Utskiftingsintervall</label>
                        <input 
                            type="number" 
                            class="form-control" 
                            id="utskiftingsintervall-update-input" 
                            v-model="newProduct.utskiftingsintervall" 
                            placeholder="50"
                            required>
                    </div>
                     <!-- Input form for vedlikeholdsutslipp -->
                    <div class="col-md-6">
                        <label for="vedlikeholdsutslipp-update-input" class="form-label">Årlige Vedlikeholdsutslipp</label>
                        <input 
                            type="number" 
                            class="form-control" 
                            id="vedlikeholdsutslipp-update-input" 
                            v-model="newProduct.vedlikeholdsutslipp" 
                            placeholder="0"
                            required>
                    </div>
                </div>
             
              <div class="btn-group" role="group">
                <button type="submit" class="btn btn-primary btn-sm">Oppdater</button>
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
    import { bygningsdeler } from '../utils/breeam.js';
    import { setDisplayedName } from '../utils/misc.js'
    import { getData } from '../utils/http-requests.js';
    import { useAuthStore } from '../stores/authStore';
    import Dropdown from 'primevue/dropdown';
    import { useToast } from "vue-toastification";

    
    export default {
      name: 'ProductUpdateModal',
      setup() {
        const authStore = useAuthStore();
        const currentProjectId = authStore.currentProject.project_id;
        const toast = useToast();

        function displaySuccessToast(message="Suksess!") {
          toast.success(message);
        }

        function displayErrorToast(message="Error!") {
          toast.error(message);
        }

        function displayWarningToast(message="Obs!") {
          toast.warning(message);
        }

        return { currentProjectId, displaySuccessToast, displayErrorToast, displayWarningToast };
      },
      props: {
        isActive: Boolean, // Used to display/ hide the modal
        productToBeUpdated: Object,
      },
      components: {
        Dropdown
      },

      data() {
        return {
            bygningsdelsNavn: bygningsdeler.map(del => `${del.bygningsdel} (${del.nummer})`),
            bygningsdeler: bygningsdeler,
            materialTyper: [
                'Alle', 'Gips', 'Betong', 'Tre', 'Isolasjon', 'Membran', 'Stål', 'Aluminium',
                'Glass', 'Keramiske fliser', 'Granitt', 'PVC', 'Vinyl', 'Betongstein',
                'Asfalt', 'Akryl', 'Kobber', 'Sink', 'Leca', 'Kalksandstein', 'Annet'
            ],
            newProduct: { product: {}, displayedName: '' },
            ecoPortalData: [],
            productsForSelection: [],
            ecoPortalStatus: 'idle',
            selectedProduct: null,
            selectedProductStatus: 'No product selected',
            selectedProductData: {},
        }
      },

      computed: {
        produktgrupper() {
           if (!this.newProduct.bygningsdel) {
            return [];
           }

           const valgtBygningsdel = bygningsdeler.find(del => `${del.bygningsdel} (${del.nummer})`.toLowerCase() === this.newProduct.bygningsdel.toLowerCase());
           const produktGrupper = valgtBygningsdel.produktgrupper.map(del => `${del.gruppe} (${del.nummer})`);
           return produktGrupper;
        },
      },

      async mounted() {
        // fetch data about material properties inlc. emission factors
        if (this.ecoPortalStatus !== 'success') {
          await this.fetchFullProductList();
          this.initializeProductOptions();
        }
      },

      methods: {
        // fetch list of product to be displayed in product dropdown
        async fetchFullProductList() {
          if (this.ecoPortalStatus === 'loading') return;

          this.ecoPortalStatus = 'loading';
          const productList = await getData('/products/full-productlist');
          
          if (productList.status === 'failed') {
            this.ecoPortalStatus = 'failed';
            this.displayErrorToast('En feil oppstod ved lasting av produktdata')
            return;
          }

          productList.forEach(product => {
            product.displayedName = setDisplayedName(product, 45);
            product['project_id'] = this.currentProjectId;
          });
          this.ecoPortalData = productList;
          this.ecoPortalStatus = 'success';
        },
        initializeProductOptions() {
          this.productToBeUpdated.displayedName = setDisplayedName(this.productToBeUpdated, 45);
          this.newProduct = this.productToBeUpdated;
          this.newProduct.product = {...this.productToBeUpdated};
          this.productsForSelection = this.ecoPortalData.filter(product => product.uuid !== this.newProduct.uuid);
        },
        closeModal() {
          this.$emit('close');
        },
        // send event to parent component and reset newProduct for the next time Modal is opened.
        handleSubmit() {
          this.newProduct.product_id = this.productToBeUpdated.product_id;
          this.$emit('submit-product', this.newProduct);
        },

        // fetch properties for the selected product, incl. emission factors
        async fetchEmissionData(product) {
          console.log('fetchEmissionData: ', product)
          const uuid = product.uuid;
          console.log(uuid)
          const emissionData = await getData(`/products/emission-data/${uuid}`);

          if (emissionData.status === 'failed') {
            this.selectedProductStatus = 'failed to load data';
            this.displayErrorToast('En feil oppstod ved lasting av utslippsfaktorer')
            return;
          }

          console.log('data.name: ' + product.name, product);
          product.displayedName = setDisplayedName(product, 30);
          product.emission_factors = emissionData.emission_factors;
          product.unit = emissionData.unit;
          this.newProduct = product;
          this.selectedProductStatus = 'success';
        }
    }
  }
</script>
