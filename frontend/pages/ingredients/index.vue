<template>
  <div class="container-fluid">
    <div class="main">
      <h1> Ingredients </h1>
      <div class="pastry_create">
        <b-form @submit.prevent="createIngredient" inline>
          <b-form-input
            id="pastry_create"
            class="mb-2 mr-sm-2 mb-sm-0"
            placeholder="Ingredient Name"
            v-model="ingredientCreate.name"
            input />
          <b-form-input
            id="gpp"
            class="mb-2 mr-sm-2 mb-sm-0"
            type="number"
            v-model="ingredientCreate.price"
            min="1"
            step="1" />
          <b-button
            class="mb-2 mr-sm-2 mb-sm-0"
            type="submit"
            variant="success"
            >Create Pastry</b-button>
        </b-form>
        <b-form-invalid-feedback v-if="!ingredientCreateValid.state" :state="ingredientCreateValid.state">
            {{ ingredientCreateValid.message }}
        </b-form-invalid-feedback>
      </div>
    </div>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="my-table"
    />
    <b-table
      :per-page="perPage"
      :items="ingredients"
      :current-page="currentPage"
      :fields="fields"
      striped
      hover
    >
      <template v-slot:cell(name)="row">
        <b-form-input
          :id="`iname${row.item.id}`"
          class="mb-2 mr-sm-2 mb-sm-0"
          type="text"
          :value="row.item.name"
          @change="editIngredient($event, 'name', row.item)" />
      </template>
      <template v-slot:cell(price)="row">
        <b-form-input
          :id="`iprice${row.item.id}`"
          class="mb-2 mr-sm-2 mb-sm-0"
          type="number"
          :value="row.item.price"
          min="1"
          step="1"
          @change="editIngredient($event, 'price', row.item)" />
      </template>
      <template v-slot:cell(actions)="row">
        <b-button
          @click="showModal(row, $event.target, 'deleteModal')"
          size="sm"
          variant="danger"
        >
          Delete
        </b-button>
      </template>
    </b-table>
    <b-modal
      id="deleteModal"
      :title="infoModal.title"
      @hide="() => {
        this.infoModal.title = ''
        this.infoModal.content = ''
      }"
      hide-footer
    >
      <template v-slot:modal-title>
        Delete Pastry
      </template>
      <template v-slot:default="{ hide }">
        <div class="d-block text-center">
          <b-form @submit.prevent="deleteIngredient(hide, infoModal.content)">
            <h5>Are you sure you want to delete {{ infoModal.content.name }}?</h5>
            <b-button type="submit" block variant="success">
              Submit
            </b-button>
            <b-button @click="hide" block>
              Cancel
            </b-button>
          </b-form>
        </div>
      </template>
    </b-modal>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  middleware ({ store }) {
    store.dispatch('pastry/GetIngredients')
  },
  computed: {
    ...mapState('pastry', {
      ingredients: 'ingredients'
    }),
    rows () {
      return this.ingredients.length
    }
  },
  data () {
    return {
      perPage: 10,
      currentPage: 1,
      fields: [
        { key: 'id', label: 'ID', sortable: true, sortDirection: 'desc' },
        { key: 'name', label: 'Ingredient', sortable: true, class: 'text-center' },
        { key: 'price', label: 'Price', sortable: true, class: 'text-center' },
        { key: 'actions', label: 'Actions' }
      ],
      infoModal: {
        id: 'info-modal',
        title: '',
        content: ''
      },
      ingredientCreate: {
        name: '',
        price: 1
      },
      ingredientCreateValid: {
        state: null,
        message: ''
      }
    }
  },
  methods: {
    showDetail (obj) {
      this.$router.push({ name: 'pastry-id', params: { id: obj.item.id } })
    },
    showModal (obj, button, id) {
      this.infoModal.content = obj.item
      this.$root.$emit('bv::show::modal', id, button)
    },
    async createIngredient (e) {
      await this.$axios
        .$post(process.env.API_URL + 'ingredients/', this.ingredientCreate)
        .then((res) => {
          console.log(res)
          this.$store.commit('pastry/AppendIngredient', res)
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response)
            this.pastry_create_valid = {
              state: false,
              message: error.response.data.message
            }
            console.log(this.pastry_create_valid)
            // this.errors = [error.response.data.message]
          } else {
            console.log('Error', error.message)
          }
        })
    },
    async editIngredient (e, key, { id, name, price }) {
      if (key === 'name') {
        name = e
      } else {
        price = e
      }
      await this.$axios
        .$put(process.env.API_URL + 'ingredients/', {
          id, name, price
        }).then((res) => {
          this.$store.commit('pastry/UpdateIngredient', res)
        })
        .catch((error) => {
          if (error.response) {
            alert(error.message)
            this.$store.dispatch('pastry/GetIngredients')
            // this.errors = [error.response.data.message]
          } else {
            console.log('Error', error.message)
          }
        })
    },
    async deleteIngredient (e) {
      await this.$axios
        .$delete(process.env.API_URL + 'ingredients/', {
          data: {
            id: this.infoModal.content.id
          }
        })
        .then((res) => {
          this.$store.dispatch('pastry/GetIngredients')
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response)
            // this.errors = [error.response.data.message]
          } else {
            console.log('Error', error.message)
          }
        })
      e()
    }
  }
}
</script>

<style>
.main {
  display: flex;
  justify-content: space-between;
  margin: 10px 0;
}
.pastry_create {
  min-width: 250px;
}
</style>
