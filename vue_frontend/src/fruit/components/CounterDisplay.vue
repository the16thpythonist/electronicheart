<template>
  <div>
    <!-- Because our project css is loaded from our Django base template, we may use those inherited styles -->
    <div id="display" class="display-4 rounded-circle">{{ count }}</div>
    
  </div>
</template>

<script>
export default {
  name: 'CounterDisplay',
  props: {
    msg: String
  },
  computed: {
    count() { return this.$store.state.fruit.count }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  #display {
    background-color: #42b883;
    color: white;
    font-size: 4rem;
    font-weight: bold;
    line-height: 6rem;
    height: 6rem;
    width: 6rem;
    text-align: center;
    vertical-align: baseline;
}
</style>
