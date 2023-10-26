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
  <div class="invoice-button">
    <button @click="getOrderInvoice(this.id)">E-mail Invoice</button>
    <p v-if="success">{{ success }}</p>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "OrderdetailsView",
  data() {
    return {
      orderDetails: [],
      success: "",
      error: "",
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
    async getOrderInvoice(id) {
      try {
        const response = await axios.get(`/mail/send_orders/${id}`);
        this.success = "Your Invoice has been Sent via e-mail";
        this.setMessageTimeout();
      } catch (error) {
        console.log(error);
        this.error = "Error in sending invoice";
        this.setMessageTimeout();
      }
    },
    setMessageTimeout() {
      setTimeout(() => {
        this.success = "";
        this.error = "";
      }, 4000);
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
.invoice-button {
  display: block;
  text-align: center;
}
button {
  padding: 10px;
}
p {
  margin: 20px;
}
</style>
