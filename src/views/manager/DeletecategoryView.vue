<template>
  <request-bar
    @selected-option="showCurrent"
    :currentName="'Delete Category'"
    :previousName="'Show Previous Delete Requests'"
  />
  <h1 class="title" v-if="isDeleteSelected">Delete category</h1>
  <div class="container" v-if="isDeleteSelected">
    <form class="category" @submit.prevent="handleSubmit">
      <label for="category-name">Select the category you want to delete</label>
      <select class="checkbox" v-model="selectedCategory">
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>
      <p>Note:- Category will be deleted on approval</p>
      <p class="error" v-if="err">{{ err }}</p>
      <p style="color: green" v-if="success">{{ success }}</p>
      <button class="submit" type="submit">Submit for approval</button>
    </form>
  </div>
  <categoryrequest-table v-else :requestDetails="deleteRequests" />
</template>

<script>
import axios from "axios";
import CategoryrequestTable from "../../components/manager/CategoryrequestTable.vue";
import RequestBar from "@/components/RequestBar.vue";
export default {
  name: "DeletecategoryView",
  components: { CategoryrequestTable, RequestBar },
  data() {
    return {
      err: "",
      categories: [],
      requestDetails: [],
      selectedCategory: 0,
      isDeleteSelected: true,
      success: "",
    };
  },
  methods: {
    showCurrent(isDeleteSelect) {
      if (isDeleteSelect) {
        this.isDeleteSelected = true;
        this.getRequests();
      } else {
        this.isDeleteSelected = false;
        this.getRequests();
      }
    },
    async handleSubmit() {
      try {
        if (this.selectedCategory !== 0) {
          const response = await axios.post(
            `/manager/delete_category/${this.selectedCategory}`
          );
          this.getRequests();
          this.success = response.data.message;
          this.clearMessage();
        } else {
          this.err = "Please Select a Category";
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
    deleteRequests() {
      return this.requestDetails.filter(
        (request) => request.action === "delete"
      );
    },
  },
};
</script>

<style scoped>
.checkbox {
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
