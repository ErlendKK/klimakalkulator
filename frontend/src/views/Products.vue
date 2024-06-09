<template>
  <div class="layout">
    <Nav-header></Nav-header>
    
    <main class="container">
      <h2>{{ heading }}</h2>
      <div class="card mb-3">
        <div class="card-body">
          <div v-if="isLoggedInComputed && currentProject">

            <!-- Open productModal to add new product to the project -->
            <button type="button" class="btn btn-success toggle-modal-button"
              @click="toggleAddModal">
              Nytt Produkt
            </button>
            <product-add-modal
              :is-active="isAddModalActive"
              @close="isAddModalActive = false"
              @submit-product="handleAddModalSubmit">
            </product-add-modal>

            <!-- Open productUpdateModal to add new product to the project -->
            <Product-update-modal
              v-if="isUpdateModalActive"
              :is-active="isUpdateModalActive"
              :productToBeUpdated="productToBeUpdated"
              @close="isUpdateModalActive = false"
              @submit-product="handleUpdateModalSubmit">
            </Product-update-modal>
  
            <!-- Table of products included in the project -->
            <div class="table-responsive-md">
              <table class="table table-sm table-hover" >
                <thead class="table-light">
                  <tr>
                    <!-- For sortable columns display sort-icon and listen for click -->
                    <th v-for="entry in tableEntries" :key="entry">
                      <template  v-if="entry.sortable">
                        <button type="button" class="btn btn-default heading text-start text-nowrap"
                          @click="sortTable(entry)">
                          {{ entry.heading }}
                          <i
                            :class="{
                              'fa-solid': true, 
                              'fa-sort': entry.body !== currentSort, 
                              'fa-sort-down': entry.body === currentSort && sortAscending, 
                              'fa-sort-up': entry.body === currentSort && !sortAscending,
                              'faded-icon': true 
                            }">
                          </i>
                        </button>
                      </template>
                      <template  v-else>
                        <button type="button" disabled class="btn btn-default border border-0 heading" style="padding-left: 0; font-weight: bold;">
                        {{ entry.heading }}
                        </button>
                      </template>
                    </th>
                    <!-- Empty heading for dropdown-menus -->
                    <th></th> 
                  </tr>
                </thead>
                <tbody>
                  <tr 
                    v-for="(product, index) in sortedProducts" 
                    :key="index">
                    <td>{{ product.bygningsdel }}</td>
                    <td>{{ product.produktgruppe }}</td>
                    <td>{{ product.displayedName }}</td>
                    <td>{{ product.type }}</td>
                    <td>{{ product.quantity }}</td>
                    <td readonly>{{ product.unit }}</td>

                    <!-- Dropdown menu for product-rows -->
                    <td>
                      <div class="dropdown"> 
                        <a class="btn ellipsis-container" href="#" role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
                          <i class="fa-solid fa-ellipsis"></i>
                        </a>
                        <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                          <li><a class="dropdown-item" href="#" @click="editButtonHandler(product)">Rediger</a></li>
                          <li><a class="dropdown-item" href="#" @click="copyButtonHandler(product)">Lag kopi</a></li>
                          <div class="dropdown-divider"></div>
                          <li><a class="dropdown-item" href="#" @click="deleteButtonHandler(product)">Slett</a></li>
                        </ul>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
              <p class="placeholder-glow if-copying-active" v-if="isCopyInProgress">
                <span class="placeholder col-12 if-copying-active"></span>
              </p>
            </div>
          </div>
          <div v-else-if="userComputed === null">
            <p>Logg inn for å se produkter</p>
          </div>
          <div v-else>
            <p><router-link to="/projects">Velg et prosjekt</router-link></p>
          </div>
        </div>
      </div>
    </main>
      
    <nav-footer />
  </div>
</template>
    
<script>
  import NavHeader from '../components/NavHeader.vue';
  import NavFooter from '../components/NavFooter.vue';
  import ProductAddModal from '../components/ProductAddModal.vue';
  import ProductUpdateModal from '../components/ProductUpdateModal.vue';
  import cloneDeep from 'lodash/cloneDeep';
  import { postData, deleteData, updateData } from '../utils/http-requests.js'
  import { displaySuccessToast, displayErrorToast } from '../utils/toasts.js'
  import { saveToLocalStorage, getFromLocalStorage } from '../utils/local-storage.js'
  import { setDisplayedName, sortByField } from '../utils/misc.js'
  import { useAuthStore } from '../stores/authStore';
  import { computed } from 'vue';

  export default {
      name: 'Products',
      components: {
        NavHeader,
        NavFooter,
        ProductAddModal,
        ProductUpdateModal
      },

      setup() {
        /**
         * Handle Global state
         */
        const authStore = useAuthStore();

        const isLoggedInComputed = computed(() => authStore.isLoggedIn);
        const userComputed = computed(() => authStore.user);
        const currentProject = computed(() => authStore.currentProject);
        const productList = computed(() => currentProject.value?.products ?? []);
        const pushToProducts = authStore.pushToProducts;
        const popFromProducts = authStore.popFromProducts;

        const heading = computed(() => {
          const project = currentProject.value;
          return project ? `Produktoversikt: ${project.name}` : 'Prosjekt er ikke valgt';
        });

        console.log(`Projectname: ${currentProject.value?.name}\nid: ${currentProject.value?.project_id}\nnumber of products: ${productList.value.length}`);
        console.log(productList.value)
        return { isLoggedInComputed, userComputed, currentProject, heading, 
          productList, pushToProducts, popFromProducts
        };
      },

    data() {
      return {
        // Table content
        tableEntries: [
          {heading: 'Bygningsdel', body: 'bygningsdel', sortable: true},
          {heading: 'Produktgruppe', body: 'produktgruppe', sortable: true},
          {heading: "Navn", body: 'name', sortable: true},
          {heading: "Produkt", body: 'type', sortable: true},
          {heading: "Mengde", body: 'quantity', sortable: false},
          {heading: "Enhet", body: 'unit', sortable: false},
        ],
        // Modal data
        isAddModalActive: false,
        isUpdateModalActive: false,
        productToBeUpdated: null,
        // Table data
        currentSort: '',
        sortAscending: true,
        isCopyInProgress: false
      }
    },

    methods: {
      /**
       * Toggle modales
       */
      toggleAddModal() {
        console.log('toggleAddModal called'); // For testing
        this.isAddModalActive = !this.isAddModalActive;
      },
      toggleUpdateModal() {
        console.log('toggleUpdateModal called'); // For testing
        this.isUpdateModalActive = !this.isUpdateModalActive;
      },

      /**
       * Sort the table by the heading indicated by currentSort and direction indicated by sortAscending
       * Store the updated preferenses in locale storeage
       */
      sortTable(entry) {
        console.log(entry)
        this.sortAscending = this.currentSort === entry.body ? !this.sortAscending : false;
        this.currentSort = entry.body;

        saveToLocalStorage('productsPreferences', {
          sortAscending: this.sortAscending,
          currentSort: this.currentSort
        })
        console.log(`this.sortAscending: ${this.sortAscending}\nthis.currentSort: ${this.currentSort}`);
      },

      /**
       * Hanlders for submit events from AddModal and UpdateModal
       * Submit to server and update global state
       */
      async handleAddModalSubmit(productData) {
        // moves the content of the product property into the root object-body and append project_id
        console.log('project_id: ' + this.currentProject.project_id)
        const fullProjectData = {
            ...productData,
            ...productData.product,
            project_id: this.currentProject.project_id
        };
        // product.product is now part of the main object
        delete fullProjectData.product;

        const newProduct = await postData(fullProjectData, '/products/add')
        console.log(newProduct)

        if (newProduct.status === 'failed') {
          const message = newProduct?.message ?? 'En feil har oppstått!';
          displayErrorToast(message);
          return;
        }
        
        this.pushToProducts(newProduct);
        displaySuccessToast('Produktet er registrert')
        this.isAddModalActive = false;
      },
      async handleUpdateModalSubmit(productData) {
        // Resets productToBeUpdated for next time.
        this.productToBeUpdated = null;
        console.log(productData)
        const db_response = await updateData(productData, '/products/update');

        if (db_response.status === 'failed') {
          const message = db_response?.message ?? 'Produktet kunne ikke oppdateres!';
          displayErrorToast(message);
          return;
        }
        
        this.popFromProducts(productData.product_id);
        this.pushToProducts(productData);
        displaySuccessToast('Produktet er oppdatert')
        this.isUpdateModalActive = false;
      },
      async deleteButtonHandler(product) {
        console.log('Deleting product:', product.name);
        const product_id = product.product_id
        const db_response = await deleteData(`/products/delete/${product_id}`)
        
        if (db_response.status !== 'success') {
          const message = db_response?.message ?? 'Produtet kunne ikke slettes!';
          displayErrorToast(message);
          return;
        }

        displaySuccessToast('Produktet er slettet!')
        this.popFromProducts(product_id);
      },

      /**
       * Hanlders for click events from the drop-down menu
       * Submit to server and update global state
       */
      editButtonHandler(product) {
        console.log('Editing product:', product.name);
        this.productToBeUpdated = product;
        this.toggleUpdateModal();
      },
      async copyButtonHandler(product) {
        // isCopyInProgress is used to avoid overlapping copy events
        if (this.isCopyInProgress) {
            displayErrorToast('Kopiering pågår, venligst vent.');
            return;
        }
        this.isCopyInProgress = true;   

        console.log('Copying product:', product.name);
        product = cloneDeep(product);
        product.product = {};
        console.log(product);
        await this.handleAddModalSubmit(product);
        this.isCopyInProgress = false;
      }
    },

    mounted() {
      this.productList.forEach(product => {
        if (!product.displayedName) {
          product.displayedName = setDisplayedName(product, 35);
        }
      })

      const productsPreferences = getFromLocalStorage('productsPreferences');

      this.currentSort = productsPreferences?.currentSort ?? 'bygningsdel';
      this.sortAscending = productsPreferences?.sortAscending ?? true;
    },
    computed: {
      sortedProducts() {
      const modifier = this.sortAscending === false ? 1 : -1;
      return sortByField(this.productList, this.currentSort, modifier);
    }
    }
  };
</script>
  
<style scoped>
  h2 {
      margin-bottom: 1.4rem;
      margin-top: 0.2rem;
    }
  .heading {
    width: 100%;
    padding: 0.1em;
    padding-left: 0; 
    font-weight: bold;
  }
  .faded-icon {
    opacity: 0.6;
  }
  .toggle-modal-button {
    margin-bottom: 1.5em;
  }
  .ellipsis-container {
    padding-top: 0.1em;
    padding-bottom: 0.1em;
    margin: 0;
  }
  .if-copying-active {
      margin-top: -0.5em;
      padding-top: 0;
      height: 2em;
    }
  /* 
    Alows dropdown menus inside table-responsive-md elements to work properly on small screens
    - For small screens (width <= 767px): dropdown menus have a static position
    - For small screens (width >= 768px): table-responsive elements overflow visibly => full content display

    Thanks to leocaseiro https://dcblog.dev/stop-bootstrap-drop-menus-being-cut-off-in-responsive-tables  
  */
  @media (max-width: 767px) {
    .table-responsive-md .dropdown-menu {
        position: static !important;
        -webkit-overflow-scrolling: touch; /* Enables smooth scrolling on touch screens*/
    }
  }
  @media (min-width: 768px) {
      .table-responsive {
          overflow: visible;
      }
  }
</style>