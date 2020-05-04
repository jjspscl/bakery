<template>
  <div class="container-fluid">
    <div class="col">
      <div class="row header">
        <h1>{{ pastry.name }}</h1>
        <b-form inline>
          <Dropdown
            :options="ingredient_names"
            v-on:selected="ingredientSelect"
            v-on:filter="ingredientQuery"
            class="mx-2 my-2"
            :disabled="false"
            :maxItem="10"
            name="ingredient"
            placeholder="Please select an option"
          />
          <div>
            <b-button
              variant="primary"
              class="my-2 mx-2"
              @click="addIngredient"> Add </b-button>
          </div>
        </b-form>
      </div>
      <Card class="row ingr-header">
       <div>Name</div>
       <div>Price</div>
       <div>Amount</div>
       <div>Subtotal</div>
       <div>Action</div>
      </Card>
      <div class="row">
        <Card v-for="(ingr, index) in pastry_ingredients" class="ingr-container">
          <div><h5>{{ get_ingredient(ingr).name }}</h5></div>
          <div>{{ get_ingredient(ingr).price }}</div>
          <div>
            <b-form @submit.prevent="" inline>
              <b-form-input
                :id="`iamount${index}`"
                class="mb-2 mr-sm-2 mb-sm-0"
                type="number"
                :value="ingr.unit"
                min="1"
                step="1"
                @change="ingredientGram($event, ingr)" /></b-form>
            </div>
          <div>{{ SumIngredient(ingr) }}</div>
          <div>
            <b-button
              variant="danger"
              @click="deleteIngredient(ingr)">Delete</b-button>
          </div>
          </Card>

      </div>
      <Card class="total-container">
        <div>Total Grams:{{ totalGrams }}</div>
          <div>
            <b-form @submit.prevent="" inline>
                <label
                label="Amount"/>
                <b-form-input
                  id="gpp"
                  class="mb-2 mr-sm-2 mb-sm-0"
                  type="number"
                  :value="pastry.gpp"
                  min="1"
                  step="1"
                  @change="total" /></b-form>
          </div>
          <div>Output in pcs: {{ OutputInPiece }}</div>
          <div>Total Cost: {{ totalCost.toFixed(2) }}</div>
          <div>Cost/pc: {{ (totalCost / pastry.gpp).toFixed(2) }}</div>
    </Card>
    </div>
  </div>
</template>

<script>
import Dropdown from '@/components/Dropdown'
import { mapState, mapGetters } from 'vuex'

export default {
  async middleware ({ route, store, redirect }) {
    // if (!(parseInt(route.params.id) in store.getters['aws/pastries'])) { return redirect('') }
    await store.dispatch('pastry/GetPastries')
    await store.dispatch('pastry/GetIngredients')
    await store.dispatch('pastry/GetPastryIngredients', route.params.id)
  },
  components: { Dropdown },
  data () {
    return {
      select_ingredient: null,
      total_grams: 0,
      grams_per_piece: 1
    }
  },
  beforeCreated () {
    window.removeEventListener('scroll', this.handleScroll)
  },
  beforeDestroyed () {
    window.removeEventListener('scroll', this.handleScroll)
  },
  computed: {
    pastry ({ $store, $route }) {
      return $store.getters['pastry/pastry']($route.params.id)
    },
    pastry_ingredients ({ $store, $route }) {
      return $store.getters['pastry/pastry_ingredients']($route.params.id)
    },
    totalGrams ({ $store, $route }) {
      return $store.state.pastry.pastry_ingredients.filter(e => e.pastry === parseInt($route.params.id)).reduce((a, b) => +a + +b.unit, 0)
    },
    OutputInPiece ({ $store, $route }) {
      const sum = $store.state.pastry.pastry_ingredients.filter(e => e.pastry === parseInt($route.params.id)).reduce((a, b) => +a + +b.unit, 0)
      return parseInt(parseFloat(sum) / parseFloat(this.pastry.gpp))
    },
    totalCost ({ $store, $route }) {
      function getCost (p) {
        return parseFloat($store.state.pastry.ingredients.find(e => e.id === parseInt(p)).price)
      }
      const indgr = $store.state.pastry.pastry_ingredients.filter(e => e.pastry === parseInt($route.params.id))
      const units = indgr.map(a => a.unit / 1000)
      const cost = indgr.map(a => a.ingredient).map(res => getCost(res))
      const total = [...units].map((e, i) => e * cost[i])
      return total.reduce((a, b) => a + b, 0)
    },
    ...mapState('pastry', {
      ingredients: 'ingredients'
    }),
    ...mapGetters('pastry', {
      ingredient_names: 'ingredient_names'
    })
  },
  methods: {
    handleScroll (event) {
      console.log(event)
    },
    ingredientSelect ($a) {
      this.select_ingredient = $a
    },
    async ingredientQuery ($a) {
      await this.$store.dispatch('pastry/GetIngredients')
    },
    addIngredient () {
      this.$store.dispatch('pastry/AddPastryIngredients',
        { id: this.$route.params.id, val: this.select_ingredient })
    },
    deleteIngredient (val) {
      this.$store.dispatch('pastry/DeletePastryIngredients',
        { obj: val })
    },
    get_ingredient (ingr) {
      return this.$store.getters['pastry/ingredient'](ingr.ingredient)
    },
    SumIngredient (obj) {
      const price = this.$store.getters['pastry/ingredient'](obj.ingredient).price
      return ((parseFloat(obj.unit) / 1000) * parseFloat(price)).toFixed(2)
    },
    ingredientGram (val, obj) {
      try {
        this.$store.dispatch('pastry/UpdatePastryIngredients', { val, obj })
      } catch (error) {
        console.log(error)
      }
    },
    async total (val) {
      const p = { ...this.pastry }
      p.gpp = parseInt(val)
      const data = await this.$axios
        .$put(process.env.API_URL + 'pastry/', p)
        .catch((error) => {
          if (error.response) {
            console.log(error.response)
            // this.errors = [error.response.data.message]
          } else {
            console.log('Error', error.message)
          }
        })
      await this.$store.commit('pastry/UpdatePastry', data)
    }
  }
}
</script>

<style>
.container-fluid{
  padding: 0;
  height: 100vh;
}

.header{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  padding: 15px;
}

.header form {
  display: flex !important;
}

.header form > div {
  flex: 1;
}
.ingr-container{
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  text-align: center;
  width: 100%;
}

.ingr-container > div{
  flex: 1;
}

.ingr-container input * {
  width: 100%;
}

.ingr-header {
  display:flex;
  flex-direction: row;
  text-align: center;
}

.ingr-header > div {
  flex: 1;
}

.total-container {
  margin-top: auto !important;
}
</style>
