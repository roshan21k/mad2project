<template>
  <div class="filterbox">
    <button
      :class="{ selected: isUpdateSelected, 'filter-button': true }"
      @click="showUpdate"
    >
      Update Product
    </button>
    <button
      :class="{ selected: isShowSelected, 'filter-button': true }"
      @click="showPrevious"
    >
      Show Previous Requests
    </button>
  </div>
  <div v-if="isUpdateSelected" class="container">
    <form class="add-product" @submit.prevent="handleSubmit">
      <h2 class="center">Update Product Form</h2>
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
      <label v-if="selectedCategory">Select the Product to be Updated</label>
      <select
        class="checkbox"
        v-if="selectedCategory"
        v-model="selectedProduct"
        @change="showOldInfo"
      >
        <option
          v-for="product in visibleProducts"
          :key="product.id"
          :value="product.id"
        >
          {{ product.name }}
        </option>
      </select>
      <label v-if="selectedProduct">Name of the product</label>
      <input
        v-if="selectedProduct"
        type="text"
        placeholder="Name of the product to be added eg)Apple"
        v-model="newName"
      />
      <label v-if="selectedProduct">Description</label>
      <textarea
        v-if="selectedProduct"
        cols="30"
        rows="10"
        placeholder="Description for new product (max 250 characters)"
        v-model="newDescription"
      ></textarea>
      <label v-if="selectedProduct">Unit of Measurement</label>
      <input
        v-if="selectedProduct"
        type="text"
        placeholder="Unit of Measurement eg) kg ,pack, liters, dozen etc.,"
        v-model="newUom"
      />
      <label v-if="selectedProduct"
        >Price <b> (OldPrice:- &#x20B9;{{ oldPrice }})</b></label
      >
      <input
        v-if="selectedProduct"
        type="number"
        placeholder="Price of new Product per unit eg) 157 ,200 etc"
        v-model="newPrice"
      />
      <label v-if="selectedProduct"
        >Stocks to be added
        <b>(StockLeft:- {{ oldStock }}{{ oldUom }}) </b></label
      >
      <input
        v-if="selectedProduct"
        type="number"
        placeholder=" Stocks to be added "
        v-model="newStock"
      />
      <p>Note:- Product will be Updated on approval</p>
      <p style="color: red" v-if="err">{{ err }}</p>
      <p style="color: green" v-if="success">{{ success }}</p>
      <button class="submit" type="submit">Submit for approval</button>
    </form>
  </div>
  <productrequest-table v-else :requestDetails="updateRequestDetails" />
</template>

<script>
import axios from "axios";
import ProductrequestTable from "@/components/manager/ProductrequestTable.vue";
export default {
  name: "AddproductView",
  components: { ProductrequestTable },
  data() {
    return {
      newName: "",
      newDescription: "",
      newUom: "",
      newStock: 0,
      newPrice: 0,
      oldPrice: 0,
      oldStock: 0,
      oldUom: "",
      categories: [],
      err: "",
      success: "",
      requestDetails: [],
      isUpdateSelected: true,
      isShowSelected: false,
      allDetails: [],
      selectedCategory: 0,
      selectedProduct: 0,
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
    updateRequestDetails() {
      if (this.requestDetails.length > 0) {
        return this.requestDetails.filter((item) => item.action === "update");
      }
    },
  },

  methods: {
    showUpdate() {
      (this.isUpdateSelected = true), (this.isShowSelected = false);
    },
    showPrevious() {
      (this.isUpdateSelected = false), (this.isShowSelected = true);
    },
    showOldInfo() {
      if (this.selectedProduct) {
        console.log("workdng");
        const prodDetails = this.allDetails
          .filter((item) => item.id === this.selectedCategory)
          .map((item) => item.products)
          .flat()
          .filter((product) => product.id === this.selectedProduct)[0];
        this.newName = prodDetails.name;
        this.newDescription = prodDetails.description;
        this.newUom = prodDetails.uom;
        this.oldUom = prodDetails.uom;
        this.oldPrice = prodDetails.price;
        this.oldStock = prodDetails.stock;
        this.newPrice = prodDetails.price;
        this.newStock = prodDetails.stock;
      }
    },
    async getAllDetails() {
      try {
        const response = await axios.get("/manager/all_details");
        this.allDetails = response.data.all_details;
      } catch (error) {
        console.log(error);
      }
    },
    formValidation() {
      if (this.selectedCategory === 0) {
        this.err = "Please select a category";
        return false;
      } else if (this.selectedProduct === 0) {
        this.err = "Please select a Product";
        return false;
      } else if (this.newName < 5) {
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
      } else {
        return true;
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
          const response = await axios.post("/manager/update_product", {
            new_name: this.newName,
            new_desc: this.newDescription,
            new_uom: this.newUom,
            new_price: this.newPrice,
            new_stock: this.newStock,
            category_id: this.selectedCategory,
            product_id: this.selectedProduct,
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
    this.productRequests();
    this.getAllDetails();
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
