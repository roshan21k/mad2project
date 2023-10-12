<template>
  <div class="apply" v-if="!submitted">
    <form @submit.prevent="handleSubmit">
      <h1>Apply For Manager</h1>
      <p v-if="errors" class="red">{{ errors }}</p>
      <button>Apply</button>
    </form>
  </div>
  <div class="submit" v-else>
    <h1 class="center">Your Request Has Been submitted Successfully</h1>
    <p class="center">You will be notified Soon!</p>
  </div>
  <h1 class="my-request">My Requests</h1>
  <div v-if="requests.length > 0" class="requests">
    <table>
      <thead>
        <tr>
          <th>Id</th>
          <th>Role</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.id }}</td>
          <td>{{ request.role }}</td>
          <td>{{ request.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "ApplyManager",
  data() {
    return {
      errors: "",
      submitted: false,
      requests: [],
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await axios.post("/user/apply");
        console.log(response);
        this.getRequests();
        this.submitted = true;
      } catch (error) {
        if (error?.response?.data?.error) {
          this.errors = error.response.data.error;
        } else {
          console.log(error);
        }
      }
    },
    async getRequests() {
      try {
        const response = await axios.get("/user/requests");
        this.requests = response.data.request_details;
      } catch (error) {
        console.log(error);
      }
    },
    clearErrors() {
      setTimeout(() => {
        this.errors = "";
      }, 3000);
    },
  },
  created() {
    this.getRequests();
  },
};
</script>

<style scoped>
.apply {
  display: flex;
  justify-content: center;
  min-height: calc(100vh - 75px);
  align-items: center;
}
form {
  display: flex;
  flex-direction: column;
  width: 500px;
  height: 250px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  justify-content: space-evenly;
  text-align: center;
}

button {
  height: 50px;
  font-size: 1rem;
}
.submit {
  display: flex;
  justify-content: center;
  flex-direction: column;
  min-height: calc(100vh - 75px);
  align-items: center;
}
.red {
  color: red;
}
.center {
  text-align: center;
  color: green;
}
.requests {
  display: flex;
  justify-content: center;
}
.my-request {
  text-align: center;
  margin-bottom: 50px;
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
