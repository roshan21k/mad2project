<template>
  <request-bar
    @selected-option="showCurrent"
    :currentName="'Show Pending Product Requests'"
    :previousName="'Show Rejected/Approved Requests'"
  />
  <showproduct-request
    v-if="showRequest"
    :requestDetails="requestDetails"
    @request="getRequests()"
  />
  <showupdatedproduct-request v-else :requestDetails="updatedRequestDetails" />
</template>

<script>
import ShowproductRequest from "@/components/admin/ShowproductRequest.vue";
import axios from "axios";
import ShowupdatedproductRequest from "@/components/admin/ShowupdatedproductRequest.vue";
import RequestBar from "@/components/RequestBar.vue";
export default {
  name: "ProductrequestView",
  components: { ShowproductRequest, ShowupdatedproductRequest, RequestBar },
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
        this.getProductRequests();
      } else {
        this.showRequest = false;
        this.getUpdatedRequests();
      }
    },
    getRequests() {
      this.getProductRequests();
      this.getUpdatedRequests();
    },
    async getProductRequests() {
      try {
        const response = await axios.get("/admin/product_requests");
        this.requestDetails = response.data.product_requests;
      } catch (error) {
        console.log(error);
      }
    },
    async getUpdatedRequests() {
      try {
        const response = await axios.get("/admin/updated_product_requests");
        this.updatedRequestDetails = response.data.product_requests;
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.getProductRequests();
    this.getUpdatedRequests();
  },
};
</script>

<style scoped></style>
