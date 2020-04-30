<template>
  <div class="container-fluid">
    <h1>{{ pastry.name }}</h1>
    <b-form inline>
      <Dropdown
        :options="ingredient_names"
        v-on:selected="ingredientSelect"
        v-on:filter="ingredientDropdown"
        :disabled="false"
        name="ingredient"
        :maxItem="10"
        placeholder="Please select an option"
      />

      <b-form-input :id="`amount`" :type="'number'"></b-form-input>
      <b-button variant="primary">
        Save
      </b-button>
    </b-form>

    {{ ingredients }}
  </div>
</template>

<script>
import Dropdown from '@/components/Dropdown'
import { mapState, mapGetters } from 'vuex'

export default {
  async middleware ({ route, store }) {
    await console.log(route.params, store)
    store.dispatch('pastry/GetPastries')
    store.dispatch('pastry/GetIngredients')
  },
  components: { Dropdown },
  data () {
    return {
    }
  },
  computed: {
    pastry ({ $store, $route }) {
      return $store.getters['pastry/pastry']($route.params.id)
    },
    ...mapState('pastry', {
      ingredients: 'ingredients'
    }),
    ...mapGetters('pastry', {
      ingredient_names: 'ingredient_names'
    })
  },
  methods: {
    ingredientSelect ($a) {
      console.log('SELECT:', $a)
    },
    ingredientQuery ($a) {
      console.log('SELECT:', $a)
    }
  }
}
</script>

<style>
</style>
