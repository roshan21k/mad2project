<template>
  <h1 v-if="this.roles.length > 0">Previous requests</h1>
  <h1 v-else>No Request Available</h1>
  <div class="container" v-if="this.roles.length > 0">
    <div style="overflow-x: auto">
      <table>
        <thead>
          <th>ID</th>
          <th>Username</th>
          <th>User email</th>
          <th>Role</th>
          <th>Status</th>
        </thead>
        <tbody>
          <tr v-for="role in this.roles" :key="role.id">
            <td>{{ role.id }}</td>
            <td>{{ role.user.username }}</td>
            <td>{{ role.user.email }}</td>
            <td>{{ role.role }}</td>
            <td :style="statusColor(role.status)">{{ role.status }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import RequestBar from "@/components/RequestBar.vue";
export default {
  name: "RoleView",
  components: { RequestBar },
  data() {
    return {};
  },
  props: ["roles"],
  methods: {
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
</style>
