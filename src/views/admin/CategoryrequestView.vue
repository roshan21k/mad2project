<template>
  <div class="filterbox">
    <button :class="{ selected: isPendingSelected }" @click="showPending">
      Show Pending requests
    </button>
    <button :class="{ selected: isCompletedSelected }" @click="showCompleted">
      Show Approved/Rejected Requests
    </button>
  </div>
  <showcategory-request
    v-if="showRequest"
    :requestDetails="requestDetails"
    @request="getRequests()"
  />
  <showupdatedcategory-request
    v-else
    :updatedRequestDetails="updatedRequestDetails"
  />
</template>

<script>
import ShowcategoryRequest from "../../components/admin/ShowcategoryRequest.vue";
import ShowupdatedcategoryRequest from "../../components/admin/ShowupdatedcategoryRequest.vue";
import axios from "axios";
export default {
  name: "RequestView",
  components: { ShowcategoryRequest, ShowupdatedcategoryRequest },
  data() {
    return {
      requestDetails: [],
      updatedRequestDetails: [],
      showRequest: true,
      isPendingSelected: true,
      isCompletedSelected: false,
    };
  },
  methods: {
    showPending() {
      this.showRequest = true;
      this.isPendingSelected = true;
      this.isCompletedSelected = false;
      this.getCategoryRequests();
    },
    showCompleted() {
      this.showRequest = false;
      this.isPendingSelected = false;
      this.isCompletedSelected = true;
      this.getUpdatedRequests();
    },
    getRequests() {
      this.getCategoryRequests();
      this.getUpdatedRequests();
    },
    async getCategoryRequests() {
      try {
        const response = await axios.get("/admin/category_requests");
        this.requestDetails = response.data.category_requests;
      } catch (error) {
        console.log(error);
      }
    },
    async getUpdatedRequests() {
      try {
        const response = await axios.get("/admin/updated_category_requests");
        this.updatedRequestDetails = response.data.category_requests;
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.getCategoryRequests();
    this.getUpdatedRequests();
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin: 50px 0px;
}
.filterbox {
  display: flex;
  justify-content: center;
  gap: 50px;
  margin-top: 50px;
}
button {
  padding: 15px;
  background-color: white;
  cursor: pointer;
}
button:hover {
  background-color: lightblue;
}
.selected {
  background-color: lightblue;
}
</style>
