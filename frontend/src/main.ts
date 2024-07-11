import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { toastOptions } from './utils/toasts'
import { PieChart } from 'vue-chart-3'
import App from './App.vue';
import router from './router/index.js';
import Toast from "vue-toastification";

import ModalComponent from './components/modalComponent.vue';
import ResultsChart from './components/ResultsChart.vue';
import ProductAddModal from './components/ProductAddModal.vue';
import ProductUpdateModal from './components/ProductUpdateModal.vue';
import ProjectAddModal from './components/ProductAddModal.vue';
import ProjectUpdateModal from './components/ProductUpdateModal.vue';
import LoginModal from './components/LoginModal.vue';
import RegistrationModal from './components/RegistrationModal.vue';
import NavHeader from './components/NavHeader.vue';

import "vue-toastification/dist/index.css";
import './assets/layout.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const app = createApp(App);
const pinia = createPinia();

app.component('PieChart', PieChart);
app.component('ResultsChart', ResultsChart);
app.component('ModalComponent', ModalComponent);
app.component('ProductAddModal', ProductAddModal);

app.component('ProductUpdateModal', ProductUpdateModal);
app.component('ProjectAddModal', ProjectAddModal);
app.component('ProjectUpdateModal', ProjectUpdateModal);
app.component('LoginModal', LoginModal);
app.component('RegistrationModal', RegistrationModal);
app.component('NavHeader', NavHeader);

app.use(pinia);
app.use(router);
app.use(Toast, toastOptions);
app.mount('#app');