import App from './App.vue'
import router from './router'
import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import vuetify_css from 'vuetify/dist/vuetify.min.css'
//import vuetify_plugin from './plugins/vuetify';
import axios from 'axios'
Vue.config.productionTip = false

Vue.use(vuetify_css)
Vue.use(Vuetify)
export default new Vuetify({ })

new Vue({
  router,
  vuetify: new Vuetify(),
  axios,
  render: h => h(App)
}).$mount('#app')
