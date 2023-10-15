<template>
  <div class="filterbox">
    <button
      :class="{ selected: isDeleteSelected, 'filter-button': true }"
      @click="showDelete"
    >
      Delete Product
    </button>
    <button
      :class="{ selected: isShowSelected, 'filter-button': true }"
      @click="showPrevious"
    >
      Show Previous Requests
    </button>
  </div>
  <div v-if="isDeleteSelected" class="container">
    <form class="add-product" @submit.prevent="handleSubmit">
      <h2 class="center">Delete Product Form</h2>
      <label>Select the category the product belongs to</label>
      <select class="checkbox" v-model="selectedCategory">
        <option
          v-for="category in allDetails"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>
      <label>Select the Product to be Deleted</label>
      <select
        class="checkbox"
        v-if="selectedCategory"
        v-model="selectedProduct"
      >
        <option
          v-for="product in visibleProducts"
          :key="product.id"
          :value="product.id"
        >
          {{ product.name }}
        </option>
      </select>
      <p>Note:- Product will be Deleted on approval</p>
      <p style="color: red" v-if="err">{{ err }}</p>
      <p style="color: green" v-if="success">{{ success }}</p>
      <button class="submit" type="submit">Submit for approval</button>
    </form>
  </div>
  <productrequest-table v-else :requestDetails="deleteRequestDetails" />
</template>

<script>
import axios from "axios";
import ProductrequestTable from "@/components/manager/ProductrequestTable.vue";
export default {
  name: "AddproductView",
  components: { ProductrequestTable },
  data() {
    return {
      selectedCategory: 0,
      selectedProduct: 0,
      allDetails: [],
      err: "",
      success: "",
      requestDetails: [],
      isDeleteSelected: true,
      isShowSelected: false,
    };
  },
  computed: {
    visibleProducts() {
      if (this.selectedCategory !== 0) {
        return this.allDetails
          .filter((item) => item.id === this.selectedCategory)
          .map((item) => item.products)
          .flat();
      }
    },
    deleteRequestDetails() {
      if (this.requestDetails.length > 0) {
        return this.requestDetails.filter((item) => item.action === "delete");
      }
    },
  },
  methods: {
    showDelete() {
      (this.isDeleteSelected = true), (this.isShowSelected = false);
    },
    showPrevious() {
      (this.isDeleteSelected = false),
        (this.isShowSelected = true),
        this.productRequests();
    },
    async getAllDetails() {
      try {
        const response = await axios.get("/manager/all_details");
        this.allDetails = response.data.all_details;
      } catch (error) {
        console.log(error);
      }
    },
    async productRequests() {
      try {
        const response = await axios.get("/manager/product_requests");
        this.requestDetails = response.data.product_requests;
      } catch (error) {
        console.log(error);
      }
    },
    async handleSubmit() {
      try {
        const response = await axios.post(
          `/manager/delete_product/${this.selectedProduct}/${this.selectedCategory}`
        );
        this.success = response.data.message;
        this.clearMessages();
        this.productRequests();
      } catch (error) {
        if (error?.response?.data?.error) {
          this.err = error.response.data.error;
          this.clearMessages();
        } else {
          this.err = error;
          this.clearMessages();
        }
      }
    },
    clearMessages() {
      setTimeout(() => {
        this.err = "";
        this.success = "";
      }, 3000);
    },
  },
  created() {
    this.getAllDetails();
    this.productRequests();
  },
};
</script>

<style scoped>
.container {
  margin: 50px 0px;
  display: flex;
  justify-content: center;
}
.add-product {
  display: flex;
  flex-direction: column;
  gap: 25px;
  padding: 25px;
  border: 1px solid black;
  width: 400px;
}

input,
.checkbox,
.submit {
  height: 35px;
  padding: 5px;
}
textarea {
  padding: 5px;
}
.center {
  text-align: center;
}
.filterbox {
  display: flex;
  justify-content: center;
  gap: 50px;
  margin-top: 50px;
}
.filter-button {
  padding: 15px;
  background-color: white;
  cursor: pointer;
}
.filter-button:hover {
  background-color: lightblue;
}
.selected {
  background-color: lightblue;
}
</style>
