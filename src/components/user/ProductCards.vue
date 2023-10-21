<template>
  <div class="card" v-if="filteredProduct.length > 0">
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
    return {};
  },
  props: ["product", "selectedPrice", "searchName"],
  methods: {
    async addToCart(id) {
      try {
        const response = await axios.post(`user/cart/${id}`);
        this.msg = response.data.message;
      } catch (error) {
        console.log(error);
      }
    },
  },
  computed: {
    filteredProduct() {
      let filteredProducts = this.product;
      if (this.selectedPrice) {
        filteredProducts = this.product.filter(
          (x) => x.price <= this.selectedPrice
        );
      }
      if (this.searchName) {
        filteredProducts = this.product.filter((x) =>
          x.name.toLowerCase().includes(this.searchName.toLowerCase())
        );
      }
      return filteredProducts;
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
.center {
  text-align: center;
}
</style>
