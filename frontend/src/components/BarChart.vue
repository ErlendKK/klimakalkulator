<template>
    <div class="chart-container" style="position: relative">
      <PieChart :chartData="chartData" :options="chartOptions" />
    </div>
  </template>

<script>
import { PieChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
    name: 'BarChart',
    components: {
        PieChart
    },
    props: {
      resultList: Array
    },
    data() {
        return {
          localResultList: [],
          chartData: null,
          chartOptions: {
            responsive: true,
            plugins: {
              legend: {
                position: 'right',
                labels: {
                    boxWidth: 18,
                    padding: 15,
                }
              }
            },
            // maintainAspectRatio: true 
          },
        }
    },
    created() {
        this.initChartData();
    },
    watch: {
        resultList: {
            handler(newVal, oldVal) {
                this.initChartData();  // Reinitialize the chart data when resultList changes
            },
            deep: true  // Checking deeply through the objects within the array
        }
    },
    methods: {
        initChartData() {
            this.localResultList = this.resultList.filter(item => item.bygningsdel !== 'Totalt');
            this.chartData = {
              labels: this.localResultList.map(item => item.bygningsdel),
              datasets: [{
                  label: 'Bygningsdel Distribution',
                  data: this.localResultList.map(item => item['A1-A3'] + item['A4'] + item['B2'] + item['B4'] + item['C']),
                  backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF']
              }]
            };
        }
    }
}
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