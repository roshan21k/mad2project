<template>
  <h1 v-if="this.roles.length > 0">Pending requests</h1>
  <h1 v-else>No Pending Requests</h1>
  <div class="container" v-if="this.roles.length > 0">
    <div style="overflow-x: auto">
      <table>
        <thead>
          <th>ID</th>
          <th>Username</th>
          <th>User email</th>
          <th>Role</th>
          <th>Approve/Reject</th>
        </thead>
        <tbody>
          <tr v-for="role in this.roles" :key="role.id">
            <td>{{ role.id }}</td>
            <td>{{ role.user.username }}</td>
            <td>{{ role.user.email }}</td>
            <td>{{ role.role }}</td>
            <td>
              <button class="approve" @click="approveRole(role.id)">
                Approve</button
              ><button class="reject" @click="rejectRole(role.id)">
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import RequestBar from "@/components/RequestBar.vue";
export default {
  name: "RoleView",
  components: { RequestBar },
  data() {
    return {};
  },
  props: ["roles"],
  emits: ["request"],
  methods: {
    async rejectRole(id) {
      try {
        const response = await axios.patch(`/admin/reject/${id}`);
        this.$emit("request");
        this.getRoleDetails();
      } catch (error) {
        console.log(error);
      }
    },
    async approveRole(id) {
      try {
        const response = await axios.patch(`/admin/approve/${id}`);
        this.$emit("request");
        this.getRoleDetails();
      } catch (error) {
        console.log(error);
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
