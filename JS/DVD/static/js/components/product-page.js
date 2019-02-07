Vue.component("product-page", {
    data() {
        return {
            id: this.$route.params.id,
            product: {}
        };
    },
    mounted() {
        this.fetchData()
    },
    methods: {
        addToCart (product) {
            if (this.product.inventory.quan_in_stock - 1 > -1) {
                this.product.inventory.quan_in_stock -= 1
                this.$root.cart.addItem(product)
            }
        },
        fetchData() {
            /** api.get kommt aus api-client.js */
            const url = "/api/products/" + this.id
            api.get(url, data => {
                this.product = data.product;
            }, error => {
                console.error(error)
            })
        }
    },
    template: `
    <div class="product">
    <table>
    <tr>
    <td>Product ID</td>
    <td>{{ product.id }}</td>
    </tr>
    <tr>
    <td>Category</td>
    <td>{{ product.category }}</td>
    </tr>
    <tr>
    <td>Title</td>
    <td>{{ product.title }}</td>
    </tr>
    <tr>
    <td>Actor</td>
    <td>{{ product.actor }}</td>
    </tr>
    <tr>
    <tr>
    <td>Category</td>
    <td>{{ product.categorytitle }}</td>
    </tr>
    <tr>
    <td>Price</td>
    <td>{{ product.price }}$</td>
    </tr>
    <tr>
    <td>In Stock</td>
    <td>{{ product.inventory.quan_in_stock }}</td>
    </tr>
    <tr>
    <button @click="addToCart(product)">add to cart</button>
    </tr>
    </table>
    </div>
    `
});
