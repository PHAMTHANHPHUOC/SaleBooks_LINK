import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import Client from './layout/wrapper/ClientMaster.vue'
import Blank from './layout/wrapper/index_blank.vue'
import './assets/css/global.css'
const app = createApp(App)

app.use(router)

app.component("client-layout", Client);
app.component("blank-layout", Blank);

app.mount("#app")