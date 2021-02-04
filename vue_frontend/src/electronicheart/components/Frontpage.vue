<template>
    <div id="frontpage">
        <p>HELLO FRONTPAGE</p>
    </div>
</template>

<script>
    export default {
        name: 'Frontpage',
        data () {
            return {
                staticRoot: process.env.VUE_APP_STATIC_ROOT
            }
        }
    }
</script>

<style scoped lang="scss">
    #frontpage {
        width: 200px;
        height: 200px;
        background-color: #42b883;
    }
</style>
