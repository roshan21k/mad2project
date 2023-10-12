<template>
  <h1 v-if="roles.length > 0">Pending Role Requests</h1>
  <div class="container" v-if="roles.length > 0">
    <div>
      <table>
        <thead>
          <th>ID</th>
          <th>Username</th>
          <th>User email</th>
          <th>Role</th>
          <th>Approve/Reject</th>
        </thead>
        <tbody>
          <tr v-for="role in roles" :key="role.id">
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
  <div v-else><h1>No Pending Requests</h1></div>
</template>

<script>
import axios from "axios";
export default {
  name: "RoleView",
  data() {
    return {
      roles: [],
    };
  },
  methods: {
    async getRoleDetails() {
      try {
        const response = await axios.get("/admin/roles");
        this.roles = response.data.role_details;
      } catch (error) {
        console.log(error);
      }
    },
    async rejectRole(id) {
      try {
        const response = await axios.patch(`/admin/reject/${id}`);
        this.getRoleDetails();
      } catch (error) {
        console.log(error);
      }
    },
    async approveRole(id) {
      try {
        const response = await axios.patch(`/admin/approve/${id}`);
        this.getRoleDetails();
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.getRoleDetails();
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
