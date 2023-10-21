<template>
  <h1 class="center">Welcome Store Manager</h1>
  <div class="container">
    <div class="request" @click="productCsv">
      <h1>Product CSV</h1>
    </div>
  </div>
  <h3 class="center" v-if="success">{{ success }}</h3>
  <h3 class="center err" v-if="error">{{ error }}</h3>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      success: "",
      error: "",
    };
  },
  methods: {
    async productCsv() {
      try {
        const response = axios.get("/manager/export_product_csv");
        this.success =
          "Your request sent Successfully! Please check your email";
        this.setMessageTimeout();
      } catch (error) {
        this.error = "Something went wrong";
        this.setMessageTimeout();
        console.log(error);
      }
    },
    setMessageTimeout() {
      setTimeout(() => {
        this.success = "";
        this.error = "";
      }, 5000);
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
  cursor: pointer;
}
.request:hover {
  background-color: lightblue;
}

.center {
  text-align: center;
  margin: 50px 0px;
}
.err {
  color: red;
}
</style>
