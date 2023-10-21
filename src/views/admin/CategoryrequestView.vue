<template>
  <request-bar
    @selected-option="showCurrent"
    :currentName="'Show Pending Category Requests'"
    :previousName="'Show Rejected/Approved Requests'"
  />
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
import ShowcategoryRequest from "@/components/admin/ShowcategoryRequest.vue";
import ShowupdatedcategoryRequest from "@/components/admin/ShowupdatedcategoryRequest.vue";
import RequestBar from "@/components/RequestBar.vue";
import axios from "axios";
export default {
  name: "RequestView",
  components: { ShowcategoryRequest, ShowupdatedcategoryRequest, RequestBar },
  data() {
    return {
      requestDetails: [],
      updatedRequestDetails: [],
      showRequest: true,
    };
  },
  methods: {
    showCurrent(isPendingselected) {
      if (isPendingselected) {
        this.showRequest = true;
        this.getCategoryRequests();
      } else {
        this.showRequest = false;
        this.getUpdatedRequests();
      }
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

<style scoped></style>
