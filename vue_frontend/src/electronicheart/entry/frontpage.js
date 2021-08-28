// Ok, so obviously we need to import Vue itself to create a new Vue instance, which is the construct that eventually
// actually hooks into the special tag within the HTML of the site.
// Now as far as I understand the path from which we are importing here is the relative path within the node_modules
// folder. Because all of this is based on node and NPM is the package manager for these node modules which then
// installs them into this special folder once "npm install" is executed. But I also *think* that the import syntax
// here is not actually a main feature of JS. In the sense that you could not just write this into a plain JS file
// which the browser then interprets. I *think* this either needs to be compiled for the browser to be usable or it
// can be *interpreted* by the node interpreter on the server.
import Vue from "vue/dist/vue.js"

// Then we can import the components, which we want to use for this file. This path now actually is a file system
// path. Based on the location of *this* file it is the correct relative path to point to this component.
// import Frontpage from "../components/Frontpage";

// Ok this is strange syntax. From my understanding, the "=>" type syntax is the JS version of lambdas/anonymous
// functions. So I am guessing, that the constant variable here does not actually contain the frontpage component, but
// instead a function which will lazy import that component once it is called?
const Frontpage = () => import( /* webpackChunkName: "chunk-frontpage" */ "../components/Frontpage.vue");

Vue.config.productionTip = false

// Here we create a new Vue instance. This will then do the magic. It will hook into the elements specified with the
// ID #frontend within the html and then replace (?) it with the specified components.
new Vue({
    el: "#frontpage",
    components: {Frontpage}
})
