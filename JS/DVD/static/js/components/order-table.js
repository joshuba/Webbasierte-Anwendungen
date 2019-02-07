Vue.component("order-table", {
  data() {
    return {
      orders: null,
      currentPage: 1,
      perPage: 20,
      lastPage: 0,
      isSearch: false,
      search: ''
    };
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    deleteOrder (orderId) {
      /** api.del kommt aus api-client.js */
      api.del(`/api/orders/${orderId}`, data => {
        this.fetchData()
      })
    },
    searchFor () {
      const url = "/api/orders?s=" + this.search
      this.isSearch = true
      api.get(url, data => {
        this.orders = data.orders
      }, error => {
        console.error(error)
      })
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
      const url = "/api/orders/" + this.currentPage + '/' + this.perPage
      api.get(url, data => {
        this.orders = data.orders
        this.lastPage = data.numpages
      }, error => {
        console.error(error)
      })
    }
  },
  template: `
  <table class="order-table">
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
  <span>Orders per Page</span>
  <input type="text" v-model="perPage" size="2"/>
  </form>
  </td>
  <td colspan="2">
  <a @click.prevent="switchPage(1)">⏪</a>
  <a @click.prevent="switchPage('-')">◀️</a>
  <span>Seite {{ currentPage }} von {{ lastPage }}</span>
  <a @click.prevent="switchPage('+')">▶️</a>
  <a @click.prevent="switchPage(lastPage)">⏩</a>
  </td>
  </tr>
  <tr>
  <th>Order-ID</th>
  <th>by User</th>
  <th>Amount</th>
  <th colspan="2">Tools</th>
  </tr>
  <tr v-for='order in orders'>
  <td>{{order.id}}</td>
  <td>{{order.customerid}}</td>
  <td class="price">{{order.totalamount.toFixed(2)}}$</td>
  <td><router-link :to="{name: 'view-order', params: {id: order.id}}" tag="button">view</router-link></td>
  <td><button type="button" @click="deleteOrder(order.id)">delete</button></td>
  </tr>
  </table>
  `
});
