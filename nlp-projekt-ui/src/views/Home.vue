<template>
  <div class="home mx-6">
    <h2>Podaj nazwę i opis produktu</h2>
    <v-form
    ref="form"
    v-model="valid"
    lazy-validation
  >
        <v-text-field
      v-model="title"
      :rules="titleRules"
      label="Nazwa Przedmiotu"
      required
    ></v-text-field>

    <v-textarea
      v-model="desc"
      :rules="descRules"
      label="Opis"
      required      
      auto-grow
    ></v-textarea>

    <v-btn
      :disabled="!valid"
      color="success"
      class="mr-4"
      @click="validate"
    >
      Sprawdź
    </v-btn>

  </v-form>
  </div>
</template>

<script>
const axios = require('axios');
import router from '../router'
export default {
  name: 'Home',
  components: {
  },
  data: () => ({
      valid: true,
      title: '',
      titleRules: [
        v => !!v || 'Tytuł jest wymagany',
        v => (v && v.length >= 5) || 'Tytuł musi mieć minimum 6 znaków',
      ],
      desc: '',
      descRules: [
        v => !!v || 'Opis jest wymagany',
        v => (v && v.length >= 100) || 'Opis musi mieć minimum 100 znaków',
        v => (v && v.length <= 10000) || 'Opis może mieć maksimum 10000 znaków',
      ],
    }),

    methods: {
      validate () {
        if(this.$refs.form.validate()){
          axios.post('/api/prediction', {
            title: this.title,
            desc: this.desc,
          })
          .then((response) =>{
            if(response.data){
              this.title = ''
              this.desc = ''
              this.$store.commit('addResponse', response.data)
              router.push('result')
              console.log(response.data);
            }
            else{
              throw "Data not loaded"
              }
          })
          .catch( (error) =>{
            console.log(error);
            this.$store.dispatch('showNotification', {text:'Coś poszło nie tak ;(', timeout: 2000, color: 'red'});
          });
        }
      },
    },
}
</script>
