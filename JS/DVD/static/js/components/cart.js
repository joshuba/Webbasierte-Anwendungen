Vue.component("cart", {
	computed: {
		total () {
			let price = 0
			Object.values(this.$root.cart.items).forEach(function(item) {
				price += item.price * item.qty
			})
			return price.toFixed(2)
		},
		products () {
			return this.$root.cart.items()
		}
	},
	methods: {
		removeFromCart(product) {
			this.$root.cart.removeItem(product)
		},
		placeOrder () {
			let ordJSON = {
				"username": api.state.username,
				"items": Object.values(this.$root.cart.items),
				"total": this.total
			}
			api.post('/api/orders', ordJSON, data => {
				if(data.status == 'success'){
					this.$router.push({
						name: 'close-order',
						params: {
							id: data.orderid,
							products: this.$root.cart.items,
							total: this.total
						}
					})
				}
			}, error => {
				console.error(error)
			} )
		}
	},
    template: `
    <div>
	<table class="cart-table" v-if="Object.keys(this.$root.cart.items).length > 0">
	<thead>
	<td>Title</td>
	<td>Qty</td>
	<td>Price(p.P.)</td>
	</thead>
    <tr v-for="product in this.$root.cart.items">
    <td>{{ product.title }}</td>
    <td>x{{product.qty}}</td>
	<td class="price">{{product.price}}$</td>
	<td><button @click="removeFromCart(product)">remove</button></td>
    </tr>
    <tr>
    <td>Total</td>
    <td></td>
	<td class="price">{{ total }}$</td>
	</tr>
	<tr>
	<form @submit.prevent="placeOrder()">
	<input type="submit" value="Place Order" />
	</form>
	</tr>
	</table>
    <span v-else>Der Warenkorb ist leer.</span>
    </div>
    `
});
