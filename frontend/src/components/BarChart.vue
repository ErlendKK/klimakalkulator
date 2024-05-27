<template>
  <div class="chart-container" style="position: relative">
    <Bar :reference="reference" 
         :emissionsTotal="emissionsTotal" 
         :options="chartOptions" />
  </div>
</template>


<script>
  import { Bar } from 'vue-chartjs'
  import { Chart, registerables } from 'chart.js'

  Chart.register(...registerables)

  export default {
    name: 'BarChart2',
    components: { Bar },
    props: {
      reference: Number,
      emissionsTotal: Number,

    },
    data() {
      return {
        chartData: {
          labels: ['Reference', 'Emissions Total'],
          datasets: [{
            label: 'Data',
            backgroundColor: ['#3498db', '#e74c3c'],
            data: [0, 0] // Initial data
          }]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true
            }
          }
      }
      }
    },
    created() {
      this.updateChartData();
    },
    methods: {
      updateChartData() {
        this.chartData.datasets[0].data = [this.reference, this.emissionsTotal];
        this.$refs.barChart.update();
      }
    },
    watch: {
      reference(newVal) {
        this.updateChartData();
      },
      emissionsTotal(newVal) {
        this.updateChartData();
      }
    }
  }
</script>