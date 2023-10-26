<template>
  <h1>Order Details for ID : {{ this.id }}</h1>
  <div class="invoice">
    <table>
      <thead>
        <tr>
          <th>Product Name</th>
          <th>Quantity</th>
          <th>Cost</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in orderDetails" :key="item.id">
          <td>{{ item.product_name }}</td>
          <td>{{ item.quantity }} {{ item.product_uom }}</td>
          <td>&#x20B9; {{ item.product_price * item.quantity }}</td>
        </tr>
        <tr class="total-row">
          <td class="total">Total</td>
          <td></td>
          <td class="total">&#x20B9; {{ totalCost }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "OrderdetailsView",
  data() {
    return {
      orderDetails: [],
    };
  },
  methods: {
    async getOrderDetails() {
      try {
        const response = await axios.get(`/user/order/${this.id}`);
        this.orderDetails = response.data.order_details;
      } catch (error) {
        console.log(error);
      }
    },
  },
  computed: {
    totalCost() {
      let total = 0;
      this.orderDetails.forEach((item) => {
        total += item.product_price * item.quantity;
      });
      return total;
    },
  },
  props: ["id"],
  created() {
    this.getOrderDetails();
  },
};
</script>

<style scoped>
h1 {
  margin: 30px;
  text-align: center;
}
table {
  margin-bottom: 50px;
  border: 1px solid black;
}
th {
  border-bottom: 1px solid black;
  padding: 15px;
}
td {
  padding: 10px 20px;
}
.total {
  font-weight: bold;
}
.total-row td {
  border-top: 1px solid black;
}
.invoice {
  display: flex;
  justify-content: center;
}
</style>
