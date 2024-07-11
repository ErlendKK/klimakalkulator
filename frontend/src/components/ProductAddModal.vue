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
          <template v-if="newProduct.product?.EPD_URL">
            <a :href="newProduct.product.EPD_URL" target="_blank" rel="noopener noreferrer"><i class="bi bi-link epd-link"></i></a>
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
        <button type="submit" class="btn btn-primary btn-md" style="min-width:8em">Legg til</button>
      </div>
    </form>
  </ModalComponent>
</template>

<script setup lang="ts">
  import ModalComponent from './ModalComponent.vue';
  import { bygningsdeler } from '../utils/breeam.js'
  import { setDisplayedName } from '../utils/misc'
  import { initializeProduct } from '../utils/initializers'
  import { getData } from '../utils/http-requests'
  import { displayErrorToast, displayWarningToast } from '../utils/toasts'
  import { computed, onMounted, ref } from 'vue';
  import { ServerResponse, Product, EmissionFactor, EmissionDataResponse } from '../interfaces/interfaces'

  const props = defineProps<{ isActive: Boolean }>();
  const emit = defineEmits(['close', 'submit-product']);
    
  const title = "Legg til nytt produkt"
  const materialTyper = ref(['Alle']);
  const searchQuery = ref('');
  const ecoPortalData = ref<any[]>([]);
  const ecoPortalStatus = ref('idle');
  const selectedProductStatus = ref('No product selected');

  const bygningsdelsNavn = computed(() => {
    return bygningsdeler.map(item => `${item.bygningsdel} (${item.nummer})`);
  });

  // TODO: Check if newProduct needs to be ref()
  let newProduct = ref<Product>(initializeProduct());
 
  const produktgrupper = computed(() => {
    if (!newProduct.value.bygningsdel) return [];

    // Select bygningsdel based on name + number
    const valgtBygningsdel = bygningsdeler.find(item => {
      return `${item.bygningsdel} (${item.nummer})`.toLowerCase() === newProduct.value.bygningsdel.toLowerCase();
    });

    // If valgtBygningsdel is undefined, something has gone wrong
    if (!valgtBygningsdel) {
      console.error(`valgtBygningsdel was not found for newProduct.bygningsdel: ${newProduct.value.bygningsdel}`);
      return [];
    }

    const produktGrupper = valgtBygningsdel.produktgrupper.map(item => `${item.gruppe} (${item.nummer})`);
    return produktGrupper;
  })

  function displayUnit(): boolean {
    return selectedProductStatus.value === 'success' && !!newProduct.value.unit;
  }

  const filteredProducts = computed((): object[] => {
    if (newProduct.value.type && newProduct.value.type !== "Alle" && ecoPortalData.value.length) {
      const filteredProds = ecoPortalData.value.filter(product => 
        product.classific === newProduct.value.type
      );
      return filteredProds;
    }
    return ecoPortalData.value; 
  })
      
  onMounted(() => {
  if (ecoPortalStatus.value !== 'success') {
    fetchFullProductList();
  }
});


// fetch list of product to be displayed in product dropdown
async function fetchFullProductList(): Promise<void> {
  if (ecoPortalStatus.value === 'loading') return;

  ecoPortalStatus.value = 'loading';
  const db_response: ServerResponse = await getData('/products/list');
  
  if (db_response.status === 'failed') {
    ecoPortalStatus.value = 'failed';
    displayWarningToast('En feil oppstod ved lasting av produktdata');
    return;
  }

  // Limit name length to avoid overflow. Fill the list materialTyper
  const productList = db_response.data as Product[];
  const classifics = new Set<string>();

  productList.forEach(product => {
    classifics.add(product.classific);
    product.displayedName = setDisplayedName(product, 45);
  });

  materialTyper.value = ['Alle', ...Array.from(classifics)];
  ecoPortalStatus.value = 'success';
  ecoPortalData.value = productList;
}

function handleClose(): void  {
  emit('close');
  setTimeout(() => newProduct.value = initializeProduct(), 1000);
}

// send event to parent component and reset newProduct.
function handleSubmit(): void  {
  emit('submit-product', newProduct.value);
  setTimeout(() => newProduct.value = initializeProduct(), 1000);
}


// fetch properties for the selected product, incl. emission factors
async function fetchEmissionData(selectedProduct: Product): Promise<void> {
  selectedProductStatus.value = 'loading data..';
  const uuid = selectedProduct.uuid;
  const db_response: ServerResponse = await getData(`/products/emission-data/${uuid}`);

  if (db_response.status === 'failed') {
    selectedProductStatus.value = 'failed to load data';
    displayErrorToast('Det oppstod en feil ved lastingen av utlsippsdata');
    return;
  }

  console.log('data.name: ' + selectedProduct.name + '\n' + selectedProduct);
  selectedProductStatus.value = 'success';
  newProduct.value.product = selectedProduct;
  newProduct.value.displayedName = setDisplayedName(selectedProduct, 45);
  
  const productData = db_response.data as EmissionDataResponse;
  newProduct.value.emission_factors = {...productData.emission_factors};
  newProduct.value.unit = productData.unit as string;
  console.log(newProduct.value);
}
</script>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ProductAddModal',
});
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