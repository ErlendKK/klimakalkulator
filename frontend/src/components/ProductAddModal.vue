<template>
  <ModalComponent :isActive="isActive" :title="title" @close="handleClose">
    <form @submit.prevent="handleSubmit">

      <div class="mb-3 row">
        <!-- Dropdown menu for selecting bygningsdel -->
        <div class="col-sm-6 ">
          <label for="bygningsdel-dropdown" class="form-label">Bygningsdel</label>
          <select id="bygningsdel-dropdown" class="form-control" v-model="newProduct.bygningsdel" required>
            <option disabled class="dropdown-header" value="">Velg bygningsdel</option>
            <option 
              v-for="bygningsdel in bygningsdelsNavn" 
              :key="bygningsdel.bygningsdel" 
              :value="bygningsdel">
              {{ bygningsdel }}
            </option>
          </select>
        </div>

        <!-- Dropdown menu for selecting produktgruppe -->
        <div class="col-sm-6">
          <label for="produktgruppe-dropdown" class="form-label">Produktgruppe</label>
          <select id="produktgruppe-dropdown" class="form-control" v-model="newProduct.produktgruppe" ref="produktgruppeDropdown" required>
            <template v-if="newProduct.Bygningsdel !== ''">
              <option disabled class="dropdown-header" value="">Velg Produktgruppe</option>
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

      <div class="mb-3 row">
        <!-- Dropdown menu for selecting product type -->
        <div class="col-sm-6">
          <label for="materialtypevalg-dropdown" class="form-label ">Produkttype</label>
          <select id="materialtypevalg-dropdown" class="form-control" v-model="newProduct.type" required>
            <template v-if="ecoPortalStatus === 'success' && ecoPortalData.length">
              <option disabled value="">Velg Produkttype</option>
              <option v-for="materialtype in materialTyper" :key="materialtype" :value="materialtype">
                {{ materialtype }}
              </option>
            </template>
            <template v-else>
              <option  disabled>Laster Produktdata...</option>
            </template>
          </select>
        </div>

        <!-- Dropdown menu for selecting product -->
        <div class="col-sm-6">         
          <label for="produktvalg-dropdown" class="form-label">Produkt</label>
          <template v-if="newProduct.product.epd_url">
            <a :href="newProduct.product.epd_url" target="_blank" rel="noopener noreferrer"><i class="bi bi-link epd-link"></i></a>
          </template>
          <select id="produktvalg-dropdown dropdown-toggle dropdown-toggle-split" class="form-control" 
            v-model="newProduct.product" 
            @change="fetchEmissionData(newProduct.product)" 
            required>
            <template v-if="ecoPortalStatus === 'success' && ecoPortalData.length">
              <option disabled value="">Velg Produkt</option>
              <!-- Only display products that match the search query -->
              <option v-for="product in filteredProducts" :key="product.uuid" :value="product">
                {{ product.displayedName }}
              </option>
            </template>
            <template v-else>
              <option  disabled>Laster Produktdata...</option>
            </template>
          </select>
        </div>
      </div>

      <div class="mb-3 row">
        <!-- Input form for amount of the product-->
        <div class="col-sm-6">
          <label for="produktmengde-input" class="form-label">Mengde</label>
          <input 
            type="number" 
            class="form-control" 
            id="produktmengde-input" 
            v-model="newProduct.quantity"
            placeholder="Oppgi mengde"
            min="0.01" 
            step="any"
            required>
        </div>

        <!-- Displays the unit -->
        <div class="col-sm-6">
          <label for="enhet-dropdown" class="form-label">Enhet</label>
          <select id="enhet-dropdown" class="form-control" v-model="newProduct.unit" required>
            <template v-if="displayUnit">
              <option disabled>{{ newProduct.unit }}</option>
            </template>
            <template v-else>
              <option disabled value=""></option>
              <option disabled value="">{{ selectedProductStatus }}</option>
            </template>
          </select> 
        </div>
      </div>

      <div class="mb-3 row">
        <!-- Input form for utskiftingsintervall -->
        <div class="col-sm-6">
          <label for="utskiftingsintervall-input" class="form-label">Utskiftingsintervall</label>
          <input 
            type="number" 
            class="form-control" 
            id="utskiftingsintervall-input" 
            v-model="newProduct.utskiftingsintervall" 
            placeholder="50"
            required>
        </div>

          <!-- Input form for vedlikeholdsutslipp -->
        <div class="col-sm-6">
          <label for="vedlikeholdsutslipp-input" class="form-label">Årlige Vedlikeholdsutslipp</label>
          <input 
            type="number" 
            class="form-control" 
            id="vedlikeholdsutslipp-input" 
            v-model="newProduct.vedlikeholdsutslipp" 
            placeholder="0"
            required>
        </div>
      </div>
      
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary btn-md" style="min-width:5em" @click="handleClose">Avbryt</button>
        <button type="submit" class="btn btn-success btn-md" style="min-width:8em">Legg til</button>
      </div>
    </form>
  </ModalComponent>
</template>
    
<script>
  import ModalComponent from './ModalComponent.vue';
  import { bygningsdeler } from '../utils/breeam.js'
  import { setDisplayedName } from '../utils/misc.js'
  import { getData } from '../utils/http-requests.js'
  import { displayErrorToast, displayWarningToast } from '../utils/toasts.js'
    
  export default {
    name: 'ProductModal',
    components: {
      ModalComponent
    },
    props: {
      isActive: Boolean, // Used to display/ hide the modal
    },
    data() {
      return {
        title: "Legg til nytt produkt",
        bygningsdelsNavn: bygningsdeler.map(item => `${item.bygningsdel} (${item.nummer})`),
        bygningsdeler: bygningsdeler,
        materialTyper: ['Alle'],

        newProduct: {
          'bygningsdel': '',
          'produktgruppe': '',
          'name': '',
          'displayedName': '',
          'type': '',
          "product": '',
          "utskiftingsintervall": 50,
          "vedlikeholdsutslipp": 0,
          "quantity": 0,
          "unit": '',
        },
        
        searchQuery: '',
        ecoPortalData: [],
        ecoPortalStatus: 'idle',
        selectedProductStatus: 'No product selected',
      }
    },
    computed: {
      produktgrupper() {
        if (!this.newProduct.bygningsdel) {
        return [];
        }

        const valgtBygningsdel = bygningsdeler.find(item => `${item.bygningsdel} (${item.nummer})`.toLowerCase() === this.newProduct.bygningsdel.toLowerCase());
        const produktGrupper = valgtBygningsdel.produktgrupper.map(item => `${item.gruppe} (${item.nummer})`);
        return produktGrupper;
      },
      displayUnit() {
        return this.selectedProductStatus === 'success' && this.newProduct.unit;
      },
      filteredProducts() {
        if (this.newProduct.type && this.newProduct.type !== "Alle" && this.ecoPortalData.length) {
          const filteredProds = this.ecoPortalData.filter(product => 
            product.classific === this.newProduct.type
          );
          return filteredProds
        }
        return this.ecoPortalData; 
      }
      
    },
    mounted() {
      // fetch data about material properties inlc. emission factors
      if (this.ecoPortalStatus !== 'success') {
        this.fetchFullProductList();
      }

    },
    methods: {
      // fetch list of product to be displayed in product dropdown
      async fetchFullProductList() {
        if (this.ecoPortalStatus === 'loading') return;

        this.ecoPortalStatus !== 'loading';
        const db_response = await getData('/products/list');
        
        if (db_response.status === 'failed') {
          this.ecoPortalStatus = 'failed';
          displayWarningToast('En feil oppstod ved lasting av produktdata');
          return;
        }

        // Limit name length to avoid overflow. Fill the list materialTyper
        const productList = db_response.data
        const classifics = new Set()
        productList.forEach(product => {
          classifics.add(product.classific)
          product.displayedName = setDisplayedName(product, 45)
        });

        this.materialTyper = ['Alle', ...classifics];
        this.ecoPortalStatus = 'success';
        this.ecoPortalData = productList;
      },
      handleClose() {
        this.$emit('close');
        this.resetNewProduct();
      },
      resetNewProduct() {
        this.newProduct = {
          'bygningsdel': '',
          'produktgruppe': '',
          'name': '',
          'displayedName': '',
          'type': '',
          "product": '',
          "utskiftingsintervall": 50,
          "vedlikeholdsutslipp": 0,
          "quantity": 0,
          "unit": '',
        };
      },

      // send event to parent component and reset newProduct.
      handleSubmit() {
        this.$emit('submit-product', this.newProduct);
        this.resetNewProduct();
      },

      // fetch properties for the selected product, incl. emission factors
      async fetchEmissionData(selectedProduct) {
        this.selectedProductStatus = 'loading data..';
        const uuid = selectedProduct.uuid;
        const emissionData = await getData(`/products/emission-data/${uuid}`);

        if (emissionData.status === 'failed') {
          this.selectedProductStatus = 'failed to load data';
          displayErrorToast('Det oppstod en feil ved lastingen av utlsippsdata');
          return;
        }

        console.log('data.name: ' + selectedProduct.name + '\n' + selectedProduct)
        this.selectedProductStatus = 'success';
        this.newProduct.product = selectedProduct;

        this.newProduct.displayedName = setDisplayedName(selectedProduct, 45);
        this.newProduct.emission_factors = {...emissionData.emission_factors};
        this.newProduct.unit = emissionData.unit;
        console.log(this.newProduct)
      }
    }
  }
</script>

<style scoped>
  .custom-dropdown {
    height: auto;
    max-height: 300px;
    overflow-x: hidden;
  }
  .product-select-container {
    display: flex;
    flex-direction: column;
  }
  .modal-btn {
    width: 5em;
    min-width: 20px;
  }
  .epd-link {
    margin-left: 0.5em;
  }
</style>