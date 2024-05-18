import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/aura-light-green/theme.css'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const toastOptions = {
    transition: "Vue-Toastification__fade",
    maxToasts: 8,
    newestOnTop: true,
    position: "top-right",
    timeout: 2500,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: true,
    closeButton: "button",
    icon: true,
    rtl: false
  };

const primeOptions = {
  unstyled: true
}

import './assets/layout.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const app = createApp(App);
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.use(PrimeVue, primeOptions);
app.use(Toast, toastOptions);

app.mount('#app')

// import { createVuetify } from 'vuetify';
// import 'vuetify/styles'; 
// const vuetify = createVuetify();
// app.use(vuetify);

