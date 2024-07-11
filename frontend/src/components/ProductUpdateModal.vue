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
          <template v-if="newProduct.EPD_URL">
            <a :href="newProduct.EPD_URL" target="_blank" rel="noopener noreferrer"><i class="bi bi-link epd-link"></i></a>
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
        <button type="submit" class="btn btn-primary btn-md" style="min-width:8em">Oppdater</button>
      </div>
    </form>
  </ModalComponent>
</template>

    
<script setup lang="ts">
  import ModalComponent from '../components/ModalComponent.vue';
  import { bygningsdeler } from '../utils/breeam.js';
  import { setDisplayedName } from '../utils/misc'
  import { initializeProduct } from '../utils/initializers'
  import { getData } from '../utils/http-requests';
  import { displayErrorToast } from '../utils/toasts'
  import { useAuthStore } from '../stores/authStore';
  import cloneDeep from 'lodash/cloneDeep';
  import { computed, onMounted, ref } from 'vue';
  import { ServerResponse, Product, EmissionDataResponse } from '../interfaces/interfaces'

  const authStore = useAuthStore();
  const emit = defineEmits(['close', 'submit-product']);
  const currentProjectId = authStore.currentProject.project_id;
  const title = "Oppdater produktet"

  const props = defineProps<{ 
    isActive: Boolean,
    productToBeUpdated: Product,
  }>();

  const bygningsdelsNavn = computed(() => {
    return bygningsdeler.map(item => `${item.bygningsdel} (${item.nummer})`);
  });

  const bygningsdelerRef = ref(bygningsdeler);
  let materialTyper = ref(["Alle"]);

  let newProduct = ref<Product>(initializeProduct());

  const ecoPortalData = ref<any[]>([]);
  const productsForSelection = ref<Product[]>([]);
  const ecoPortalStatus = ref('idle');
  const selectedProduct = ref<Product | null>(null);
  let selectedProductStatus = ref('No product selected');
  const selectedProductData = ref<any>({});

  const produktgrupper = computed(() => {
  if (!newProduct.value.bygningsdel) return [];

  const valgtBygningsdel = bygningsdeler.find(del => 
    `${del.bygningsdel} (${del.nummer})`.toLowerCase() === newProduct.value.bygningsdel.toLowerCase()
  );

  if (!valgtBygningsdel) return [];

  return valgtBygningsdel.produktgrupper.map(del => `${del.gruppe} (${del.nummer})`);
});

const filteredProducts = computed(() => {
  if (newProduct.value.type && newProduct.value.type !== "Alle" && productsForSelection.value.length) {
    return productsForSelection.value.filter(product => 
      product.classific === newProduct.value.type
    );
  }
  return ecoPortalData.value; 
});

onMounted(async () => {
  // Fetch data about material properties including emission factors
  if (ecoPortalStatus.value !== 'success') {
    await fetchFullProductList();
    initializeProductOptions();
  }
});

// fetch list of product to be displayed in product dropdown
async function fetchFullProductList(): Promise<void> {
  if (ecoPortalStatus.value === 'loading') return;

  ecoPortalStatus.value = 'loading';
  const db_response = await getData('/products/list');
  
  if (db_response.status === 'failed') {
    ecoPortalStatus.value = 'failed';
    displayErrorToast('En feil oppstod ved lasting av produktdata');
    return;
  }

  // Limit name length to avoid overflow. Fill the list materialTyper
  const productList = db_response.data as Product[];
  const classifics = new Set<string>();
  productList.forEach(product => {
    classifics.add(product.classific);
    product.displayedName = setDisplayedName(product, 45);
    product['project_id'] = currentProjectId;
  });

  materialTyper.value = ['Alle', ...Array.from(classifics)];
  ecoPortalData.value = productList;
  console.log(ecoPortalData);
  ecoPortalStatus.value = 'success';
}

function initializeProductOptions(): void {
  newProduct.value = cloneDeep(props.productToBeUpdated);
  newProduct.value.displayedName = setDisplayedName(newProduct.value, 45);
  newProduct.value.product = {...newProduct.value};
  console.log(newProduct.value)
  productsForSelection.value = ecoPortalData.value.filter(product => product.uuid !== newProduct.value.uuid);
}

function handleClose(): void {
  emit('close');
}

function handleSubmit(): void {
  newProduct.value.product_id = props.productToBeUpdated.product_id;
  emit('submit-product', newProduct.value);
}

// fetch properties for the selected product, incl. emission factors
async function fetchEmissionData(product) {
  console.log('fetchEmissionData: ', product)
  const uuid = product.uuid;
  const db_response = await getData(`/products/emission-data/${uuid}`);

  if (db_response.status === 'failed') {
    selectedProductStatus.value = 'failed to load data';
    displayErrorToast('En feil oppstod ved lasting av utslippsfaktorer')
    return;
  }

  console.log('data.name: ' + product.name, product);
  product.displayedName = setDisplayedName(product, 30);

  const productData = db_response.data as EmissionDataResponse;
  product.emission_factors = productData.emission_factors;
  product.unit = productData.unit;
  newProduct.value = Object.assign(newProduct.value, product);
  selectedProductStatus.value = 'success';
  console.log(newProduct.value)
}
</script>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ProductUpdateModal',
});
</script>

<style scoped>
  .loading-spinner {
    width: 100%;
  }
  .epd-link {
    margin-left: 0.5em;
  }
</style>
