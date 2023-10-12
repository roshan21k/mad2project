<template>
  <!-- <h1>{{ this.$store.state.isAuthenticated }}</h1>
  <h2>{{ this.$store.state.userRole }}</h2> -->
  <!-- <h2>Welcome User</h2> -->

  <filter-bar
    :options="filterOptions"
    :maxPrice="maxPrice"
    :minPrice="minPrice"
    @category-selected="filterCategories"
    @price-selected="filterPrice"
  />
  <div v-for="x in categories" :key="x.id">
    <h2 v-if="categoryid === 0">{{ x.name }}</h2>
    <h2 v-else-if="x.id === categoryid">{{ x.name }}</h2>
    <product-cards
      v-if="categoryid === 0"
      :product="x.products"
      :selectedPrice="price"
    />
    <product-cards
      v-else-if="x.id === categoryid"
      :product="x.products"
      :selectedPrice="price"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";
import ProductCards from "../../components/user/ProductCards.vue";
import FilterBar from "../../components/user/FilterBar.vue";
import axios from "axios";
export default {
  components: {
    ProductCards,
    FilterBar,
  },
  data() {
    return {
      categories: [],
      filterOptions: [],
      maxPrice: 0,
      minPrice: 0,
      categoryid: 0,
      price: 0,
    };
  },
  name: "HomeView",
  computed: {
    ...mapState(["isAuthenticated", "userRole"]),
  },
  methods: {
    filterCategories(id) {
      if (id == "") {
        this.categoryid = 0;
      } else {
        this.categoryid = id;
      }
    },
    filterPrice(price) {
      this.price = price;
    },
    async filters() {
      try {
        const response = await axios.get("user/filter");
        this.filterOptions = response.data.categories;
        this.maxPrice = response.data.max_price;
        this.minPrice = response.data.min_price;
      } catch (err) {
        console.log(err);
      }
    },
  },
  async created() {
    this.filters();
    try {
      const response = await axios.get("user/");
      this.categories = response.data.categories;
    } catch (err) {
      console.log(err);
    }
  },
};
</script>
<style scoped>
h2 {
  margin: 50px 0px 50px 0px;
  text-align: center;
  color: green;
  text-decoration: underline;
}
</style>
