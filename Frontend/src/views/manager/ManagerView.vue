<template>
  <h1>Welcome Store Manager</h1>
  <div class="container">
    <router-link class="router" :to="{ name: 'addCategory' }">
      <div class="request">
        <h1>Add Category</h1>
      </div>
    </router-link>
    <router-link class="router" :to="{ name: 'deleteCategory' }">
      <div class="request">
        <h1 class="">Delete Category</h1>
      </div>
    </router-link>
    <router-link class="router" :to="{ name: 'updateCategory' }">
      <div class="request">
        <h1 class="">Update Category</h1>
      </div>
    </router-link>
    <router-link class="router" :to="{ name: 'addProduct' }">
      <div class="request">
        <h1>Add Product</h1>
      </div>
    </router-link>
    <router-link class="router" :to="{ name: 'deleteProduct' }">
      <div class="request">
        <h1 class="">Delete Product</h1>
      </div>
    </router-link>
    <router-link class="router" :to="{ name: 'updateProduct' }">
      <div class="request">
        <h1 class="">Update Product</h1>
      </div>
    </router-link>
  </div>
</template>

<script>
import axios from "axios";
export default {
  methods: {
    async csvDownload() {
      try {
        const response = axios.get("/manager/export_product_csv");
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-evenly;
  flex-wrap: wrap;
}
.request {
  margin: 50px;
  padding: 15px;
  border: 1px solid black;
  border-radius: 75px;
  width: 300px;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  background-color: aliceblue;
}
.request:hover {
  background-color: lightblue;
}

h1 {
  text-align: center;
  margin: 50px 0px;
}
.router {
  text-decoration: none;
  color: black;
}
</style>
