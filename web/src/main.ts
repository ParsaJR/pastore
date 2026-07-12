
// Fonts
import "@fontsource-variable/inter/wght.css"
import "@fontsource-variable/jetbrains-mono/wght.css"

import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from "pinia"
import 'vue3-toastify/dist/index.css';
import ui from '@nuxt/ui/vue-plugin'

const app = createApp(App)

const pinia = createPinia()

app.use(router)
app.use(ui)
app.use(pinia)


app.mount('#app')
