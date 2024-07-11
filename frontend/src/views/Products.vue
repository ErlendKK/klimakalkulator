<template>
  <div class="layout">
    <Nav-header></Nav-header>

    <main class="container">
      <h2>{{ heading }}</h2>
      <div v-if="isLoggedInComputed && currentProject">
        <!-- Open productModal to add new product to the project -->
        <button type="button" class="btn btn-primary toggle-modal-button" @click="toggleAddModal">
          Nytt Produkt
        </button>
        <product-add-modal
          :is-active="isAddModalActive"
          @close="isAddModalActive = false"
          @submit-product="handleAddModalSubmit"
        >
        </product-add-modal>

        <!-- Open productUpdateModal to add new product to the project -->
        <Product-update-modal
          v-if="isUpdateModalActive"
          :is-active="isUpdateModalActive"
          :productToBeUpdated="productToBeUpdated"
          @close="isUpdateModalActive = false"
          @submit-product="handleUpdateModalSubmit"
        >
        </Product-update-modal>

        <!-- Table of products included in the project -->
        <div class="table-responsive-md">
          <table class="table table-sm table-hover">
            <thead class="table-light">
              <tr>
                <!-- For sortable columns display sort-icon and listen for click -->
                <th v-for="entry in tableEntries" :key="entry">
                  <template v-if="entry.sortable">
                    <button
                      type="button"
                      class="btn btn-default heading text-start text-nowrap"
                      @click="sortTable(entry)"
                    >
                      {{ entry.heading }}
                      <i
                        :class="{
                          'fa-solid': true,
                          'fa-sort': entry.body !== currentSort,
                          'fa-sort-down': entry.body === currentSort && sortAscending,
                          'fa-sort-up': entry.body === currentSort && !sortAscending,
                          'faded-icon': true,
                        }"
                      >
                      </i>
                    </button>
                  </template>
                  <template v-else>
                    <button
                      type="button"
                      disabled
                      class="btn btn-default border border-0 heading"
                      style="padding-left: 0; font-weight: bold"
                    >
                      {{ entry.heading }}
                    </button>
                  </template>
                </th>
                <!-- Empty heading for dropdown-menus -->
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(product, index) in sortedProducts" :key="index">
                <td>{{ product.bygningsdel }}</td>
                <td>{{ product.produktgruppe }}</td>
                <td>{{ product.displayedName }}</td>
                <td>{{ product.type }}</td>
                <td>{{ product.quantity }}</td>
                <td readonly>{{ product.unit }}</td>

                <!-- Dropdown menu for product-rows -->
                <td>
                  <div class="dropdown">
                    <a
                      class="btn ellipsis-container"
                      href="#"
                      role="button"
                      id="dropdownMenuLink"
                      data-bs-toggle="dropdown"
                      aria-expanded="false"
                    >
                      <i class="fa-solid fa-ellipsis"></i>
                    </a>
                    <ul class="dropdown-menu" aria-labelledby="dropdownMenuLink">
                      <li>
                        <a class="dropdown-item" href="#" @click="editButtonHandler(product)"
                          >Rediger</a
                        >
                      </li>
                      <li>
                        <a class="dropdown-item" href="#" @click="copyButtonHandler(product)"
                          >Lag kopi</a
                        >
                      </li>
                      <div class="dropdown-divider"></div>
                      <li>
                        <a class="dropdown-item" href="#" @click="deleteButtonHandler(product)"
                          >Slett</a
                        >
                      </li>
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
        <p>Logg inn for å se materialer</p>
      </div>
      <div v-else>
        <p><router-link to="/projects">Velg et prosjekt</router-link></p>
      </div>
    </main>

    <nav-footer />
  </div>
</template>

<script setup lang="ts">
import NavHeader from "../components/NavHeader.vue"
import NavFooter from "../components/NavFooter.vue"
import ProductAddModal from "../components/ProductAddModal.vue"
import ProductUpdateModal from "../components/ProductUpdateModal.vue"
import cloneDeep from "lodash/cloneDeep"
import { postData, deleteData, updateData } from "../utils/http-requests"
import { displaySuccessToast, displayErrorToast } from "../utils/toasts"
import { saveToLocalStorage, getFromLocalStorage } from "../utils/local-storage"
import { setDisplayedName, sortByField } from "../utils/misc"
import { initializeProduct } from "../utils/initializers"
import { useAuthStore } from "../stores/authStore"
import { computed, ref, onMounted } from "vue"
import {
  ServerResponse,
  User,
  Product,
  Project,
  TableEntry,
  SortPreference,
} from "../interfaces/interfaces"

const authStore = useAuthStore()
const isLoggedInComputed = computed(() => authStore.isLoggedIn)
const userComputed = computed<User | null>(() => authStore.user)
const currentProject = computed<Project | null>(() => authStore.currentProject)
const productList = computed<Product[]>(() => currentProject.value?.products ?? [])
const pushToProducts = authStore.pushToProducts
const popFromProducts = authStore.popFromProducts

const heading = computed(() => {
  const project = currentProject.value
  return project ? `Produktoversikt: ${project.name}` : "Prosjekt er ikke valgt"
})

let currentSort = ref<string>("")
let sortAscending = ref<boolean>(true)

let isAddModalActive = ref<boolean>(false)
let isUpdateModalActive = ref<boolean>(false)

let productToBeUpdated = ref<Product>(initializeProduct())
let isCopyInProgress = ref<boolean>(false)

console.log(
  `Projectname: ${currentProject.value?.name}\nid: ${currentProject.value?.project_id}\nnumber of products: ${productList.value.length}`
)
console.log(productList.value)

const tableEntries: TableEntry[] = [
  { heading: "Bygningsdel", body: "bygningsdel", sortable: true },
  { heading: "Produktgruppe", body: "produktgruppe", sortable: true },
  { heading: "Navn", body: "name", sortable: true },
  { heading: "Produkt", body: "type", sortable: true },
  { heading: "Mengde", body: "quantity", sortable: false },
  { heading: "Enhet", body: "unit", sortable: false },
]

function toggleAddModal(): void {
  console.log("toggleAddModal called")
  isAddModalActive.value = !isAddModalActive.value
}

function toggleUpdateModal(): void {
  console.log("toggleUpdateModal called")
  isUpdateModalActive.value = !isUpdateModalActive.value
}

function sortTable(entry: TableEntry): void {
  console.log(entry)
  sortAscending.value = currentSort.value === entry.body ? !sortAscending.value : false
  currentSort.value = entry.body

  saveToLocalStorage("productsPreferences", {
    sortAscending: sortAscending.value,
    currentSort: currentSort.value,
  })
  console.log("sortAscending: " + sortAscending.value)
  console.log("currentSort: " + currentSort.value)
}

async function handleAddModalSubmit(productData: Product): Promise<void> {
  // moves the content of the product property into the root object-body and append project_id
  console.log("project_id: " + currentProject.value.project_id)
  const fullProjectData: Product = {
    ...productData,
    ...productData.product,
    project_id: currentProject.value.project_id,
  }
  // product.product is now part of the main object
  delete fullProjectData.product

  const db_response: ServerResponse = await postData(fullProjectData, "/products/add")
  console.log(db_response)

  if (db_response.status === "failed") {
    const message = db_response?.message ?? "En feil har oppstått!"
    displayErrorToast(message)
    return
  }

  const newProduct = db_response.data as Product
  pushToProducts(newProduct)
  displaySuccessToast("Produktet er registrert")
  isAddModalActive.value = false
}

async function handleUpdateModalSubmit(productData: Product): Promise<void> {
  // Resets productToBeUpdated for next time.
  productToBeUpdated.value = initializeProduct()
  console.log(productData)
  const db_response: ServerResponse = await updateData(productData, "/products/update")

  if (db_response.status === "failed") {
    const message: string = db_response?.message ?? "Produktet kunne ikke oppdateres!"
    displayErrorToast(message)
    return
  }

  popFromProducts(productData.product_id)
  pushToProducts(productData)
  displaySuccessToast("Produktet er oppdatert")
  isUpdateModalActive.value = false
}

async function deleteButtonHandler(product: Product): Promise<void> {
  console.log("Deleting product:", product.name)
  const product_id = product.product_id
  const db_response: ServerResponse = await deleteData(`/products/delete/${product_id}`)

  if (db_response.status !== "success") {
    const message = db_response?.message ?? "Produtet kunne ikke slettes!"
    displayErrorToast(message)
    return
  }

  displaySuccessToast("Produktet er slettet!")
  popFromProducts(product_id)
}

function editButtonHandler(product: Product) {
  console.log("Editing product:", product.name)
  productToBeUpdated.value = product
  toggleUpdateModal()
}

async function copyButtonHandler(product: Product) {
  if (isCopyInProgress.value) {
    displayErrorToast("Kopiering pågår, venligst vent.")
    return
  }
  isCopyInProgress.value = true

  console.log("Copying product:", product.name)
  product = cloneDeep(product)
  product.product = {}
  console.log(product)
  await handleAddModalSubmit(product)
  isCopyInProgress.value = false
}

onMounted(() => {
  // Limit the length of the displayed projectname
  const numberOfCharacters = 35
  productList.value.forEach((product) => {
    if (!product.displayedName) {
      product.displayedName = setDisplayedName(product, numberOfCharacters)
    }
  })

  // sort the table based on the users preferences.
  const productsPreferences: SortPreference = getFromLocalStorage("productsPreferences")
  currentSort.value = productsPreferences?.currentSort ?? "bygningsdel"
  sortAscending.value = productsPreferences?.sortAscending ?? true
})

const sortedProducts = computed(() => {
  const modifier = sortAscending.value === false ? 1 : -1
  return sortByField(productList.value, currentSort.value, modifier)
})
</script>

<style scoped>
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
/* Thanks to leocaseiro https://dcblog.dev/stop-bootstrap-drop-menus-being-cut-off-in-responsive-tables */
@media (max-width: 767px) {
  .table-responsive-md .dropdown-menu {
    position: static !important;
    -webkit-overflow-scrolling: touch; /* Improves scrolling on touch devices */
  }
}
@media (min-width: 768px) {
  .table-responsive {
    overflow: visible;
  }
}
</style>
