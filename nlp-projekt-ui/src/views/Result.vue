<template>
  <div class="mx-6">
    <router-link to="/">
    <v-icon class="mr-2 " large>mdi-arrow-left</v-icon>
    </router-link>
    <h2>Wynik</h2>
    <v-row class="mt-2">
      <v-col cols="3" class="my-2">Predykcja opini: {{$store.state.response.rating}}</v-col>
      <v-col>
    <v-rating
      v-model="$store.state.response.rating"
      background-color="orange lighten-3"
      color="orange"
      readonly
    ></v-rating>
      </v-col>
    </v-row>
    <p class="mt-4 mb-6">Predykcja ilości opini: {{$store.state.response.rating_count}}</p>
        <v-text-field
      v-model="$store.state.response.title"
      label="Nazwa Przedmiotu"
      readonly
    ></v-text-field>

    <v-textarea
      v-model="$store.state.response.desc"
      label="Opis"
      readonly
      auto-grow
    ></v-textarea>

  </div>
</template>

<script>
import router from "../router"
import store from "../store"
export default {
  name: 'Result',
  components: {
  },
  data: () => ({}),

    methods: {
    },
    beforeRouteEnter(to, from, next) {
      console.log(from)
      if(!store.state.response){
        store.dispatch('showNotification', {text:'Nie załadowano danych.', timeout: 2000, color: 'red'})
        if(from.path !== '/' || from.name === null){
          router.push('/')}
      }
      else{
        next()
      }
    },
    beforeRouteLeave(to, from, next) {
      console.log('leave')
      this.$store.commit('removeResponse')
      next()
    }
}
</script>
