<template>
  <div v-if="userDetails" class="container">
    <div class="box">
      <p><span class="bold"> ID </span>: {{ userDetails.id }}</p>
      <p><span class="bold">Username </span>: {{ userDetails.username }}</p>
      <p><span class="bold">Email </span>: {{ userDetails.email }}</p>
      <p><span class="bold">Role </span>: {{ userDetails.role }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      userDetails: "",
    };
  },
  methods: {
    async getUserDetails() {
      try {
        const response = await axios.get("user/about_me");
        this.userDetails = response.data.about;
      } catch (error) {
        console.log(error);
      }
    },
  },
  created() {
    this.getUserDetails();
  },
};
</script>

<style scoped>
.container {
  display: flex;
  height: calc(100vh - 75px);
  justify-content: center;
  align-items: center;
}
.box {
  display: flex;
  flex-direction: column;
  border: 1px solid black;
  padding: 25px;
  gap: 10px;
}
.bold {
  font-weight: bold;
}
</style>
