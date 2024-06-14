<template>
  <ModalComponent :isActive="isActive" :title="title" @close="handleClose">
    <form @submit.prevent="handleSubmit">
      
      <div class="mb-3 row">
        <!-- Dropdown menu for selecting bygningsdel -->
        <div class="col-sm-6">
          <label for="bygningsdel-update-dropdown" class="form-label">Bygningsdel</label>
          <select id="bygningsdel-update-dropdown" class="form-control" 
            v-model="newProduct.bygningsdel" required 
            v-if="ecoPortalStatus === 'success' && filteredProducts.length">
            <option disabled value="">Velg bygningsdel</option>
            <option v-for="bygningsdel in bygningsdelsNavn" :key="bygningsdel.bygningsdel" :value="bygningsdel">
              {{ bygningsdel }}
            </option>
          </select>
          <div v-else>
            <button class="btn btn-block loading-spinner" type="button" disabled>
              <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              Laster...
            </button>
          </div>
        </div>

        <!-- Dropdown menu for selecting produktgruppe -->
        <div class="col-sm-6">
          <label for="produktgruppe-update-dropdown" class="form-label">Produktgruppe</label>
          <template v-if="newProduct.bygningsdel !== ''">
            <select id="produktgruppe-update-dropdown" class="form-control" 
              v-model="newProduct.produktgruppe" required>
              <option disabled value="">Velg produktGruppe</option>
              <option 
                v-for="produktgruppe in produktgrupper" 
                :key="produktgruppe" 
                :value="produktgruppe">
                {{ produktgruppe }}
              </option>
            </select>
          </template>
          <div v-else>
            <button class="btn btn-block loading-spinner" type="button" disabled>
              <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              Laster...
            </button>
          </div>
        </div>
      </div>

      <div class="mb-3 row">
        <!-- Dropdown menu for selecting product type -->
        <div class="col-sm-6">
          <label for="materialtypevalg-update-dropdown" class="form-label">Material</label>
          <select id="materialtypevalg-update-dropdown" class="form-control" 
              v-model="newProduct.type" required 
              v-if="ecoPortalStatus === 'success' && filteredProducts.length">
              <option disabled value="">Velg Materialtype</option>
              <option v-for="materialtype in materialTyper" :key="materialtype" :value="materialtype">
                {{ materialtype }}
              </option>
          </select>
          <div v-else>
            <button class="btn btn-block loading-spinner" type="button" disabled>
              <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              Laster...
            </button>
          </div>
        </div>
        
        <!-- Dropdown menu for selecting product -->
        <div class="col-sm-6" 
          v-if="ecoPortalStatus === 'success' && filteredProducts.length">
          <label for="produktvalg-update-dropdown" class="form-label">Produkt</label>
          <template v-if="newProduct.epd_url">
            <a :href="newProduct.epd_url" target="_blank" rel="noopener noreferrer"><i class="bi bi-link epd-link"></i></a>
          </template>
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
              v-for="entry in filteredProducts" 
              :key="entry.uuid"
              :value="entry">
              {{ entry.displayedName }}
            </option>
          </select>
        </div>
        <div class="col-sm-6" v-else>
          <label for="produktvalg-update-placeholder" class="form-label">Produkt</label>
          <button class="btn btn-block loading-spinner" type="button" disabled>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Laster...
          </button>
        </div>
      </div>

      <div class="mb-3 row">
        <!-- Input form for amount of the product-->
        <div class="col-sm-6" v-if="ecoPortalStatus === 'success' && filteredProducts.length">
          <label for="produktmengde-update-input" class="form-label">Mengde</label>
          <input type="number" class="form-control" id="produktmengde-update-input" 
            v-model="newProduct.quantity"
            required>
        </div>
        <div class="col-sm-6" v-else>
          <label for="mengde-loading-placeholder" class="form-label">Mengde</label>
          <button class="btn btn-block loading-spinner" type="button" disabled>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Laster...
          </button>
        </div>

        <!-- Displays the unit -->
        <div class="col-sm-6"
          v-if="ecoPortalStatus === 'success' && filteredProducts.length">
          <label for="enhet-update-dropdown" class="form-label">Enhet</label>
          <select id="enhet-update-dropdown" class="form-control" v-model="newProduct.unit" required readonly>
            <option disabled>{{ newProduct.unit }}</option>
          </select> 
        </div>
        <div class="col-sm-6"
          v-else>
          <label for="enhet-update-placeholder" class="form-label">Enhet</label>
          <button class="btn btn-block loading-spinner" type="button" disabled>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Laster...
          </button>
        </div>
      </div>

      <div class="mb-3 row">
        <!-- Input form for utskiftingsintervall -->
        <div class="col-sm-6" v-if="ecoPortalStatus === 'success' && filteredProducts.length">
          <label for="utskiftingsintervall-update-input" class="form-label">Utskiftingsintervall</label>
          <input type="number" class="form-control" id="utskiftingsintervall-update-input" 
            v-model="newProduct.utskiftingsintervall" 
            placeholder="50"
            required>
        </div>
        <div class="col-sm-6" v-else>
          <label for="utskiftingsintervall-loading-placeholder" class="form-label">Utskiftingsintervall</label>
          <button class="btn btn-block loading-spinner" type="button" disabled>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Laster...
          </button>
        </div>

        <!-- Input form for vedlikeholdsutslipp -->
        <div class="col-sm-6" v-if="ecoPortalStatus === 'success' && filteredProducts.length">
          <label for="vedlikeholdsutslipp-update-input" class="form-label">Årlige Vedlikeholdsutslipp</label>
          <input type="number" class="form-control" id="vedlikeholdsutslipp-update-input" 
            v-model="newProduct.vedlikeholdsutslipp" 
            placeholder="0"
            required>
        </div>
        <div class="col-sm-6" v-else>
          <label for="vedlikeholdsutslipp-loading-placeholder" class="form-label">Årlige Vedlikeholdsutslipp</label>
          <button class="btn btn-block loading-spinner" type="button" disabled>
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Laster...
          </button>
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
  import ModalComponent from '../components/ModalComponent.vue';
  import { bygningsdeler } from '../utils/breeam.js';
  import { setDisplayedName } from '../utils/misc.js'
  import { getData } from '../utils/http-requests.js';
  import { useAuthStore } from '../stores/authStore';
  import { displayErrorToast } from '../utils/toasts.js'
  import cloneDeep from 'lodash/cloneDeep';
    
  export default {
    name: 'ProductUpdateModal',
    setup() {
      const authStore = useAuthStore();
      const currentProjectId = authStore.currentProject.project_id;

      return { currentProjectId };
    },
    props: {
      isActive: Boolean, // Used to display/ hide the modal
      productToBeUpdated: Object,
    },
    components: {
      ModalComponent
    },
    data() {
      return {
        title: "Oppdater produktet",
        bygningsdelsNavn: bygningsdeler.map(del => `${del.bygningsdel} (${del.nummer})`),
        bygningsdeler: bygningsdeler,
        materialTyper: ["Alle"],
        newProduct: { 
          product: {}, 
          displayedName: '',
          bygningsdel: '' 
        },
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
        if (!this.newProduct.bygningsdel) return [];

        const valgtBygningsdel = bygningsdeler.find(del => 
        `${del.bygningsdel} (${del.nummer})`.toLowerCase() === this.newProduct.bygningsdel.toLowerCase()
        );

        const produktGrupper = valgtBygningsdel.produktgrupper.map(del => `${del.gruppe} (${del.nummer})`);
        return produktGrupper;
      },
      filteredProducts() {
        if (this.newProduct.type && this.newProduct.type !== "Alle" && this.productsForSelection.length) {
          const filteredList = this.productsForSelection.filter(product => 
            product.classific === this.newProduct.type
          );
          return filteredList
        }
        return this.ecoPortalData; 
      }
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
        const db_response = await getData('/products/list');
        
        if (db_response.status === 'failed') {
          this.ecoPortalStatus = 'failed';
          displayErrorToast('En feil oppstod ved lasting av produktdata')
          return;
        }

        // Limit name length to avoid overflow. Fill the list materialTyper
        const productList = db_response.data;
        const classifics = new Set()
        productList.forEach(product => {
          classifics.add(product.classific)
          product.displayedName = setDisplayedName(product, 45);
          product['project_id'] = this.currentProjectId;
        });

        this.materialTyper = ['Alle', ...classifics];
        this.ecoPortalData = productList;
        console.log(this.ecoPortalData)
        this.ecoPortalStatus = 'success';
      },
      initializeProductOptions() {
        this.newProduct = cloneDeep(this.productToBeUpdated);
        this.newProduct.displayedName = setDisplayedName(this.newProduct, 45);
        this.newProduct.product = {...this.newProduct};
        console.log(this.newProduct)
        this.productsForSelection = this.ecoPortalData.filter(product => product.uuid !== this.newProduct.uuid);
      },
      handleClose() {
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
          displayErrorToast('En feil oppstod ved lasting av utslippsfaktorer')
          return;
        }

        console.log('data.name: ' + product.name, product);
        product.displayedName = setDisplayedName(product, 30);
        product.emission_factors = emissionData.emission_factors;
        product.unit = emissionData.unit;
        this.newProduct = Object.assign(this.newProduct, product);
        this.selectedProductStatus = 'success';
        console.log(this.newProduct)
      }
    }
  }
</script>

<style scoped>
  .loading-spinner {
    width: 100%;
  }
  .epd-link {
    margin-left: 0.5em;
  }
</style>
