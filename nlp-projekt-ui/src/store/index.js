import Vue from 'vue'
import Vuex from 'vuex'
import { v4 as uuidv4 } from 'uuid';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    notifications:[],
    response: null,
  },
  mutations: {
    addResponse(state, payload){
      state.response = payload
    },
    removeResponse(state){
      state.response = null
    },
    showNotification (state, payload) {
      state.notifications.push(payload)
    },
    removeNotification (state, payload) {
      for(var i = 0; i < state.notifications.length; i++){
        if(state.notifications[i].id === payload.id){
          state.notifications.splice(i, 1)
          break
        }
      }
    }
  },
  actions: {
    showNotification(state, payload){
      payload.show = true
      payload.id = uuidv4();
      this.commit('showNotification', payload)
      setTimeout(() =>{
        this.commit('removeNotification', payload)
      }, payload.timeout)
    }
  },
  modules: {
  }
})
