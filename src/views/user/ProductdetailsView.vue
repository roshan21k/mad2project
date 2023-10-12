<template>
  <h1 v-if="productDetail" class="heading">
    Product details for {{ this.productDetail.name }}
  </h1>

  <div v-if="productDetail" class="product">
    <div>
      <img
        :src="`https://source.unsplash.com/random/900×700/?${productDetail.name.toLowerCase()}`"
      />
    </div>
    <div class="details">
      <p><span class="title">Product id: </span> {{ productDetail.id }}</p>
      <p><span class="title">Product Name: </span> {{ productDetail.name }}</p>
      <p>
        <span class="title">Product price: </span> &#x20B9;
        {{ productDetail.price }}
      </p>
      <p><span class="title">Product Category: </span> {{ category }}</p>
      <p>
        <span class="title"
          >Ratings:
          <star-rating
            v-model:rating="productDetail.ratings_average"
            :increment="0.1"
            :star-size="25"
            :read-only="true"
            :round-start-rating="true"
            :show-rating="true"
        /></span>
      </p>
      <p class="max">
        <span class="title">Product description:</span>
        {{ productDetail.description }}
      </p>
      <div class="button">
        <button :disabled="addingToCart" @click="addToCart(productDetail.id)">
          {{ cartText }}
        </button>
      </div>
    </div>
  </div>
  <h1 class="heading">Write a Review</h1>
  <div class="reviews">
    <div class="star-rating">
      <star-rating
        v-model:rating="ratings"
        :increment="0.5"
        :round-start-rating="true"
        :show-rating="true"
      ></star-rating>
    </div>
    <p v-if="err" class="error">{{ err }}</p>
    <textarea
      class="comment-textarea"
      placeholder="Add your comment..."
      v-model="comment"
    ></textarea>
    <div class="comment">
      <button @click="handleComment">Submit</button>
    </div>
    <review-details
      v-if="reviewDetails.length > 0"
      :reviewDetails="reviewDetails"
    />
  </div>
</template>

<script>
import axios from "axios";
import StarRating from "vue-star-rating";
import ReviewDetails from "@/components/user/ReviewDetails.vue";
export default {
  name: "ProductdetailsView",
  components: { StarRating, ReviewDetails },
  data() {
    return {
      cartText: "Add to cart",
      addingToCart: false,
      productDetail: null,
      category: null,
      ratings: 5,
      comment: "",
      err: "",
      reviewDetails: [],
    };
  },
  props: ["id"],
  methods: {
    async getProductDetails() {
      try {
        const response = await axios.get(`user/product/${this.id}`);
        this.productDetail = response.data.product_details;
        this.category = response.data.category;
      } catch (error) {
        console.log(error);
      }
    },
    async addToCart(id) {
      try {
        const response = await axios.post(`user/cart/${id}`);
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
    async getReviews() {
      try {
        const response = await axios.get(`user/product/${this.id}/reviews`);
        this.reviewDetails = response.data.review_details;
      } catch (error) {
        console.log(error);
      }
    },
    setClearMessageTimeout() {
      setTimeout(() => {
        this.cartText = "Add To Cart";
        this.addingToCart = false;
        this.err = null;
      }, 3000);
    },
    async handleComment() {
      if (this.comment.trim().length > 10 && this.comment.length <= 250) {
        try {
          const response = await axios.post(`user/product/${this.id}/comment`, {
            comment: this.comment,
            rating: this.ratings,
          });
          this.getProductDetails();
          this.getReviews();
        } catch (error) {
          this.err = error.response.data.error;
          this.setClearMessageTimeout();
          console.log(error);
        }
      } else {
        this.err =
          "Make sure your comment is atleast 10 character long and less than 250 characters";
        this.setClearMessageTimeout();
      }
    },
    checkComment() {},
  },
  created() {
    this.getProductDetails();
    this.getReviews();
  },
};
</script>

<style scoped>
img {
  width: 500px;
  height: 500px;
}
.heading {
  text-align: center;
  margin: 50px;
}
.product {
  display: flex;
  justify-content: center;
  gap: 100px;
  flex-wrap: wrap;
}
.max {
  width: 400px;
  line-height: 1.5;
}
.details * {
  padding: 10px;
}
.title {
  padding: 0;
  margin: 0;
  font-weight: bold;
}
button[disabled] {
  color: black;
  cursor: not-allowed;
}
.ratings {
  font-weight: bold;
  color: orange;
}
.reviews {
  margin: 50px;
}
textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
}
.star-rating {
  margin-bottom: 10px;
}
.comment {
  display: flex;
  justify-content: center;
}
.comment button {
  margin: 25px;
  height: 40px;
  width: 75px;
}
.error {
  margin: 25px 0px;
  color: red;
  text-align: center;
}
</style>
