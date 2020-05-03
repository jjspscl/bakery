<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">
        <b-button v-b-toggle.sidebar-backdrop variant="warning">
          <svg
            class="bi bi-list"
            width="1em"
            height="1em"
            viewBox="0 0 16 16"
            fill="currentColor"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill-rule="evenodd"
              d="M2.5 11.5A.5.5 0 013 11h10a.5.5 0 010 1H3a.5.5 0 01-.5-.5zm0-4A.5.5 0 013 7h10a.5.5 0 010 1H3a.5.5 0 01-.5-.5zm0-4A.5.5 0 013 3h10a.5.5 0 010 1H3a.5.5 0 01-.5-.5z"
              clip-rule="evenodd"
            />
          </svg> Bakery
        </b-button>
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse" />

      <b-collapse id="nav-collapse" is-nav>
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              <em>User</em>
            </template>
            <b-dropdown-item href="#">
              Profile
            </b-dropdown-item>
            <b-dropdown-item href="#">
              Sign Out
            </b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-sidebar
      id="sidebar-backdrop"
      title="Bakery"
      backdrop
      shadow
    >
      <hr>
      <div class="container-fluid">
        <b-nav vertical>
          <b-nav-item @click="$router.push({ name: 'index' })">
            Home
          </b-nav-item><hr>
          <b-nav-item @click="$router.push({ name: 'pastry'})">
            Pastry
          </b-nav-item><hr>
          <b-nav-item @click="$router.push({ name: 'ingredients'})">
            Ingredients
          </b-nav-item><hr>
        </b-nav>
      </div>
    </b-sidebar>
  </div>
  </div>
</template>

<script>
export default {}

</script>

<style scoped>
.col a {
  text-decoration: none;
}
</style>
