<template>
  <div>
    <div ref="ProductModal" class="modal fade" :class="{ show: isActive, 'd-block': isActive }" tabindex="-1" role="dialog">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Legg til nytt produkt</h5>
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
                      <label for="bygningsdel-dropdown" class="form-label">Bygningsdel</label>
                      <select id="bygningsdel-dropdown" class="form-control" v-model="newProduct.bygningsdel" required>
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
                      <label for="produktgruppe-dropdown" class="form-label">Produktgruppe</label>
                      <select id="produktgruppe-dropdown" class="form-control" v-model="newProduct.produktgruppe" ref="produktgruppeDropdown" required>
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
              <div class="mb-3 row">
                <div class="col-md-6">
                  <label for="produktvalg-dropdown" class="form-label">Produkt</label>
                      <select id="produktvalg-dropdown" class="form-control" 
                        v-model="newProduct.product" 
                        @change="fetchEmissionData(newProduct.product)" 
                        required>
                        <!-- If ecoPortalData has been fetched; display productnames as options  -->
                        <template v-if="ecoPortalStatus === 'success' && ecoPortalData.length">
                          <option disabled value="">Velg Produkt</option>
                          <option v-for="product in ecoPortalData" :key="product.name" :value="product">
                            {{ product.displayedName }}
                          </option>
                        </template>
                        <!-- Else; display placeholder -->
                        <template v-else>
                          <option disabled value="">Laster Produktdata...</option>
                        </template>

                      </select>
                    </div>

                    <div class="col-md-6">
                  <label for="materialtypevalg-dropdown" class="form-label">Material</label>
                      <select id="materialtypevalg-dropdown" class="form-control" v-model="newProduct.type" required>
                          <option disabled value="">Velg Materialtype</option>
                          <option v-for="materialtype in materialTyper" :key="materialtype" :value="materialtype">
                            {{ materialtype }}
                          </option>
                      </select>
                    </div>
              </div>

              <div class="mb-3 row">
                  <!-- Mengde Input -->
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

                  <div class="col-sm-6">
                      <!-- Dropdown menu for selecting unit -->
                      <label for="enhet-dropdown" class="form-label">Enhet</label>
                      <select id="enhet-dropdown" class="form-control" v-model="newProduct.unit" required>
                        <!-- If newProduct.product has been defined; display unit  -->
                        <template v-if="displayUnit">
                          <option>{{ newProduct.unit }}</option>
                        </template>
                        <!-- Else; display placeholder -->
                        <template v-else>
                          <option disabled value=""></option>
                          <option disabled value="">{{ selectedProductStatus }}</option>
                        </template>
                      </select> 
                  </div>
              </div>

              <div class="mb-3 row">
                    <!-- Input form for utskiftingsintervall -->
                    <div class="col-md-6">
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
                    <div class="col-md-6">
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
    import { bygningsdeler } from '../utils/breeam.js'
    import { setDisplayedName } from '../utils/misc.js'
    import { getData } from '../utils/http-requests.js'
    import { useToast } from "vue-toastification";
   
    
    export default {
      name: 'ProductModal',
      props: {
        isActive: Boolean, // Used to display/ hide the modal
      },
      setup() {
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

            return { displaySuccessToast, displayErrorToast, displayWarningToast };
        },
      data() {
        return {
            bygningsdelsNavn: bygningsdeler.map(item => `${item.bygningsdel} (${item.nummer})`),
            bygningsdeler: bygningsdeler,
            materialTyper: [
                'Alle', 'Gips', 'Betong', 'Tre', 'Isolasjon', 'Membran', 'Stål', 'Aluminium',
                'Glass', 'Keramiske fliser', 'Granitt', 'PVC', 'Vinyl', 'Betongstein',
                'Asfalt', 'Akryl', 'Kobber', 'Sink', 'Leca', 'Kalksandstein', 'Annet'
            ],
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
          const productList = await getData('/products/full-productlist');
          
          if (productList.status === 'failed') {
            this.ecoPortalStatus = 'failed';
            this.displayWarningToast('Lastingen av produktinformasjon mislyktes');
            return;
          }

          // Limit name length to avoid overflow
          productList.forEach(product => {
            product.displayedName = setDisplayedName(product, 45)
          });

          this.ecoPortalStatus = 'success';
          this.ecoPortalData = productList;
        },

        closeModal() {
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
            this.displayErrorToast('Det oppstod en feil ved lastingen av utlsippsdata');
            return;
          }

          console.log('data.name: ' + selectedProduct.name + '\n' + selectedProduct)
          this.selectedProductStatus = 'success';
          this.newProduct.product = selectedProduct;

          this.newProduct.displayedName = setDisplayedName(selectedProduct, 45);
          this.newProduct.emission_factors = {...emissionData.emission_factors};
          this.newProduct.unit = emissionData.unit;
        }
    }
  }
</script>