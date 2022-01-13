<template>
  <v-app id="inspire">
    <v-app-bar
      app
    >
    <router-link to="/">
    <v-icon class="mr-2 " large>mdi-home</v-icon>
    </router-link>
          <v-toolbar-title>Predykcja oceny produktu na podstawie jego opisu</v-toolbar-title>
      <v-spacer></v-spacer>

      <Authors/>
    </v-app-bar>

    <v-main class="grey lighten-3">
      <v-container>
        <v-row>
          <v-col>
            <v-sheet
              min-height="88vh"
              rounded="lg"
              class="pa-4"
            >
              <router-view/>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <Notification/>
  </v-app>
</template>

<script>
import Authors from '@/components/Authors.vue'
import Notification from '@/components/Notification.vue'
  export default {
    name: 'App',
    components: {
      Authors,
      Notification
    },

    data: () => ({
    }),
  }
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.router-link-active {

    text-decoration: none;

    //&.router-link-exact-active {
    //  color: #42b983;
    //}
}
</style>
