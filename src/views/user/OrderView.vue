<template>
  <h1>Your Orders</h1>
  <div v-if="orders.length > 0" class="orders">
    <div v-for="order in orders" :key="order.id" class="order">
      <div class="order-details">
        <p><span class="bold">Order Id : </span> {{ order.id }}</p>
        <p>
          <span class="bold">Order on :</span>
          {{ order.ordered_on.substring(0, 10) }} at
          {{ order.ordered_on.substring(10) }}
        </p>
        <p>
          <span class="bold"> Total Amount: </span>&#x20B9; {{ order.total }}
        </p>
        <router-link :to="'/order/' + order.id">
          <button>View Details</button>
        </router-link>
      </div>
    </div>
  </div>
  <div v-else class="container">
    <h1>No Orders To Show</h1>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "OrderView",
  data() {
    return {
      orders: [],
    };
  },

  methods: {
    async getOrderDetails() {
      try {
        const response = await axios.get("/user/orders");
        this.orders = response.data.order_details;
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.getOrderDetails();
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(75vh - 75px);
}
.orders {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin: 50px;
}

.order {
  display: flex;
  flex-direction: column;
  margin: 25px;
  padding: 25px;
  border: 1px solid black;
}
.order-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.bold {
  font-weight: bold;
}
h1 {
  margin: 25px;
  text-align: center;
}
button {
  height: 30px;
}
</style>
