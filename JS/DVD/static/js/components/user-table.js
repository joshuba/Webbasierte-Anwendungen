Vue.component("user-table", {
  data() {
    return {
      users: null,
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
    deleteUser (userId) {
      /** api.del kommt aus api-client.js */
      api.del(`/api/users/${userId}`, data => {
        this.fetchData()
      })
    },
    sort (param) {
        this.sortParam = param
        if (this.isSearch) {
          this.searchFor()
        } else {
          this.fetchData()
        }
    },
    searchFor () {
      let url = "/api/users?s=" + this.search
      if (this.sortParam) url += '&sort=' + this.sortParam
      this.isSearch = true
      api.get(url, data => {
        this.users = data.users
      }, error => {
        console.error(error)
      })
    },
    clearSearch () {
      this.isSearch = false
      this.fetchData()
    },
    updatePerPage () {
      this.usersPerPage = this.perPage
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
      let url = "/api/users/" + this.currentPage + '/' + this.perPage
      if (this.sortParam) url += '?sort=' + this.sortParam
      api.get(url, data => {
        this.users = data.users;
        this.lastPage = data.numpages
      }, error => {
        console.error(error)
      })
    }
  },
  template: `
  <table class="user-table">
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
  <span>Users per Page</span>
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
  <th>Username <span @click="sort('username')">⯆</span> <span @click="sort('username_desc')">⯅</span></th>
  <th>E-Mail <span @click="sort('email')">⯆</span> <span @click="sort('email_desc')">⯅</span></th>
  <th colspan="3">Tools</th>
  </tr>
  <tr v-for='user in users'>
  <td>{{user.username}}</td>
  <td>{{user.email}}</td>
  <td><router-link :to="{name: 'user', params: {id: user.id}}" tag="button">edit</router-link></td>
  <td><router-link :to="{name: 'view-user', params: {id: user.id}}" tag="button">view</router-link></td>
  <td><button type="button" @click="deleteUser(user.id)">delete</button></td>
  </tr>
  </table>
  `
});
