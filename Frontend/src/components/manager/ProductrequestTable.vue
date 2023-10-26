<template>
  <h1 v-if="requestDetails.length > 0">Previous requests</h1>
  <div class="container" v-if="requestDetails.length > 0">
    <div style="overflow-x: auto">
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
          </tr>
        </thead>
        <tbody v-for="request in this.visibleRequests" :key="request.id">
          <tr>
            <td>{{ request.id }}</td>
            <td>
              {{
                request.new_name
                  ? request.new_name
                  : request.product.name && request.product
              }}<br />
              <del
                class="old"
                v-if="
                  request.new_name !== request.product?.name &&
                  request.action === 'update' &&
                  request.product
                "
                >{{ request.product ? request.product.name : "NA" }}</del
              >
            </td>
            <td>
              {{
                request.new_desc
                  ? request.new_desc.slice(0, 8)
                  : request.product?.description
                  ? request.product.description.slice(0, 8)
                  : "NA"
              }}
              <a
                v-if="request.new_desc || request.product?.description"
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
                  request.action === 'update' &&
                  request.product
                "
                >{{ request.product ? request.product.uom : "NA" }}</del
              >
            </td>
            <td>
              <span v-if="request?.new_price"> &#x20B9; </span>
              {{
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
              >
                &#x20B9;
                {{ request.product ? request.product.price : "NA" }}</del
              >
            </td>
            <td>
              <p v-if="request.action === 'update'">Stock Added:-</p>
              {{
                request.new_stock || request.new_stock === 0
                  ? request.new_stock
                  : "NA"
              }}
            </td>
            <td>{{ request.action }}</td>
            <td :style="statusColor(request.status)">
              {{ request.status }}
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
import ModalComp from "../ModalComp.vue";

export default {
  name: "CategoryrequestTable",
  components: { ModalComp },
  props: ["requestDetails"],
  data() {
    return {
      perPage: 5, // Number of items to show per page
      currentPage: 1, // Current page
      isModalVisible: false,
      content: "",
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
    statusColor(status) {
      switch (status) {
        case "pending":
          return "color:orange; font-weight:bold";
        case "rejected":
          return "color:red; font-weight:bold";
        case "approved":
          return "color:green;  font-weight:bold";
      }
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
</style>
