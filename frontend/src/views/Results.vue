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
                  v-for="key in Object.keys(resultList[0])"
                  :key="key"
                  scope="row">
                  {{ key }}
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
          <ResultsChart :resultList="resultList"/>
        </div>
        <div v-else-if="userComputed === null">
          <p>Logg inn for å se resultater</p>
        </div>
        <div v-else>
          <p><router-link to="/projects">Velg et prosjekt</router-link></p>
        </div>
      </main>

    <nav-footer></nav-footer>
  </div>
</template>
  
<script setup lang="ts">
  import ResultsChart from '../components/ResultsChart.vue';
  import NavFooter from '../components/NavFooter.vue';
  import NavHeader from '../components/NavHeader.vue';
  import { useAuthStore } from '../stores/authStore';
  import { computed, onMounted, ref } from 'vue';
  import { User, Product, Project, EmissionFactor, TableEntry, Result } from '../interfaces/interfaces'

  const authStore = useAuthStore();
  const isLoggedInComputed = computed(() => authStore.isLoggedIn);
  const userComputed = computed<User | null>(() => authStore.user);
  const currentProject = computed<Project | null>(() => authStore.currentProject);
  const productList = computed<Product[]>(() => currentProject.value?.products ?? []);
  console.log('TEST!!')
  console.log(currentProject.value)
  console.log(productList.value)

  const heading = computed(() => {
      return currentProject.value?.name ? `Resutater: ${currentProject.value?.name}` : 'Prosjekt er ikke valgt';
  });

  const resultList = ref<Result[]>([
    { bygningsdel: 'Grunn og fundamenter (21)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
    { bygningsdel: 'Bæresystemer (22)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
    { bygningsdel: 'Yttervegger (23)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
    { bygningsdel: 'Innervegger (24)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
    { bygningsdel: 'Dekker (25)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
    { bygningsdel: 'Yttertak (26)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
    { bygningsdel: 'Trapper, balkonger m.m. (28)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
    { bygningsdel: 'Utendørs konstruksjoner (72)', 'A1-A3': 0, 'A4': 0, 'B2': 0, 'B4': 0, 'C': 0, total: 0, andel: '0%' },
    { bygningsdel: 'Totalt', 'A1-A3': 0, 'A4': 0, 'B2': 6, 'B4': 0, 'C': 0, total: 0, andel: '0%' }
  ]);

  const dataFormats: readonly string[] = [
    "kg CO2e",
    "tonn CO2e",
    "kg CO2e per kvm per år"
  ];

  let selectedDataFormat = ref<string>("kg CO2e");

  function resetResultList(): void {
    // Reset all emissions values to zero before calculation
    resultList.value.forEach(row => {
      row['A1-A3'] = 0;
      row['A4'] = 0;
      row['B2'] = 0;
      row['B4'] = 0;
      row['C'] = 0;
    });
  }

  function calculateEmissions(unitCoversionFactor: number) {
  // Aggregate emissions for each product       

    productList.value.forEach(product => {
        const currentRow = resultList.value.find(row => row.bygningsdel === product.bygningsdel);

        if (currentRow && product.emission_factors) {
          const emissions = product.emission_factors;

          // Total production emissions
          const totalA1A3 = (emissions.A1 + emissions.A2 + emissions.A3 + emissions.A1A2A3) * product.quantity * unitCoversionFactor;
          const totalA4 = emissions.A4 * product.quantity * unitCoversionFactor;
          // Total end-of-life emissions
          const totalC1C4 = (emissions.C1 + emissions.C2 + emissions.C3 + emissions.C3) * product.quantity * unitCoversionFactor;
          // Total emissions for replacing materials = [number of replacements] * (production emissions + end-of-life emissions)
          const totalB4 = (currentProject.value.analyseperiode / product.utskiftingsintervall) * (totalA1A3 + totalC1C4); // unitCoversionFactor is already accounted for
          const totalB2 = currentProject.value.analyseperiode * product.vedlikeholdsutslipp * product.quantity * unitCoversionFactor;

          currentRow['A1-A3'] += totalA1A3;
          currentRow['A4'] += totalA4;
          currentRow['B2'] += totalB2;
          currentRow['B4'] += totalB4;
          currentRow['C'] += totalC1C4;
        }
    });
  }

  const decimalPlaces = computed(() => {
    return selectedDataFormat.value === "kg CO2e" ? 0 : 2;
  })

  function roundOffEmissions(): void {
    resultList.value.forEach(row => {
      row['A1-A3'] = parseFloat(row['A1-A3'].toFixed(decimalPlaces.value));
      row['A4'] = parseFloat(row['A4'].toFixed(decimalPlaces.value));
      row['B2'] = parseFloat(row['B2'].toFixed(decimalPlaces.value));
      row['B4'] = parseFloat(row['B4'].toFixed(decimalPlaces.value));
      row['C'] = parseFloat(row['C'].toFixed(decimalPlaces.value));
    });
  }

  function updateDisplayedEmissions(unitCoversionFactor: number = 1): void {
    // Initate table and emission data
    console.log('updateDisplayedEmissions called')
    resetResultList();
    calculateEmissions(unitCoversionFactor);
    roundOffEmissions(); 
    
    // Calculate totals and percentages for display
    let totalEmissions = 0;
    resultList.value.slice(0, -1).forEach(item => {
      item.total = item['A1-A3'] + item['A4'] + item['B2'] + item['B4'] + item['C'];
      item.total = parseFloat(item.total.toFixed(decimalPlaces.value));
      totalEmissions += item.total;
    });

    // Format each tableRow
    const lastIdx = resultList.value.length - 1;
    const totalRow = resultList.value[lastIdx];
    totalRow['A1-A3'] = formatTableEntry('A1-A3');
    totalRow['A4'] = formatTableEntry('A4');
    totalRow['B2'] = formatTableEntry('B2');
    totalRow['B4'] = formatTableEntry('B4');
    totalRow['C'] = formatTableEntry('C');
    totalRow.total = parseFloat(totalEmissions.toFixed(decimalPlaces.value));

    resultList.value.forEach(item => {
      item.andel = `${Math.round(item.total / totalEmissions * 100)}%`;
    });
  }

  function formatTableEntry(entry) {
    console.log('formatTableEntry called')
    const emissions = resultList.value.reduce((acc, curr) => acc + curr[entry], 0)
    return parseFloat(emissions.toFixed(decimalPlaces.value));
  }

  function handleFormatSelection() {
    console.log('handleFormatSelection called for factor: ' + selectedDataFormat.value);
    
    const conversionFactors = {
      "kg CO2e": 1,
      "tonn CO2e": .001,
      "kg CO2e per kvm per år": currentProject.value.bta && currentProject.value.analyseperiode
        ? 1 / (currentProject.value.bta * currentProject.value.analyseperiode)
        : 0,  // Handles undefined or zero values
    };

    const selectedConversionFactor = conversionFactors[selectedDataFormat.value];
    updateDisplayedEmissions(selectedConversionFactor);
  }

  onMounted(() => updateDisplayedEmissions());
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
