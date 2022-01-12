<template>
  <div class="mx-6">
    <h2>Wynik</h2>
    <v-row class="mt-2">
      <v-col cols="2" class="my-2">Predykcja opini: {{rating}}</v-col>
      <v-col>
    <v-rating
      v-model="rating"
      background-color="orange lighten-3"
      color="orange"
      readonly
    ></v-rating>
      </v-col>
    </v-row>
    <p class="mt-4 mb-6">Predykcja ilości opini: {{rating_count}}</p>
        <v-text-field
      v-model="title"
      label="Nazwa Przedmiotu"
      disabled
    ></v-text-field>

    <v-textarea
      v-model="desc"
      label="Opis"
      disabled
    ></v-textarea>

  </div>
</template>

<script>

export default {
  name: 'Result',
  components: {
  },
  data: () => ({
      rating: 3,
      rating_count: 8,
      title: 'Lorem ipsum dolor sit amet',
      desc: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque et magna elit. Sed in arcu ac est pretium tincidunt. Sed in placerat augue. Nulla quis mauris vel ante porta molestie eget a nisi. Vestibulum rutrum nisi sed facilisis finibus. In hac habitasse platea dictumst. Nulla facilisi. Maecenas erat lacus, pharetra at tortor ac, scelerisque malesuada nulla. Nullam mattis condimentum tincidunt. Etiam eu massa condimentum, rhoncus dolor nec, lobortis massa. Nam tempor pellentesque est quis gravida. Pellentesque felis est, faucibus vel lacinia vel, sagittis et urna.',
    }),

    methods: {
    },
}
</script>
