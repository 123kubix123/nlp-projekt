<template>
  <div>
    <v-snackbar 
      v-for="notification in $store.state.notifications"
      v-bind:key="notification.id"
      v-model="notification.show"
    >
      {{ notification.text }}

      <template v-slot:action="{ attrs }">
        <v-btn
          :color="notification.color"
          text
          v-bind="attrs"
          @click="notification.show = false"
        >
          Zamknij
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
  export default {
    name: 'Notification',

    data: () => ({
    }),
  }
</script>
