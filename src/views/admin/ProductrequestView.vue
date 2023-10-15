<template>
  <div class="filterbox">
    <button :class="{ selected: isPendingSelected }" @click="showPending">
      Show Pending requests
    </button>
    <button :class="{ selected: isCompletedSelected }" @click="showCompleted">
      Show Approved/Rejected Requests
    </button>
  </div>
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
export default {
  name: "ProductrequestView",
  components: { ShowproductRequest, ShowupdatedproductRequest },
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
      this.getProductRequests();
    },
    showCompleted() {
      this.showRequest = false;
      this.isPendingSelected = false;
      this.isCompletedSelected = true;
      this.getUpdatedRequests();
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
