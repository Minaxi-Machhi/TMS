import App from '@/App.vue';
import { registerPlugins } from '@core/utils/plugins';
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community';
import { createApp } from 'vue';
import { PerfectScrollbarPlugin } from 'vue3-perfect-scrollbar';
import router from './router';
import loaderUtility from './utilities/loader/loader-utility';

import '@core/scss/template/index.scss';
import '@layouts/styles/index.scss';
import 'vue3-perfect-scrollbar/style.css';

// Create vue app
const app = createApp(App);
app.use(router);
app.use(PerfectScrollbarPlugin)

// Register plugins
registerPlugins(app);

// Register loader component from loader-utility
app.component("LoaderComponent", loaderUtility.LoaderComponent);

// Register all Community features
ModuleRegistry.registerModules([AllCommunityModule]);

// Mount vue app
app.mount('#app');
