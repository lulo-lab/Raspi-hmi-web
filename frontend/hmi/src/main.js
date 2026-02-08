import { createApp } from 'vue'
import App from './App.vue'

// Importiere Element Plus und das CSS
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(ElementPlus)

app.mount('#app')
