<template>
<div class="text-center">
    <v-dialog
      v-model="dialog"
      width="500"
      transition="dialog-bottom-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs"
          v-on="on" 
          icon>
        <v-icon>mdi-information</v-icon>
      </v-btn>
        
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Projekt Zaliczeniowy na przedmiot NLP
        </v-card-title>

        <v-card-text class="pt-2">
          <p>Temat: Predykcja oceny produktu na podstawie jego opisu</p>

        Autorzy:
        <ul>
        <li>Wolski Jakub, nr indeksu: 323 588</li>
        <li>Wojciech Maciejewski, nr indeksu: 293 143</li>
        </ul>
         </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  export default {
    name: 'Authors',

    data: () => ({
      
      dialog: false,
    }),
  }
</script>
