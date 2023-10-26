<template>
  <request-bar
    @selected-option="showCurrent"
    :currentName="'Show Pending Role Requests'"
    :previousName="'Show Rejected/Approved Requests'"
  />
  <showrole-request
    v-if="showRequest"
    :roles="roles"
    @request="getRequests()"
  />
  <showupdatedrole-request v-else :roles="updatedRoles" />
</template>

<script>
import axios from "axios";
import RequestBar from "@/components/RequestBar.vue";
import ShowroleRequest from "@/components/admin/ShowroleRequest.vue";
import ShowupdatedroleRequest from "@/components/admin/ShowupdatedroleRequest.vue";
export default {
  name: "RoleView",
  components: { RequestBar, ShowroleRequest, ShowupdatedroleRequest },
  data() {
    return {
      roles: [],
      updatedRoles: [],
      showRequest: true,
    };
  },
  methods: {
    showCurrent(isPendingselected) {
      if (isPendingselected) {
        this.showRequest = true;
        this.getRoleDetails();
      } else {
        this.showRequest = false;
        this.getUpdatedRoleDetails();
      }
    },
    getRequests() {
      this.getRoleDetails();
    },
    async getRoleDetails() {
      try {
        const response = await axios.get("/admin/roles");
        this.roles = response.data.role_details;
      } catch (error) {
        console.log(error);
      }
    },
    async getUpdatedRoleDetails() {
      try {
        const response = await axios.get("/admin/updated_roles");
        this.updatedRoles = response.data.updated_role_details;
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.getRoleDetails();
    this.getUpdatedRoleDetails();
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
