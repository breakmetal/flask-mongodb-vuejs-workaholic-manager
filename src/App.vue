<template>
  <v-app>
    <layout-main></layout-main>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';
import layoutMain from './components/layouts/layout-main'

export default {
  name: 'App',
  components: {
    HelloWorld,
    layoutMain
  },
  data: () => ({
    //
  }),
};
</script>
