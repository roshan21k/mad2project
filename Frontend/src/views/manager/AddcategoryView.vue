<template>
  <request-bar
    @selected-option="showCurrent"
    :currentName="'Add Category'"
    :previousName="'Show Previous Add Requests'"
  />
  <h1 class="title" v-if="isAddSelected">Add category</h1>
  <div class="container" v-if="isAddSelected">
    <form class="category" @submit.prevent="handleSubmit">
      <label for="category-name">Name for new Category</label>
      <input type="text" name="" id="category-name" v-model="updatedName" />
      <p>Note:- New Category will be Added on approval</p>
      <p class="error" v-if="err">{{ err }}</p>
      <p style="color: green" v-if="success">{{ success }}</p>
      <button class="submit" type="submit">Submit for approval</button>
    </form>
  </div>
  <categoryrequest-table v-else :requestDetails="addRequests" />
</template>

<script>
import axios from "axios";
import CategoryrequestTable from "@/components/manager/CategoryrequestTable.vue";
import RequestBar from "@/components/RequestBar.vue";
export default {
  name: "AddcategoryView",
  components: { CategoryrequestTable, RequestBar },
  data() {
    return {
      updatedName: "",
      err: "",
      success: "",
      requestDetails: [],
      isAddSelected: true,
    };
  },
  methods: {
    showCurrent(isAddSelect) {
      if (isAddSelect) {
        this.isAddSelected = true;
        this.getRequests();
      } else {
        this.isAddSelected = false;
        this.getRequests();
      }
    },
    async handleSubmit() {
      try {
        if (this.updatedName.length >= 5) {
          const response = await axios.post("/manager/add_category", {
            updated_name: this.updatedName,
          });
          this.success = response.data.message;
          this.clearMessage();
          this.getRequests();
        } else {
          this.err = "Name should be atleast 5 characters";
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
  computed: {
    addRequests() {
      return this.requestDetails.filter((request) => request.action === "add");
    },
  },
  created() {
    this.getRequests();
  },
};
</script>

<style scoped>
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
