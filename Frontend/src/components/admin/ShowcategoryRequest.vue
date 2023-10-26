<template>
  <h1 class="center" v-if="requestDetails.length > 0">
    Pending requests for Category Updates
  </h1>
  <h1 class="center" v-else>No Pending requests</h1>
  <div class="container" v-if="requestDetails.length > 0">
    <div style="overflow-x: auto">
      <p class="center" v-if="success" style="color: green">{{ success }}</p>
      <p class="center" v-if="error" style="color: red">{{ error }}</p>
      <table>
        <thead>
          <th>ID</th>
          <th>Name</th>
          <th>Action</th>
          <th>Status</th>
          <th>Username</th>
          <th>Approve/Reject</th>
        </thead>
        <tbody>
          <tr v-for="request in visibleRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>
              {{ request.name }}
              <div v-if="request.old_name">
                <i>
                  <del> ({{ request.old_name }})</del></i
                >
              </div>
            </td>
            <td :style="actionColor(request.action)">{{ request.action }}</td>
            <td>{{ request.status }}</td>
            <td>{{ request.user.username }}</td>
            <td>
              <button class="approve" @click="approveCategory(request.id)">
                Approve</button
              ><button class="reject" @click="rejectCategory(request.id)">
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
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "ShowcategoryRequest",
  props: ["requestDetails"],
  emits: ["request"],
  data() {
    return {
      perPage: 5,
      currentPage: 1,
      success: "",
      error: "",
    };
  },
  methods: {
    async rejectCategory(id) {
      try {
        const response = await axios.patch(`/admin/reject/category/${id}`);
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
    async approveCategory(id) {
      try {
        const response = await axios.post(`/admin/approve/category/${id}`);
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
.center {
  text-align: center;
}
h1 {
  margin: 50px 0px;
}
p {
  margin-bottom: 20px;
  font-weight: bold;
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
