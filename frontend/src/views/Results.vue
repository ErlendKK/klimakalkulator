<template>
  <div class="layout">
    <nav-header></nav-header>
    <main class="container"> 
      <h2>{{ heading }}</h2>
      <div v-if="isLoggedInComputed && currentProject">

        <!-- Dropdown menu for selecting unit -->
        <select id="selectedDataFormat-dropdown" class="form-control" 
          v-model="selectedDataFormat" @change="handleFormatSelection"  required>
          <option 
            v-for="format in dataFormats"
            :key="format" 
            :value="format">
            {{ format }}
          </option>
        </select>

        <!-- Table of emission data -->
        <div class="table-responsive">
          <table class="table table-hover table-sm" >
            <thead class="table-light">
              <tr>
                <th
                  v-for="heading in tableHeadings"
                  :key="heading"
                  scope="row">
                  {{ heading }}
                </th>
              </tr> 
            </thead>
            <tbody>
              <tr v-for="row in resultList.slice(0, resultList.length - 1)" :key="row.bygningsdel">
                <td v-for="(value, key) in row" :key="key">
                  {{ value }}
                </td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td v-for="(value, key) in resultList[resultList.length - 1]" :key="key">
                  {{ value }}
                </td>
              </tr>
            </tfoot>
          </table>

          <!-- Display chart -->
        </div>
          <hr class="content-seperator">
          <PieChart :resultList="resultList"/>
        </div>
        <div v-else-if="userComputed === null">
          <p>Logg inn for å se resultater</p>
        </div>
        <div v-else>
          <p>Velg et prosjekt</p>
        </div>
      </main>

    <nav-footer></nav-footer>
  </div>
</template>
  
<script>
  // import BygningsdelChart from '../components/BygningsdelChart.vue'
  import PieChart from '../components/PieChart.vue'
  import NavFooter from '../components/NavFooter.vue';
  import NavHeader from '../components/NavHeader.vue';
  import { useAuthStore } from '../stores/authStore';
  import { computed } from 'vue';

  export default {
    name: 'Results',
    components: {
      NavHeader,
      NavFooter,
      PieChart
    },

    setup() {
      const authStore = useAuthStore();
      const isLoggedInComputed = computed(() => authStore.isLoggedIn);
      const userComputed = computed(() => authStore.user);
      const currentProject = computed(() => authStore.currentProject);
      const productList = computed(() => currentProject.value?.products ?? []);
      
      const heading = computed(() => {
          return currentProject.value?.name ? `Resutater: ${currentProject.value?.name}` : 'Prosjekt er ikke valgt';
      });

      return { isLoggedInComputed, userComputed, currentProject, heading, productList };
    },

    data() {
      return {

        tableHeadings: [
          'Bygningsdel',
          'A1-A3',
          'A4',
          'B2',
          'B4',
          'C',
          'Total',
          'Andel'
        ],
        resultList: [
          { bygningsdel: 'Grunn og fundamenter (21)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
          { bygningsdel: 'Bæresystemer (22)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
          { bygningsdel: 'Yttervegger (23)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
          { bygningsdel: 'Innervegger (24)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
          { bygningsdel: 'Dekker (25)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
          { bygningsdel: 'Yttertak (26)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
          { bygningsdel: 'Trapper, balkonger m.m. (28)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
          { bygningsdel: 'Utendørs konstruksjoner (72)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
          { bygningsdel: 'Totalt', 'A1-A3': 0, 'A4': 0, 'B2': 6, 'B4': 0, 'C': 0, total: 0, andel: '0%' }
        ],
        dataFormats: [
          "kg CO2e",
          "tonn CO2e",
          "kg CO2e per kvm per år"
        ],
        selectedDataFormat: "kg CO2e",
        numberA: 10,
        numberB: 12
      }
    },
    methods: {
      resetResultList() {
        // Reset all emissions values to zero before calculation
        this.resultList.forEach(row => {
          row['A1-A3'] = 0;
          row['A4'] = 0;
          row['B2'] = 0;
          row['B4'] = 0;
          row['C'] = 0;
        });
      },
      calculateEmissions(unitCoversionFactor) {
      // Aggregate emissions for each product       

        this.productList.forEach(product => {
            const currentRow = this.resultList.find(row => row.bygningsdel === product.bygningsdel);

            if (currentRow && product.emission_factors) {
              const emissions = product.emission_factors;

              // Total production emissions
              const totalA1A3 = (emissions.A1 + emissions.A2 + emissions.A3 + emissions.A1A2A3) * product.quantity * unitCoversionFactor;
              const totalA4 = emissions.A4 * product.quantity * unitCoversionFactor;
              // Total end-of-life emissions
              const totalC1C4 = (emissions.C1 + emissions.C2 + emissions.C3 + emissions.C3) * product.quantity * unitCoversionFactor;
              // Total emissions for replacing materials = [number of replacements] * (production emissions + end-of-life emissions)
              const totalB4 = (this.currentProject.analyseperiode / product.utskiftingsintervall) * (totalA1A3 + totalC1C4); // unitCoversionFactor is already accounted for
              const totalB2 = this.currentProject.analyseperiode * product.vedlikeholdsutslipp * product.quantity * unitCoversionFactor;
              console.log('totalB4: ' + totalB4)

              currentRow['A1-A3'] += totalA1A3;
              currentRow['A4'] += totalA4;
              currentRow['B2'] += totalB2;
              currentRow['B4'] += totalB4;
              currentRow['C'] += totalC1C4;
            }
        });
      },
      roundOffEmissions() {
        this.resultList.forEach(row => {
          row['A1-A3'] = parseFloat(row['A1-A3'].toFixed(this.decimalPlaces));
          row['A4'] = parseFloat(row['A4'].toFixed(this.decimalPlaces));
          row['B2'] = parseFloat(row['B2'].toFixed(this.decimalPlaces));
          row['B4'] = parseFloat(row['B4'].toFixed(this.decimalPlaces));
          row['C'] = parseFloat(row['C'].toFixed(this.decimalPlaces));
        });
      },
      updateDisplayedEmissions(unitCoversionFactor=1) {
        // Initate table and emission data
        this.resetResultList();
        this.calculateEmissions(unitCoversionFactor);
        this.roundOffEmissions(); 
        
        // Calculate totals and percentages for display
        let totalEmissions = 0;
        this.resultList.slice(0, -1).forEach(item => {
          item.total = item['A1-A3'] + item['A4'] + item['B2'] + item['B4'] + item['C'];
          item.total = parseFloat(item.total.toFixed(this.decimalPlaces));
          totalEmissions += item.total;
        });

        const totalRow = this.resultList[this.resultList.length - 1];
        totalRow['A1-A3'] = this.formatTableEntry('A1-A3');
        totalRow['A4'] = this.formatTableEntry('A4');
        totalRow['B2'] = this.formatTableEntry('B2');
        totalRow['B4'] = this.formatTableEntry('B4');
        totalRow['C'] = this.formatTableEntry('C');
        totalRow.total = parseFloat(totalEmissions.toFixed(this.decimalPlaces));

        this.resultList.forEach(item => {
          item.andel = `${Math.round(item.total / totalEmissions * 100)}%`;
        });
      },
      formatTableEntry(entry) {
        const emissions = this.resultList.reduce((acc, curr) => acc + curr[entry], 0)
        return parseFloat(emissions.toFixed(this.decimalPlaces));
      },
      handleFormatSelection() {
        console.log('handleFormatSelection called for factor: ' + this.selectedDataFormat);
        
        const conversionFactors = {
          "kg CO2e": 1,
          "tonn CO2e": .001,
          "kg CO2e per kvm per år": this.currentProject.bta && this.currentProject.analyseperiode
            ? 1 / (this.currentProject.bta * this.currentProject.analyseperiode)
            : 0,  // Handles undefined or zero values
        };

        const selectedConversionFactor = conversionFactors[this.selectedDataFormat];
        this.updateDisplayedEmissions(selectedConversionFactor);
      }
      
    },
    computed: {
      decimalPlaces() {
        return this.selectedDataFormat === "kg CO2e" ? 0 : 2;
      } 
    },
    mounted() {
      this.updateDisplayedEmissions();
    },

    };
</script>

<style scoped>
  .table-responsive {
    margin-top: 1.5em;
  }
  button {
      margin-bottom: 1.5em;
  }
  .content-seperator {
    margin-top: 2.5em;
    margin-bottom: 1.5em;
  }
</style>
