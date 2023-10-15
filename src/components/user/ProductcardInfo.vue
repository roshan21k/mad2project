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
  <p>Stock Left : {{ productItem.stock }} {{ productItem.uom }}</p>
  <div class="button">
    <button
      :disabled="addingToCart || soldOut"
      @click="addToCart(productItem.id)"
      :class="{ 'sold-out': this.soldOut }"
    >
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
      addingToCart: false,
      ratings: this.productItem.ratings_average,
      soldOut: this.productItem.stock === 0,
    };
  },
  props: {
    productItem: {},
  },
  methods: {
    async addToCart(id) {
      try {
        const response = await axios.post(`user/cart/${id}`);
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
        this.addingToCart = false;
      }, 3000);
    },
  },
  computed: {
    cartText() {
      if (this.soldOut) {
        return "SoldOut!";
      } else if (this.addingToCart) {
        return "Added ✅";
      } else {
        return "Add To Cart";
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
.sold-out {
  background-color: rgb(255, 75, 75);
}
</style>
