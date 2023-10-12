<template>
  <h1 v-if="requestDetails.length > 0">Previous requests</h1>
  <div class="container" v-if="requestDetails.length > 0">
    <div>
      <table>
        <thead>
          <th>ID</th>
          <th>Name</th>
          <th>Action</th>
          <th>Status</th>
        </thead>
        <tbody v-for="request in this.visibleRequests" :key="request.id">
          <tr>
            <td>{{ request.id }}</td>
            <td>{{ request.name }}</td>
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
</template>

<script>
export default {
  name: "CategoryrequestTable",
  props: ["requestDetails"],
  data() {
    return {
      perPage: 5, // Number of items to show per page
      currentPage: 1, // Current page
    };
  },
  methods: {
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
</style>
