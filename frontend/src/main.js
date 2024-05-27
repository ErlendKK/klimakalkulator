import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { toastOptions } from './utils/toasts.js'
import App from './App.vue';
import router from './router';
import Toast from "vue-toastification";

import "vue-toastification/dist/index.css";
import './assets/layout.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(Toast, toastOptions);
app.mount('#app');