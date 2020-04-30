import Vue from 'vue'
export const state = () => ({
  pastry: [],
  ingredients: []
})

export const getters = {
  pastries: state => state.pastry,
  pastry: state => (params) => {
    return state.pastry.find(e => e.id === parseInt(params))
  },
  ingredients: state => state.ingredients,
  ingredient_names: (state) => {
    return state.ingredients.map((a) => {
      return {
        name: a.name,
        id: a.id
      }
    })
  }
}

export const mutations = {
  AppendPastry (state, res) {
    state.pastry.push({
      id: res.id,
      name: res.name
    })
  },
  AppendPastries (state, data) {
    state.pastry = []
    data.forEach((res) => {
      state.pastry.push({
        id: res.id,
        name: res.name
      })
    })
  },
  UpdatePastry (state, obj) {
    state.pastry.forEach((e, index) => {
      if (e.id === obj.id) { Vue.set(state.pastry, index, obj) }
    })
  },
  AppendIngredients (state, data) {
    // console.log(data.map(a => a.name))
    data.forEach((res) => {
      const ix = state.ingredients.map(a => a.name).indexOf(res.name)
      if (ix === -1) {
        state.ingredients.push(res)
      } else {
        Vue.set(state.ingredients, ix, res)
      }
    })
  }
}

export const actions = {
  async GetPastries ({
    commit,
    $axios
  }, obj) {
    const data = await this.$axios
      .$get(process.env.API_URL + 'pastry/')
      .catch((error) => {
        if (error.response) {
          console.log(error.response)
          // this.errors = [error.response.data.message]
        } else {
          console.log('Error', error.message)
        }
      })
    await commit('AppendPastries', data)
  },
  async GetIngredients ({
    commit,
    $axios
  }, obj) {
    const data = await this.$axios
      .$get(process.env.API_URL + 'ingredients/')
      .catch((error) => {
        if (error.response) {
          console.log(error.response)
          // this.errors = [error.response.data.message]
        } else {
          console.log('Error', error.message)
        }
      })
    await commit('AppendIngredients', data)
  }
}
