<template>
  <div class="container-fluid">
    <h1> Pastry </h1>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="my-table"
    />
    <b-table
      :per-page="3"
      :items="pastries"
      :current-page="currentPage"
      :fields="fields"
      striped
      hover
    >
      <template v-slot:cell(actions)="row">
        <b-button
          @click="editPastry(row.item, $event.target)"
          size="sm"
          variant="success"
        >
          Edit
        </b-button>
        <b-button
          @click="showDetail()"
          size="sm"
          variant="primary"
        >
          {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
        </b-button>
      </template>
    </b-table>
    <b-modal
      :id="infoModal.id"
      :title="infoModal.title"
      @hide="() => {
        this.infoModal.title = ''
        this.infoModal.content = ''
      }"
      hide-footer
    >
      <template v-slot:modal-title>
        Edit Pastry
      </template>
      <template v-slot:default="{ hide }">
        <div class="d-block text-center">
          <b-form @submit.prevent="submitPastry(hide)">
            <b-form-input
              id="input-1"
              v-model="form.pastry_name"
              :placeholder="infoModal.content.name"
              type="text"
              required
            /><br>
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
    store.dispatch('pastry/GetPastries')
  },
  computed: {
    ...mapState('pastry', {
      pastries: 'pastry'
    }),
    rows () {
      return this.pastries.length
    }
  },
  data () {
    return {
      perPage: 3,
      currentPage: 1,
      fields: [
        { key: 'id', label: 'ID', sortable: true, sortDirection: 'desc' },
        { key: 'name', label: 'Pastry', sortable: true, class: 'text-center' },
        { key: 'actions', label: 'Actions' }
      ],
      infoModal: {
        id: 'info-modal',
        title: '',
        content: ''
      },
      form: {
        pastry_name: ''
      }
    }
  },
  methods: {
    showDetail () {
      this.$router.push({ name: 'pastry-id', params: { id: 1 } })
    },
    editPastry (obj, button) {
      this.infoModal.content = obj
      this.$root.$emit('bv::show::modal', this.infoModal.id, button)
    },
    async submitPastry (e) {
      const data = await this.$axios
        .$put(process.env.API_URL + 'pastry/', {
          id: this.infoModal.content.id,
          name: this.form.pastry_name
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response)
            // this.errors = [error.response.data.message]
          } else {
            console.log('Error', error.message)
          }
        })
      await this.$store.commit('pastry/UpdatePastry', data)
      e()
    }
  }
}
</script>

<style>
</style>
