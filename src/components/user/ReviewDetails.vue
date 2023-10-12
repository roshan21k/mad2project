<template>
  <h1 class="center">Top Reviews</h1>
  <div class="review">
    <div v-for="review in reviewDetails" :key="review.id" class="review-detail">
      <h2>Review By {{ review.username }}</h2>
      <star-rating
        v-model:rating="review.rating"
        :increment="0.1"
        :star-size="25"
        :read-only="true"
        :round-start-rating="true"
        :show-rating="true"
      />
      <p>{{ review.comment }}</p>
    </div>
  </div>
</template>

<script>
import StarRating from "vue-star-rating";
export default {
  name: "ReviewDetails",
  components: { StarRating },
  props: ["reviewDetails"],
};
</script>

<style scoped>
.review {
  display: flex;
  gap: 50px;
  justify-content: space-evenly;
  flex-wrap: wrap;
  margin: 25px;
}
.review-detail {
  border: 1px solid black;
  padding: 25px;
}
.review-detail * {
  padding: 10px;
  width: 300px;
}
.center {
  margin: 50px 0px;
  text-align: center;
}
</style>
