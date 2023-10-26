<template>
  <request-bar
    @selected-option="showCurrent"
    :currentName="'Update Category'"
    :previousName="'Show Previous Update Requests'"
  />
  <h1 class="title" v-if="isUpdateSelected">Update category</h1>
  <div class="container" v-if="isUpdateSelected">
    <form class="category" @submit.prevent="handleSubmit">
      <label for="category-name">Select the category you want to Update</label>
      <select class="checkbox" v-model="selectedCategory">
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>
      <input type="text" placeholder="Enter new Name" v-model="newName" />
      <p>Note:- Category will be Updated on approval</p>
      <p class="error" v-if="err">{{ err }}</p>
      <p style="color: green" v-if="success">{{ success }}</p>
      <button class="submit" type="submit">Submit for approval</button>
    </form>
  </div>
  <categoryrequest-table v-else :requestDetails="updateRequests" />
</template>

<script>
import axios from "axios";
import CategoryrequestTable from "@/components/manager/CategoryrequestTable.vue";
import RequestBar from "@/components/RequestBar.vue";
export default {
  name: "UpdatecategoryView",
  components: { CategoryrequestTable, RequestBar },
  data() {
    return {
      err: "",
      success: "",
      categories: [],
      requestDetails: [],
      selectedCategory: 0,
      newName: "",
      isUpdateSelected: true,
    };
  },
  methods: {
    showCurrent(isUpdateSelect) {
      if (isUpdateSelect) {
        this.isUpdateSelected = true;
        this.getRequests();
      } else {
        this.isUpdateSelected = false;
        this.getRequests();
      }
    },
    async handleSubmit() {
      try {
        if (this.selectedCategory !== 0 && this.newName.length >= 5) {
          const response = await axios.post(
            `/manager/update_category/${this.selectedCategory}`,
            {
              updated_name: this.newName,
            }
          );
          this.getRequests();
          this.success = response.data.message;
          this.clearMessage();
        } else {
          this.err = "Please Select a Category or Enter a Valid Name";
          this.clearMessage();
        }
      } catch (error) {
        if (error?.response?.data?.error) {
          this.err = error.response.data.error;
          this.clearMessage();
        } else {
          this.err = error;
          this.clearMessage();
        }
        console.log(error);
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
    async getRequests() {
      try {
        const response = await axios.get("/manager/requests");
        this.requestDetails = response.data.category_requests;
      } catch (error) {
        console.log(error);
      }
    },
    clearMessage() {
      setTimeout(() => {
        this.err = "";
        this.success = "";
      }, 3000);
    },
  },
  created() {
    this.getRequests();
    this.getCategories();
  },
  computed: {
    updateRequests() {
      return this.requestDetails.filter(
        (request) => request.action === "update"
      );
    },
  },
};
</script>

<style scoped>
.checkbox,
input {
  padding: 10px;
}
.container {
  display: flex;
  justify-content: center;
  margin-top: 50px;
}
.category {
  border: 1px solid black;
  display: flex;
  flex-direction: column;
  gap: 25px;
  padding: 25px;
}
.title {
  margin: 50px;
  text-align: center;
}
input {
  height: 30px;
}
p {
  font-weight: lighter;
}
.submit {
  height: 30px;
}
.error {
  color: red;
}
</style>
