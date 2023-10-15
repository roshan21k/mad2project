<template>
  <h1 v-if="requestDetails.length > 0">Pending requests</h1>
  <h1 v-else>No Pending Requests</h1>
  <div class="container" v-if="requestDetails.length > 0">
    <div style="overflow-x: auto">
      <p class="center" v-if="success" style="color: green">{{ success }}</p>
      <p class="center" v-if="error" style="color: red">{{ error }}</p>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>UOM</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Action</th>
            <th>Status</th>
            <th>Approve/Reject</th>
          </tr>
        </thead>
        <tbody v-for="request in this.visibleRequests" :key="request.id">
          <tr>
            <td>{{ request.id }}</td>
            <td>
              {{ request.new_name ? request.new_name : request.product.name
              }}<br />
              <del
                class="old"
                v-if="
                  request.new_name !== request.product?.name &&
                  request.action === 'update'
                "
                >{{ request.product ? request.product.name : "NA" }}</del
              >
            </td>
            <td>
              {{
                request.new_desc
                  ? request.new_desc.slice(0, 8)
                  : request.product.description
                  ? request.product.description.slice(0, 8)
                  : "NA"
              }}
              <a
                v-if="request.new_desc || request.product.description"
                @click="
                  showModal(
                    request.new_desc
                      ? request.new_desc
                      : request.product.description
                      ? request.product.description
                      : 'NA'
                  )
                "
              >
                ....(Read More)</a
              >
            </td>
            <td>
              {{
                request.new_uom
                  ? request.new_uom
                  : request.product
                  ? request.product.uom
                  : "NA"
              }}<br />
              <del
                class="old"
                v-if="
                  request.new_uom !== request.product?.uom &&
                  request.action === 'update'
                "
                >{{ request.product ? request.product.uom : "NA" }}</del
              >
            </td>
            <td>
              <span v-if="request?.new_price"> &#x20B9; </span
              >{{
                request.new_price
                  ? request.new_price
                  : request.product
                  ? request.product.price
                  : "NA"
              }}<br />
              <del
                class="old"
                v-if="
                  request.new_price !== request.product?.price &&
                  request.action === 'update' &&
                  request.product?.price
                "
                >&#x20B9;{{
                  request.product ? request.product.price : "NA"
                }}</del
              >
            </td>
            <td>
              <p v-if="request.action === 'update'">Stock Added:-</p>
              {{
                request.new_stock || request.new_stock === 0
                  ? request.new_stock
                  : "NA"
              }}<br />
              <p
                class="old"
                v-if="
                  request.new_stock !== request.product?.stock &&
                  request.action === 'update'
                "
              >
                Stock left:- {{ request.product.stock }}
              </p>
            </td>
            <td :style="actionColor(request.action)">{{ request.action }}</td>
            <td>
              {{ request.status }}
            </td>
            <td>
              <button class="approve" @click="approveProduct(request.id)">
                Approve</button
              ><button class="reject" @click="rejectProduct(request.id)">
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button @click="previousPage" :disabled="currentPage === 1">
          Previous
        </button>
        <span>Page {{ currentPage }} of {{ totalPages }} </span>
        <button @click="nextPage" :disabled="currentPage === totalPages">
          Next
        </button>
      </div>
    </div>
  </div>
  <modal-comp
    v-if="isModalVisible"
    :content="content"
    @modal-closed="closeModal"
  />
</template>

<script>
import axios from "axios";
import ModalComp from "../ModalComp.vue";

export default {
  name: "CategoryrequestTable",
  components: { ModalComp },
  props: ["requestDetails"],
  emits: ["request"],
  data() {
    return {
      perPage: 5,
      currentPage: 1,
      isModalVisible: false,
      content: "",
      success: "",
      error: "",
    };
  },
  methods: {
    closeModal() {
      this.isModalVisible = false;
    },
    showModal(desc) {
      this.content = desc;
      this.isModalVisible = true;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    actionColor(status) {
      switch (status) {
        case "update":
          return "color:orange; font-weight:bold";
        case "delete":
          return "color:red; font-weight:bold";
        case "add":
          return "color:green;  font-weight:bold";
      }
    },
    async rejectProduct(id) {
      try {
        const response = await axios.patch(`/admin/reject/product/${id}`);
        this.$emit("request");
        this.success = response.data.message;
        this.clearMessageTimeout();
      } catch (error) {
        if (error?.response?.data?.error) {
          this.error = error.response.data.error;
          this.clearMessageTimeout();
        } else {
          this.error = error;
        }
      }
    },
    async approveProduct(id) {
      try {
        const response = await axios.post(`/admin/approve/product/${id}`);
        this.$emit("request");
        this.success = response.data.message;
        this.clearMessageTimeout();
      } catch (error) {
        if (error?.response?.data?.error) {
          this.error = error.response.data.error;
          this.clearMessageTimeout();
        } else {
          this.error = error;
          this.clearMessageTimeout();
        }
      }
    },
    clearMessageTimeout() {
      setTimeout(() => {
        this.success = "";
        this.error = "";
      }, 3000);
    },
  },
  computed: {
    totalPages() {
      return Math.ceil(this.requestDetails.length / this.perPage);
    },
    visibleRequests() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.requestDetails.slice(startIndex, endIndex);
    },
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin: 50px 0px;
}
.container {
  display: flex;
  margin: 50px 0px;
  justify-content: center;
}
table {
  margin-bottom: 50px;
  border: 1px solid black;
}
th {
  border-bottom: 1px solid black;
  padding: 15px;
}
td {
  padding: 10px 20px;
}
a {
  cursor: pointer;
  color: blue;
}
.old {
  color: orange;
}
button {
  margin-right: 10px;
  padding: 5px;
}
.approve {
  background-color: greenyellow;
}
.reject {
  background-color: lightcoral;
}
.approve:hover {
  background-color: rgb(151, 226, 38);
}
.reject:hover {
  background-color: rgb(193, 103, 103);
}
</style>
