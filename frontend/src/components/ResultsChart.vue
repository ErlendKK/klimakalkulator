<template>
  <div class="chart-container" style="position: relative">
    <PieChart :chartData="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
  import { PieChart } from 'vue-chart-3';
  import { Chart, registerables } from 'chart.js';
  import { computed, ref, onMounted, watch } from 'vue';
  import { ServerResponse, User, Product, Project, EmissionFactor, TableEntry, Result } from '../interfaces/interfaces';

  Chart.register(...registerables);

  // Defines props
  const props = defineProps<{ 
    resultList: Result[]
  }>();

  let localResultList: Result[] = [];
  let chartData = ref({});

  let chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'right',
        labels: {
          boxWidth: 18,
          padding: 15,
        }
      }
    }
  }

  onMounted(() => initChartData());

  // Watcher equivalent to the watch property in Options API
  watch(props.resultList, (newVal, oldVal) => {
    initChartData();
  }, { deep: true });

  /**
   * Creates/recreates the pie chart
   * Filter out items where 'bygningsdel' is 'Totalt'
   * Prepare chart data using filtered resultList
   */
  function initChartData(): void {
    const strippedResultList: Result[] = props.resultList.filter(item => item.bygningsdel !== 'Totalt');
    const chartLabels: string[] = strippedResultList.map(item => item.bygningsdel);

    chartData.value = {
      labels: chartLabels,
      datasets: [{
        label: 'Bygningsdel Distribution',
        data: strippedResultList.map(item => item['A1-A3'] + item['A4'] + item['B2'] + item['B4'] + item['C']),
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF']
      }]
    };
  }
</script>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'ResultsChart',
});
</script>

<style scoped>
  .chart-container {
    display: flex;
    align-items: center;
    max-height: 220px;
    min-height: 220px;
    border: 1px solid black;
    padding: 0.2em;
    margin-bottom: 1em;
  }
</style>