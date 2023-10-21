<template>
  <h3 class="error" v-if="err">{{ err }}</h3>
  <div class="error" v-if="insufficient">
    <p v-for="item in insufficient" :key="item">
      Name : {{ item.product_name }} | requested: {{ item.requested }} |
      available: {{ item.available }}
    </p>
  </div>
  <div class="cart">
    <div>
      <div class="cart-details" v-for="item in cartDetails" :key="item.id">
        <img
          :src="`https://source.unsplash.com/random/900×700/?${item.product.name.toLowerCase()}`"
        />
        <div class="cart-info">
          <div>
            <p>
              <span :style="{ 'font-weight': 'bold' }"> Name : </span>
              {{ item.product.name }}
            </p>
          </div>

          <p>
            <span :style="{ 'font-weight': 'bold' }"> Product Price : </span>
            {{ item.product.price }} per {{ item.product.uom }}
          </p>
          <p>
            <span :style="{ 'font-weight': 'bold' }"> Added on : </span
            >{{ item.added_on }}
          </p>
          <div class="quantity">
            <button @click="incrementCartItem(item.id)">➕</button>
            <p>{{ item.quantity }}</p>
            <button @click="decrementCartItem(item.id)">➖</button>
          </div>
          <p>
            <span :style="{ 'font-weight': 'bold' }"> Ratings : </span
            ><star-rating
              v-model:rating="item.product.ratings_average"
              :increment="0.1"
              :star-size="25"
              :read-only="true"
              :round-start-rating="true"
              :show-rating="true"
            />
          </p>
          <button class="remove" @click="removeCartItem(item.id)">
            Remove
          </button>
        </div>
      </div>
    </div>
    <div>
      <h2 :style="{ 'text-align': 'center', 'margin-bottom': '25px' }">
        Sub-Total
      </h2>
      <table>
        <thead>
          <tr>
            <th>Product Name</th>
            <th>Quantity</th>
            <th>Cost</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cartDetails" :key="item.id">
            <td>{{ item.product.name }}</td>
            <td>{{ item.quantity }} {{ item.product.uom }}</td>
            <td>&#x20B9; {{ item.product.price * item.quantity }}</td>
          </tr>
          <tr class="total-row">
            <td class="total">Total</td>
            <td></td>
            <td class="total">&#x20B9; {{ totalCost }}</td>
          </tr>
        </tbody>
      </table>
      <div class="order">
        <button @click="handleCheckOut">Check Out</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import StarRating from "vue-star-rating";
export default {
  components: { StarRating },
  name: "CartDetails",
  data() {
    return {
      err: "",
      insufficient: "",
    };
  },
  props: ["cartDetails"],
  emits: ["order-placed"],
  methods: {
    async incrementCartItem(id) {
      try {
        const response = await axios.patch(`/user/cart/${id}/increment`);
        const updateItem = this.cartDetails.find((item) => item.id === id);
        if (updateItem) {
          updateItem.quantity = response.data.cart_count;
        }
      } catch (error) {
        if (error?.response?.data?.error) {
          this.err = error.response.data.error;
          setErrorTimeout();
        } else {
          this.err = err;
          setErrorTimeout();
        }
      }
    },
    async decrementCartItem(id) {
      try {
        const response = await axios.patch(`/user/cart/${id}/decrement`);
        const updateItem = this.cartDetails.find((item) => item.id === id);
        if (updateItem) {
          updateItem.quantity = response.data.cart_count;
        }
      } catch (error) {
        if (error?.response?.data?.error) {
          this.err = error.response.data.error;
          this.setErrorTimeout();
        } else {
          this.err = err;
          this.setErrorTimeout();
        }
      }
    },
    async removeCartItem(id) {
      try {
        const response = await axios.delete(`/user/cart/${id}/remove`);
        const deleteItem = this.cartDetails.findIndex((item) => item.id === id);
        if (deleteItem !== -1) {
          this.cartDetails.splice(deleteItem, 1);
        }
      } catch (error) {
        if (error?.response?.data?.error) {
          this.err = error.response.data.error;
          this.setErrorTimeout();
        } else {
          this.err = err;
          this.setErrorTimeout();
        }
      }
    },
    async handleCheckOut() {
      if (this.cartDetails.length !== 0) {
        try {
          const response = await axios.post("/user/place_order");
          this.$emit("order-placed", response.data.order_id);
        } catch (error) {
          if (error?.response?.data?.error) {
            this.err = error.response.data.error;
            this.insufficient = error.response.data.items;
            this.setErrorTimeout();
          } else {
            this.err = err;
            this.setErrorTimeout();
          }
        }
      }
    },
    setErrorTimeout() {
      setTimeout(() => {
        this.err = null;
      }, 3000);
    },
  },
  computed: {
    totalCost() {
      let total = 0;
      for (const i of this.cartDetails) {
        total += i.product.price * i.quantity;
      }
      return total;
    },
  },
};
</script>

<style scoped>
.cart {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: center;
  margin-top: 50px;
  gap: 50px;
}
img {
  height: 200px;
  width: 200px;
}
.cart-details {
  display: flex;
  margin: 25px;
  padding: 25px;
  justify-content: space-around;
  border: 1px solid black;
}
.cart-info {
  display: flex;
  padding: 0px 25px;
  flex-direction: column;
  justify-content: space-around;
  align-items: flex-start;
}
.quantity {
  display: flex;
  flex-direction: row;
  gap: 30px;
}
.quantity button {
  height: 25px;
  width: 25px;
}
.error {
  color: red;
  text-align: center;
}
.remove {
  padding: 5px;
}
table {
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
.order {
  display: flex;
  margin-top: 20px;
  justify-content: center;
}
.order button {
  height: 50px;
  width: 100px;
  background-color: lightgreen;
}
.order button:hover {
  background-color: #7bcf7b;
}
.ratings {
  font-weight: bold;
  color: orange;
}
</style>
