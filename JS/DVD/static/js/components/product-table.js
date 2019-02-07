Vue.component("product-table", {
  data() {
    return {
      products: null,
      currentPage: 1,
      perPage: 20,
      lastPage: 0,
      isSearch: false,
      search: '',
      sortParam: ""
    };
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    searchFor () {
      let url = "/api/products?s=" + this.search
      if (this.sortParam) url += '&sort=' + this.sortParam
      this.isSearch = true
      api.get(url, data => {
        this.products = data.products
        this.lastPage = data.numpages
      }, error => {
        console.error(error)
      })
    },
    sort(param) {
      this.sortParam = param
      if (this.isSearch) {
        this.searchFor()
      } else {
        this.fetchData()
      }
    },
    clearSearch () {
      this.isSearch = false
      this.fetchData()
    },
    updatePerPage () {
      this.ordersPerPage = this.perPage
      this.fetchData()
    },
    switchPage (arg) {
      if (arg == '+' && (this.currentPage + 1) <= this.lastPage){
        this.currentPage +=1
        this.fetchData()
      } else if(arg ==='-' && (this.currentPage -1) > 0){
        this.currentPage -= 1
        this.fetchData()
      } else if (!isNaN(parseInt(arg)) && arg <= this.lastPage && arg > 0) {
        this.currentPage = arg
        this.fetchData()
      }
    },
    fetchData () {
      /** api.get kommt aus api-client.js */
      let url = "/api/products/" + this.currentPage + '/' + this.perPage
      if (this.sortParam) url += '?sort=' + this.sortParam
      api.get(url, data => {
        this.products = data.products;
        this.lastPage = data.numpages
      }, error => {
        console.error(error)
      })
    },
    addToCart (product) {
      if (product.inventory.quan_in_stock - 1 > -1){
        product.inventory.quan_in_stock -= 1
        this.$root.cart.addItem(product)
      }
    }
  },
  template: `
  <table class="product-table">
   <tr>
  <td>
  <form @submit.prevent="searchFor">
  <label for="search">Search</label>
  <input type="text" id="search" v-if="!isSearch" name ="search" v-model="search">
  <a v-if="isSearch" @click.prevent="clearSearch">❌  zurücksetzen</a>
  </form>
  </td>
  <td>
  <form @submit="updatePerPage">
  <span>Products per Page</span>
  <input type="text" v-model="perPage" size="2"/>
  </form>
  </td>
  <td colspan="3">
  <a @click.prevent="switchPage(1)">⏪</a>
  <a @click.prevent="switchPage('-')">◀️</a>
  <span>Seite {{ currentPage }} von {{ lastPage }}</span>
  <a @click.prevent="switchPage('+')">▶️</a>
  <a @click.prevent="switchPage(lastPage)">⏩</a>
  </td>
  </tr>
  <tr>
  <th>Title <span @click="sort('title')">⯆</span> <span @click="sort('title_desc')">⯅</span></th>
  <th>Category <span @click="sort('category')">⯆</span> <span @click="sort('category_desc')">⯅</span></th>
  <th>In Stock</th>
  <th>Price <span @click="sort('price')">⯆</span> <span @click="sort('price_desc')">⯅</span></th>
  <th colspan="2">Tools</th>
  </tr>
  <tr v-for='product in products'>
  <td>{{product.title}}</td>
  <td>{{product.categorytitle}}</td>
  <td>{{product.inventory.quan_in_stock}}</td>
  <td class="price">{{product.price}}$</td>
  <td><router-link :to="{name: 'view-product', params: {id: product.id}}" tag="button">view</router-link></td>
  <td><button type="button" @click="addToCart(product)">add to cart</button></td>
  </tr>
  </table>
  `
});
