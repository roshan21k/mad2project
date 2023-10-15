<template>
  <div class="card">
    <div class="product-card" v-for="x in filteredProduct" :key="x">
      <productcard-info :productItem="x" />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import ProductcardInfo from "./ProductcardInfo.vue";
export default {
  components: { ProductcardInfo },
  data() {
    return {
      msg: null,
    };
  },
  props: ["product", "selectedPrice"],
  methods: {
    async addToCart(id) {
      try {
        const response = await axios.post(`user/cart/${id}`);
        console.log(response.data.message);
        this.msg = response.data.message;
      } catch (err) {
        if (!err.response.data.error) {
          this.msg = err;
        } else {
          this.msg = err.response.data.error;
        }
        console.log(err);
      }
    },
  },
  computed: {
    filteredProduct() {
      if (!this.selectedPrice) {
        return this.product;
      } else {
        return this.product.filter((x) => x.price <= this.selectedPrice);
      }
    },
  },
};
</script>

<style scoped>
img {
  height: 250px;
  width: 250px;
}
.card {
  margin: 25px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-evenly;
}
.product-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 30px;
  background-color: #ffffff;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
}
.product-card * {
  padding: 10px 10px;
}
</style>
