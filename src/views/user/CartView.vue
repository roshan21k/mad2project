<template>
  <div v-if="orderPlaced" class="container">
    <div class="center">
      <h1>Your Order has Been placed successfully!</h1>
      <h3>Redirecting to Home in {{ countDown }}</h3>
    </div>
  </div>
  <cart-details
    v-else-if="cartDetails.length > 0"
    :cartDetails="cartDetails"
    @order-placed="orderHasPlaced"
  />
  <div class="container" v-else><h1 class="center">No Items in Cart</h1></div>
</template>

<script>
import axios from "axios";
import CartDetails from "@/components/user/CartDetails.vue";
export default {
  name: "CartView",
  components: { CartDetails },
  data() {
    return {
      cartDetails: [],
      orderPlaced: false,
      countDown: 2,
    };
  },
  methods: {
    orderHasPlaced(id) {
      this.orderPlaced = true;
      const countDownInterval = setInterval(() => {
        this.countDown--;
        if (this.countDown === 0) {
          clearInterval(countDownInterval);
          this.$router.push("/");
        }
      }, 1000);
    },
    async getCartDetails() {
      try {
        const response = await axios.get("/user/cart");
        this.cartDetails = response.data.cart_details;
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.getCartDetails();
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 75px);
}
.center {
  text-align: center;
}
.center h1 {
  margin-bottom: 20px;
  color: Green;
}
</style>
