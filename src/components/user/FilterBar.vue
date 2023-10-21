<template>
  <div class="filters">
    <div>
      <h3>Filter By:</h3>
    </div>
    <div>
      <div class="filter-group">
        <div>
          <label>Search :</label>
          <input type="text" v-model="search" @input="handleSearch" />
        </div>

        <div>
          <label for="category">Category :</label>
          <select v-model="selectedCategory" @change="handleCategoryChange">
            <option value="">All Categories</option>
            <option
              v-for="option in options"
              :key="option.id"
              :value="option.id"
            >
              {{ option.name }}
            </option>
          </select>
        </div>
        <div>
          <label for="price">Price : </label>
          <input
            type="range"
            :min="minPrice"
            :max="maxPrice"
            v-model="selectedPriceRange"
            @change="handlePriceChange"
          />
          <div>
            <p>{{ selectedPriceRange }} Rs</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FilterBar",
  data() {
    return {
      selectedCategory: "",
      selectedPriceRange: this.maxPrice,
      search: "",
    };
  },
  props: ["options", "maxPrice", "minPrice"],

  methods: {
    handleSearch() {
      this.$emit("name-search", this.search);
    },
    handleCategoryChange() {
      this.$emit("category-selected", this.selectedCategory);
    },
    handlePriceChange() {
      //   console.log(this.selectedPriceRange);
      this.$emit("price-selected", this.selectedPriceRange);
    },
  },
  watch: {
    maxPrice(newMaxPrice) {
      this.selectedPriceRange = newMaxPrice;
    },
  },
};
</script>

<style scoped>
.filters {
  display: flex;
  justify-content: space-around;
  margin: 25px 100px;
  border: 1px solid black;
  gap: 25px;
  padding: 25px 0px;
  flex-wrap: wrap;
}
.filter-group {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 50px;
  justify-content: space-evenly;
}
/* .price-range {
  display: flex;
  gap: 20px;
} */
</style>
