<template>
  <router-link
    :to="'/product/' + productItem.id"
    class="name"
    :productItem="productItem"
  >
    <img
      :src="`https://source.unsplash.com/random/900×700/?${productItem.name.toLowerCase()}`"
    />
    <h2>{{ productItem.name }}</h2>
  </router-link>
  <p>Price: {{ productItem.price }} per {{ productItem.uom }}</p>
  <star-rating
    v-model:rating="ratings"
    :increment="0.1"
    :star-size="25"
    :read-only="true"
    :round-start-rating="true"
    :show-rating="true"
  />
  <div class="button">
    <button :disabled="addingToCart" @click="addToCart(productItem.id)">
      {{ cartText }}
    </button>
  </div>
</template>

<script>
import axios from "axios";
import StarRating from "vue-star-rating";
export default {
  components: { StarRating },
  data() {
    return {
      cartText: "Add to cart",
      addingToCart: false,
      ratings: this.productItem.ratings_average,
    };
  },
  props: {
    productItem: {},
  },
  methods: {
    async addToCart(id) {
      try {
        const response = await axios.post(`user/cart/${id}`);
        console.log(response.data.message);
        this.cartText = "Added ✅";
        this.addingToCart = true;

        this.setClearMessageTimeout();
      } catch (err) {
        if (!err?.response?.data?.error) {
          this.setClearMessageTimeout();
        } else {
          this.setClearMessageTimeout();
        }
      }
    },
    setClearMessageTimeout() {
      setTimeout(() => {
        this.cartText = "Add To Cart";
        this.addingToCart = false;
      }, 3000);
    },
  },
};
</script>

<style scoped>
img {
  height: 250px;
  width: 250px;
}
.product-card * {
  padding: 10px 10px;
}
.button {
  display: flex;
  justify-content: center;
}
.message {
  word-wrap: break-word;
}
button[disabled] {
  color: black;
  cursor: not-allowed;
}
.ratings {
  font-weight: bold;
  color: orange;
}
.name {
  text-decoration: none;
  color: black;
  padding: 0;
}
</style>
