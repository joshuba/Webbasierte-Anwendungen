(function() {
  "use strict";
  const routes = [
    { path: "/", component: Vue.component("user-table") },
    { path: "/cart", component: Vue.component("cart") },
    { path: "/orders", component: Vue.component("order-table") },
    { path: "/products", component: Vue.component("product-table") },
    { path: "/login", component: Vue.component("login") },
    { path: "/register", component: Vue.component("registration") },
    {
      path: "/user/:id",
      name: "user",
      component: Vue.component("user-editor"),
      props: { isUpdate: true }
    },
    {
      path: "/view-user/:id",
      name: "view-user",
      component: Vue.component("user-page")
    },
    {
      path: "/order/:id",
      name: "view-order",
      component: Vue.component("order-page")
    },
    {
      path: "/product/:id",
      name: "view-product",
      component: Vue.component("product-page")
    },
    {
      path: "/confirm/:id",
      name: "close-order",
      component: Vue.component("wrap-up")
    },
    {
      path: "/search/:type",
      name: "search",
      component: Vue.component("search")
    }
  ];
  /** Initalisierung des Routers, mit den vorher definierten Komponenten */
  const router = new VueRouter({
    routes
  });

  router.beforeEach((to, from, next) => {
    let unprotected_routes = ["/login", "/register"];
    if (!api.isLoggedIn && unprotected_routes.indexOf(to.path) < 0) {
      // kein browsen ohne login
      next("/login");
    } else if (api.isLoggedIn && unprotected_routes.indexOf(to.path) > 0) {
      // kein login und keine registrierung wenn angemeldet
      next("/");
    } else {
      // ansonsten weiter browsen
      next();
    }
  });

  let cart = {
    addItem: function(product){
      api.put('/api/products', {
        type: 'remove',
        quantity: 1,
        id: product.id
      }, data => {
        if (data.status == 'success') {
          if (this.items[product.id]) {
            this.items[product.id].qty += 1
          } else {
            this.items[product.id] = product
            this.items[product.id].qty = 1
          }
        }
      }, error => {
        alert("There was an error adding your product")
        console.error(error)
      })
    },
    removeItem: function(product){
      api.put('/api/products', {
        type: 'add',
        quantity: product.qty,
        id: product.id
      }, data => {
        if (data.status == 'success') Vue.delete(this.items, product.id)
      }, error => {
        console.error(error)
      })
    },
    finishedOrder: function () {
      this.items = {}
    },
    clear: function(){
      console.log('clearing cart')
      for(let product in this.items){
        this.removeItem(this.items[product])
      }
    },
    getItems: function() {
      return this.items
    },
    items: {}
  }

  new Vue({
    created () {
      document.addEventListener('beforeunload', this.handler)
    },
    data() {
      return {
        api: api.state,
        cart: cart
      }
    },
    methods: {
      handler: function(event) {
        event.preventDefault()
        this.cart.clear()
        window.open('', '_self', '').close()
      }
    },
    el: "#vue-app",
    router: router,
    template: `
    <div id='vue-app'>
    <h2>Flask and Vue Boilerplate</h2>
    <navigation v-if='api.isLoggedIn'></navigation>
    <router-view></router-view>
    </div>`
  });
})();
