Vue.component("order-page", {
    data() {
        return {
            id: this.$route.params.id,
            order: {},
            products: []
        };
    },
    mounted() {
        this.fetchData()
    },
    methods: {
        fetchData() {
            /** api.get kommt aus api-client.js */
            const url = "/api/orders/" + this.id
            api.get(url, data => {
                this.order = data.order;
            }, error => {
                console.error(error)
            })
        }
    },
    template: `
    <div class="order">
    <table>
    <tr>
    <td>Order-ID</td>
    <td>{{ order.id }}</td>
    </tr>
    <tr>
    <td>Date</td>
    <td>{{ order.orderdate }}</td>
    </tr>
    <tr>
    <td>by Customer</td>
    <td><span>{{ order.customerid }}</span> <router-link :to="{name: 'view-user', params: {id: order.customerid}}" tag="button" style="display:inline-block; width: auto;">view</router-link></td>
    </tr>
    </table>
    <h2>Items</h2>
    <table class="items">
    <thead>
    <td>Title</td>
    <td>Price</td>
    <td>Qty</td>
    <td>Actions</td>
    </thead>
    <tr v-for="position in order.positions">
    <td>{{ position.product.title }}</td>
    <td class="price">{{ position.product.price }}$</td>
    <td>x{{ position.quantity }}</td>
    <td><router-link :to="{name: 'view-product', params: {id: position.product.id}}" tag="button">view</router-link></td>
    </tr>
    <tr>
    <td>Net. Amount</td>
    <td class="price">{{ order.netamount.toFixed(2) }}$</td>
    </tr>
    <tr>
    <td>Tax</td>
    <td class="price">{{ order.tax.toFixed(2) }}$</td>
    </tr>
    <tr>
    <td>Total</td>
    <td class="price">{{ order.totalamount.toFixed(2) }}$</td>
    </tr>
    </table>
    </div>
    `
});
