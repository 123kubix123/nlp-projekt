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
import router from '../router'
export default {
  name: 'Home',
  components: {
  },
  data: () => ({
      valid: true,
      title: 'Lorem ipsum dolor sit amet',
      titleRules: [
        v => !!v || 'Tytuł jest wymagany',
        v => (v && v.length >= 5) || 'Tytuł musi mieć minimum 6 znaków',
      ],
      desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque et magna elit. Sed in arcu ac est pretium tincidunt. Sed in placerat augue. Nulla quis mauris vel ante porta molestie eget a nisi. Vestibulum rutrum nisi sed facilisis finibus. In hac habitasse platea dictumst. Nulla facilisi. Maecenas erat lacus, pharetra at tortor ac, scelerisque malesuada nulla. Nullam mattis condimentum tincidunt. Etiam eu massa condimentum, rhoncus dolor nec, lobortis massa. Nam tempor pellentesque est quis gravida. Pellentesque felis est, faucibus vel lacinia vel, sagittis et urna.',
      descRules: [
        v => !!v || 'Opis jest wymagany',
        v => (v && v.length >= 100) || 'Opis musi mieć minimum 100 znaków',
        v => (v && v.length <= 10000) || 'Opis może mieć maksimum 10000 znaków',
      ],
    }),

    methods: {
      validate () {
        if(this.$refs.form.validate()){
          router.push('result')
        }
      },
    },
}
</script>
