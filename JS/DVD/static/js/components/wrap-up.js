Vue.component("wrap-up", {
    mounted() {
        this.$root.cart.finishedOrder()
    },
    template: `
	<div>
	<h2>Your Order is being processed.</h2>
	<table class="cart-table">
	<thead>
	<td>Title</td>
	<td>Qty</td>
	<td>Price(p.P.)</td>
	</thead>
    <tr v-for="product in this.$route.params.products">
    <td>{{ product.title }}</td>
    <td>x{{product.qty}}</td>
    <td class="price">{{product.price}}$</td>
    </tr>
    <tr>
    <td>Total</td>
    <td></td>
    <td class="price">{{ this.$route.params.total }}$</td>
    </tr>
    </table>
    </div>
    `
});
