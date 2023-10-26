<template>
  <h1 v-if="updatedRequestDetails.length > 0">
    Approved/Rejected for Category
  </h1>
  <h1 v-else>No requests Found</h1>
  <div class="container" v-if="updatedRequestDetails.length > 0">
    <div style="overflow-x: auto">
      <select v-model="rowPerPage" @change="changeRows">
        <option :value="5">5 per table</option>
        <option :value="10">10 per table</option>
        <option :value="10">15 per table</option>
        <option :value="10">20 per table</option>
      </select>
      <table>
        <thead>
          <th>ID</th>
          <th>Name</th>
          <th>Action</th>
          <th>Status</th>
          <th>Username</th>
        </thead>
        <tbody>
          <tr v-for="request in visibleRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.name }}</td>
            <td>{{ request.action }}</td>
            <td :style="statusColor(request.status)">{{ request.status }}</td>
            <td>{{ request.user.username }}</td>
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
  name: "ShowupdatedcategoryRequest",
  props: ["updatedRequestDetails"],
  data() {
    return {
      perPage: 5,
      currentPage: 1,
      rowPerPage: 5,
    };
  },
  methods: {
    changeRows() {
      this.perPage = this.rowPerPage;
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
      return Math.ceil(this.updatedRequestDetails.length / this.perPage);
    },
    visibleRequests() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      const endIndex = startIndex + this.perPage;
      return this.updatedRequestDetails.slice(startIndex, endIndex);
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
