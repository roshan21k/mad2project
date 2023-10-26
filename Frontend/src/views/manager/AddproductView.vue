<template>
  <request-bar
    @selected-option="showCurrent"
    :currentName="'Add Product'"
    :previousName="'Show Previous Add Requests'"
  />
  <div v-if="isAddSelected" class="container">
    <form class="add-product" @submit.prevent="handleSubmit">
      <h2 class="center">Add Product Form</h2>
      <label for="category-name">Name of product</label>
      <input
        type="text"
        placeholder="Name of the product to be added eg)Apple"
        v-model="newName"
      />
      <label for="category-name">Description Of the product</label>
      <textarea
        cols="30"
        rows="10"
        placeholder="Description for new product (max 250 characters)"
        v-model="newDescription"
      ></textarea>
      <label for="category-name">Unit of Measurement-UOM</label>
      <input
        type="text"
        placeholder="Unit of Measurement eg) kg ,pack, liters, dozen etc.,"
        v-model="newUom"
      />
      <label for="category-name">Price of product</label>
      <input
        type="number"
        placeholder="Price of new Product per unit eg) 157 ,200 etc"
        v-model="newPrice"
      />
      <label for="category-name">Intial Stocks to be added</label>
      <input
        type="number"
        placeholder="Initial Stocks to be added "
        v-model="newStock"
      />
      <label for="category-name"
        >Select the category the product belongs to</label
      >
      <select class="checkbox" v-model="selectedCategory">
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>
      <p>Note:- Product will be Updated on approval</p>
      <p style="color: red" v-if="err">{{ err }}</p>
      <p style="color: green" v-if="success">{{ success }}</p>
      <button class="submit" type="submit">Submit for approval</button>
    </form>
  </div>
  <productrequest-table v-else :requestDetails="addRequestDetails" />
</template>

<script>
import axios from "axios";
import ProductrequestTable from "@/components/manager/ProductrequestTable.vue";
import RequestBar from "@/components/RequestBar.vue";
export default {
  name: "AddproductView",
  components: { ProductrequestTable, RequestBar },
  data() {
    return {
      newName: "",
      newDescription: "",
      newUom: "",
      newPrice: 0,
      newStock: 0,
      selectedCategory: 0,
      categories: [],
      err: "",
      success: "",
      requestDetails: [],
      isAddSelected: true,
    };
  },
  computed: {
    addRequestDetails() {
      return this.requestDetails.filter((item) => item.action === "add");
    },
  },
  methods: {
    showCurrent(isAddSelect) {
      if (isAddSelect) {
        this.isAddSelected = true;
        this.productRequests();
      } else {
        this.isAddSelected = false;
        this.productRequests();
      }
    },
    formValidation() {
      if (this.newName < 5) {
        this.err = "Name should be atleast 5 characters";
        return false;
      } else if (this.newDescription < 10 || this.newDescription > 250) {
        this.err = "Description should be between 5 and 250 characters";
        return false;
      } else if (!this.newUom) {
        this.err = "Please enter a valid UOM";
        return false;
      } else if (this.newPrice <= 0) {
        this.err = "Price can't be 0 or lesser";
        return false;
      } else if (this.newStock <= 0) {
        this.err = "Stock can't be 0 or lesser";
        return false;
      } else if (this.selectedCategory === 0) {
        this.err = "Please select a category";
        return false;
      } else {
        return true;
      }
    },
    async getCategories() {
      try {
        const response = await axios.get("/user/filter");
        this.categories = response.data.categories;
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
      if (this.formValidation()) {
        try {
          const response = await axios.post("/manager/add_product", {
            new_name: this.newName,
            new_desc: this.newDescription,
            new_uom: this.newUom,
            new_price: this.newPrice,
            new_stock: this.newStock,
            category_id: this.selectedCategory,
          });
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
    this.getCategories();
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
</style>
