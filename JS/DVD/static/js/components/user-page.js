Vue.component("user-page", {
    data() {
        return {
            id: this.$route.params.id,
            orders: [],
            user: {}
        };
    },
    mounted() {
        this.fetchData()
    },
    methods: {
        fetchData() {
            /** api.get kommt aus api-client.js */
            const url = "/api/users/" + this.id
            const orderurl = "/api/orders/c/" + this.id
            api.get(url, data => {
                this.user = data.user;
            }, error => {
                console.error(error)
            })
            api.get(orderurl, data => {
                this.orders = data.orders;
            }, error => {
                console.error(error)
            })
        }
    },
    template: `
    <div class="user-table">
    <div class="user">
    <table>
    <tr>
    <td>Name</td>
    <td>{{user.firstname}} {{user.lastname}}</td>
    </tr>
    <tr>
    <td>UserName</td>
    <td>{{user.username}}</td>
    </tr>
    <tr>
    <td>Address</td>
    <td>{{user.address1}}</td>
    </tr>
    <tr v-if="user.address2">
    <td></td>
    <td>{{user.address2}}</td>
    </tr>
    <tr>
    <td></td>
    <td>{{user.zip}} {{user.city}}, {{user.state}}</td>
    </tr>
    <tr>
    <td></td>
    <td>{{user.country}}</td>
    </tr>
    <tr>
    <td>Phone</td>
    <td>{{user.phone}}</td>
    </tr>
    <tr>
    <td>Email</td>
    <td>{{user.email}}</td>
    </tr>
    </table>
    </br>
    <h2>Orders</h2>
    <table class="orders">
    <thead>
    <td>Order-ID</td>
    <td>Total</td>
    </thead>
    <tr v-for="order in orders">
    <td>{{ order.id }}</td>
    <td>{{ order.totalamount }}</td>
    <td>
    <router-link :to="{name: 'view-order', params: {id: order.id}}" tag="button">view</router-link>
    </td>
    </tr>
    </table>
    </div>
    </div>
    `
});
