<template>
    <div class="layout">
      <Nav-header></Nav-header>
      
      <main class="container">
        <h2>{{ heading }}</h2>
        <div v-if="isLoggedInComputed && currentProject">

          <!-- Open productModal to add new product to the project -->
          <button type="button" class="btn btn-primary" 
            @click="toggleAddModal">
            Nytt Produkt
          </button>
          <product-modal
            :is-active="isAddModalActive"
            @close="isAddModalActive = false"
            @submit-product="handleAddModalSubmit">
          </product-modal>
          <!-- Open productUpdateModal to add new product to the project -->
          <!-- Uses v-if to trigger mounted() everytime its activated -->
          <Product-update-modal
            v-if="isUpdateModalActive"
            :is-active="isUpdateModalActive"
            :productToBeUpdated="productToBeUpdated"
            @close="isUpdateModalActive = false"
            @submit-product="handleUpdateModalSubmit">
          </Product-update-modal>
    
          <!-- Table of products included in the project -->
          <table class="table table-hover table-sm">
            <thead>
              <tr>
                <th v-for="entry in tableEntries" :key="entry">
                  {{ entry.heading }}
                  <template  v-if="entry.sortable">
                    <i
                      :class="{
                        'fa-solid': true, 
                        'fa-sort': entry.body !== currentSort, 
                        'fa-sort-down': entry.body === currentSort && !sortAscending, 
                        'fa-sort-up': entry.body === currentSort && sortAscending
                      }"
                      @click="sortTable(entry)">
                    </i>
                  </template>
                </th>
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
                <td>
                  <div class="dropdown">
                    <a class="btn " href="#" role="button" id="dropdownMenuLink" data-bs-toggle="dropdown" aria-expanded="false">
                      <i class="fa-solid fa-ellipsis"></i>
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                      <li><a class="dropdown-item" href="#" @click="deleteButtonHandler(product)">Slett</a></li>
                      <li><a class="dropdown-item" href="#" @click="editButtonHandler(product)">Rediger</a></li>
                      <li><a class="dropdown-item" href="#" @click="copyButtonHandler(product)">Lag kopi</a></li>
                    </ul>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- TODO: Implement page when not logged in -->
        <div v-else-if="userComputed === null">
          <p>Logg inn for å se materialer</p>
        </div>
        <div v-else>
          <p>Velg et prosjekt</p>
        </div>
      </main>

      <nav-footer />
    </div>
</template>
    
<script>
  import NavHeader from '../components/NavHeader.vue';
  import NavFooter from '../components/NavFooter.vue';
  import ProductModal from '../components/ProductModal.vue';
  import ProductUpdateModal from '../components/ProductUpdateModal.vue';
  import { getData, postData, deleteData, updateData } from '../utils/http-requests.js'
  import { saveToLocalStorage, getFromLocalStorage } from '../utils/local-storage.js'
  import { setDisplayedName } from '../utils/misc.js'
  
  import { useAuthStore } from '../stores/authStore';
  import { computed } from 'vue';
  import { useToast } from "vue-toastification";

  export default {
      name: 'Products',
      components: {
        NavHeader,
        NavFooter,
        ProductModal,
        ProductUpdateModal
      },

      setup() {
        const authStore = useAuthStore();

        const isLoggedInComputed = computed(() => authStore.isLoggedIn);
        const userComputed = computed(() => authStore.user);
        const currentProject = computed(() => authStore.currentProject);
        const productList = computed(() => currentProject.value?.products ?? []);
        const toast = useToast();
        const pushToProducts = authStore.pushToProducts;
        const popFromProducts = authStore.popFromProducts;

        const heading = computed(() => {
          const project = currentProject.value;
          return project ? `Produktoversikt: ${project.name}` : 'Prosjekt er ikke valgt';
        });

        function displaySuccessToast(message="Suksess!") {
          toast.success(message);
        }

        function displayErrorToast(message="Error!") {
          toast.error(message);
        }

        function displayWarningToast(message="Obs!") {
          toast.warning(message);
        }

        console.log(`Projectname: ${currentProject.value?.name}\nid: ${currentProject.value?.project_id}\nnumber of products: ${productList.value.length}`);

        return { isLoggedInComputed, userComputed, currentProject, heading, 
          productList, pushToProducts, popFromProducts, displaySuccessToast, 
          displayErrorToast, displayWarningToast 
        };
      },

    data() {
      return {
        tableEntries: [
          {heading: 'Bygningsdel', body: 'bygningsdel', sortable: true},
          {heading: 'Produktgruppe', body: 'produktgruppe', sortable: true},
          {heading: "Navn", body: 'name', sortable: true},
          {heading: "Produkt", body: 'type', sortable: true},
          {heading: "Mengde", body: 'quantity', sortable: false},
          {heading: "Enhet", body: 'unit', sortable: false},
        ],
        currentSort: '', // entry.body
        sortAscending: true,
        isAddModalActive: false,
        isUpdateModalActive: false,
        productToBeUpdated: null,
      }
    },

    methods: {
      toggleAddModal() {
        console.log('toggleAddModal called'); // For testing
        this.isAddModalActive = !this.isAddModalActive;
      },
      toggleUpdateModal() {
        console.log('toggleUpdateModal called'); // For testing
        this.isUpdateModalActive = !this.isUpdateModalActive;
      },
      sortTable(entry) {
        console.log(entry)
        this.sortAscending = this.currentSort === entry.body ? !this.sortAscending : false;
        this.currentSort = entry.body;

        saveToLocalStorage('productsPreferences', {
          sortAscending: this.sortAscending,
          currentSort: this.currentSort
        })
        console.log(this.sortAscending)
        console.log(this.currentSort)
      },

      async handleAddModalSubmit(productData) {
        // move the content of the product property into the root object-body and append project_id
        console.log('project_id: ' + this.currentProject.project_id)
        const fullProjectData = {
            ...productData,
            ...productData.product,
            project_id: this.currentProject.project_id
        };
        delete fullProjectData.product;
        console.log(fullProjectData)

        const newProduct = await postData(fullProjectData, '/products/add')
        console.log(newProduct)

        if (newProduct.status === 'failed') {
          const message = newProduct?.message ?? 'En feil har oppstått!';
          this.displayErrorToast(message);
          return;
        }
        
        this.pushToProducts(newProduct);
        this.displaySuccessToast('Produktet er registrert')
        this.isAddModalActive = false;
      },

      async handleUpdateModalSubmit(productData) {
        // Resets productToBeUpdated for next time.
        this.productToBeUpdated = null;
        console.log(productData)
        const db_response = await updateData(productData, '/products/update');

        if (db_response.status === 'failed') {
          const message = db_response?.message ?? 'Produktet kunne ikke oppdateres!';
          this.displayErrorToast(message);
          return;
        }
        
        this.popFromProducts(productData.product_id);
        this.pushToProducts(productData);
        this.displaySuccessToast('Produktet er oppdatert')
        this.isUpdateModalActive = false;
      },

      async deleteButtonHandler(product) {
        console.log('Deleting product:', product.name);
        const product_id = product.product_id
        const db_response = await deleteData(`/products/delete/${product_id}`)
        
        if (db_response.status !== 'success') {
          const message = db_response?.message ?? 'Produtet kunne ikke slettes!';
          this.displayErrorToast(message);
          return;
        }

        this.displaySuccessToast('Produktet er slettet!')
        this.popFromProducts(product_id);
      },

      editButtonHandler(product) {
        console.log('Editing product:', product.name);
        this.productToBeUpdated = product;
        this.toggleUpdateModal();
      },
      copyButtonHandler(product) {
        console.log('Copying product:', product.name);
        product.product = {};
        console.log(product);
        this.handleAddModalSubmit(product);
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
        return this.productList.sort((a, b) => {
          const modifier = this.sortAscending === false ? 1 : -1;

          if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
          if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
          return 0;
        });
      }
    }
  };
</script>
  
<style scoped>
  button {
    margin-bottom: 1.5em;
  }
</style>