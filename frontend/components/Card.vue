<template lang="html">
  <div class="card">
    <slot />
  </div>
</template>

<script>
export default {

}
</script>

<style lang="css" scoped>
  .card{
    position: relative;
    z-index: 1;
    background: #FFFFFF;
    margin: 0 auto;
    box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
    margin: 15px;
    min-height: 50px;
    padding: 24px;
  }

</style>
