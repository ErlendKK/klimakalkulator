<template>
  <div class="layout">
    <nav-header></nav-header>

    <main class="container"> 
      <h2>{{ heading }}</h2>
      <div v-if="isLoggedInComputed && currentProject">
        <table class="table table-hover table-sm" >
          <thead>
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
            <tr 
              v-for="row in resultList"
              :key="row.bygningsdel">
              <td
                v-for="(col, index) in row"
                :key="index">
                {{ col }}
              </td>
            </tr>
          </tbody>
        </table>
        <hr class="content-seperator">
        <BarChart :resultList="resultList"/>
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
  import BarChart from '../components/BarChart.vue'
  import NavFooter from '../components/NavFooter.vue';
  import NavHeader from '../components/NavHeader.vue';
  import { useAuthStore } from '../stores/authStore';
  import { computed } from 'vue';

  export default {
    name: 'Results',
    components: {
      NavHeader,
      NavFooter,
      BarChart
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
        ]
      }
    },
    methods: {
      updateEmissions() {
        console.log(this.productList)
        
        // Reset all emissions values to zero before calculation
        this.resultList.forEach(row => {
          row['A1-A3'] = 0;
          row['A4'] = 0;
          row['B2'] = 0;
          row['B4'] = 0;
          row['C'] = 0;
        });

        // Aggregate emissions for each product
        this.productList.forEach(product => {
          const currentRow = this.resultList.find(row => row.bygningsdel === product.bygningsdel);

          if (currentRow && product.emission_factors) {
            const emissions = product.emission_factors;

            // Total production emissions
            const totalA1A3 = (emissions.A1 + emissions.A2 + emissions.A3 + emissions.A1A2A3) * product.quantity;
            // Total end-of-life emissions
            const totalC1C4 = (emissions.C1 + emissions.C2 + emissions.C3 + emissions.C3) * product.quantity;
            // Total emissions for replacing materials = [number of replacements] * (production emissions + end-of-life emissions)
            const totalB4 = Math.floor(this.currentProject.analyseperiode / product.utskiftingsintervall) * (totalA1A3 + totalC1C4)
            const totalB2 = this.currentProject.analyseperiode * product.vedlikeholdsutslipp * product.quantity

            currentRow['A1-A3'] += Math.floor(totalA1A3);
            currentRow['A4'] += Math.floor(emissions.A4 * product.quantity);
            currentRow['B2'] += Math.floor(totalB2);
            currentRow['B4'] += Math.floor(totalB4);
            currentRow['C'] += Math.floor(totalC1C4);
          }
        });

        // Calculate totals and percentages for display
        let totalEmissions = 0;
        this.resultList.slice(0, -1).forEach(item => {
          item.total = item['A1-A3'] + item['A4'] + item['B2'] + item['B4'] + item['C'];
          totalEmissions += item.total;
        });

        const totalRow = this.resultList[this.resultList.length - 1];
        totalRow['A1-A3'] = this.formatTableEntry('A1-A3')
        totalRow['A4'] = this.formatTableEntry('A4')
        totalRow['B2'] = this.formatTableEntry('B2')
        totalRow['B4'] = this.formatTableEntry('B4')
        totalRow['C'] = this.formatTableEntry('C')
        totalRow.total = Math.floor(totalEmissions);

        this.resultList.forEach(item => {
          item.andel = `${Math.round(item.total / totalEmissions * 100)}%`;
        });
      },
      formatTableEntry(entry) {
        return Math.floor(this.resultList.reduce((acc, curr) => acc + curr[entry], 0));
      }
      
    },
    mounted() {
      this.updateEmissions();
    },

    };
</script>

<style scoped>
    button {
        margin-bottom: 1.5em;
    }
    .content-seperator {
      margin-top: 2.5em;
      margin-bottom: 1.5em;
    }
</style>
