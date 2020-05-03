<template>
  <div class="container-fluid">
    <div class="main">
      <h1> Pastry </h1>
      <div class="pastry_create">
        <b-form @submit.prevent="create_pastry" inline>
          <b-form-input
            id="pastry_create"
            class="mb-2 mr-sm-2 mb-sm-0"
            placeholder="Pastry Name"
            v-model="pastry_create"
            input />
          <b-button
            class="mb-2 mr-sm-2 mb-sm-0"
            type="submit"
            variant="success"
            >Create Pastry</b-button>
        </b-form>
        <b-form-invalid-feedback v-if="!pastry_create_valid.state" :state="pastry_create_valid.state">
            {{ pastry_create_valid.message }}
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
      :items="pastries"
      :current-page="currentPage"
      :fields="fields"
      striped
      hover
    >
      <template v-slot:cell(actions)="row">
        <b-button
          @click="showDetail(row)"
          size="sm"
          variant="primary"
        >
          Details
        </b-button>
        <b-button
          @click="showModal(row, $event.target,'editModal')"
          size="sm"
          variant="success"
        >
          Edit
        </b-button>
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
      id="editModal"
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
            />
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
          <b-form @submit.prevent="deletePastry(hide)">
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
      perPage: 10,
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
      },
      pastry_create: '',
      pastry_create_valid: {
        state: null,
        message: ''
      }
    }
  },
  methods: {
    showDetail (obj) {
      this.$router.push({ name: 'pastry-id', params: { id: obj.item.id } })
    },
    async create_pastry () {
      await this.$axios
        .$post(process.env.API_URL + 'pastry/', {
          data: this.pastry_create
        }).then((res) => {
          this.$store.commit('pastry/AppendPastry', res)
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
    showModal (obj, button, id) {
      this.infoModal.content = obj.item
      this.$root.$emit('bv::show::modal', id, button)
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
    },
    async deletePastry (e) {
      await this.$axios
        .$delete(process.env.API_URL + 'pastry/', {
          data: {
            id: this.infoModal.content.id,
            name: this.form.pastry_name
          }
        })
        .then((res) => {
          this.$store.dispatch('pastry/GetPastries')
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
