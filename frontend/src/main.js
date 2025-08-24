import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Chartkick from 'vue-chartkick'
import Chart from 'chart.js/auto' // Import Chart.js with auto-registration

createApp(App).use(router).use(Chartkick.use(Chart)).mount('#app')
