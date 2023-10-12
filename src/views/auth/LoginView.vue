<template>
  <div class="login">
    <form @submit.prevent="handleSubmit">
      <h1>Login</h1>
      <p class="red" v-if="errors">{{ errors }}</p>
      <input
        type="text"
        v-model="username"
        placeholder="Enter Your Username or Email"
      />
      <input
        type="password"
        v-model="password"
        placeholder="Enter Your Password"
        autocomplete="on"
      />
      <button>Login</button>
    </form>
  </div>
</template>
<script>
import axios from "axios";
import { mapState, mapMutations } from "vuex";
export default {
  data() {
    return {
      username: "",
      password: "",
      errors: "",
    };
  },
  methods: {
    ...mapMutations(["setAuthenticated", "setUserRole"]),
    redirectRoute(role) {
      if (role == "manager") {
        return "/manager";
      } else if (role == "admin") {
        return "/admin";
      } else {
        return "/";
      }
    },
    async handleSubmit() {
      if (this.username.length == 0) {
        this.errors = "Please Enter a Username";
      } else if (this.password.length == 0) {
        this.errors = "Please Enter Password";
      } else if (this.username.includes("@")) {
        try {
          const response = await axios.post("auth/login", {
            email: this.email,
            password: this.password,
          });
          console.log(response.data.tokens.access);
          localStorage.setItem("accesstoken", response.data.tokens.access);
          localStorage.setItem("refreshtoken", response.data.tokens.refresh);
          this.setAuthenticated(true);
          this.setUserRole(response.data.role);
          this.$router.push(this.redirectRoute(response.data.role));
        } catch (err) {
          console.log("email error");
          if (!err.response.data.error) {
            this.errors = err;
          } else {
            this.errors = err.response.data.error;
          }
        }
      } else {
        try {
          const response = await axios.post("auth/login", {
            username: this.username,
            password: this.password,
          });
          console.log(response.data.tokens.access);
          localStorage.setItem("accessToken", response.data.tokens.access);
          localStorage.setItem("refreshToken", response.data.tokens.refresh);
          localStorage.setItem("userRole", response.data.role);
          this.setAuthenticated(true);
          this.setUserRole(response.data.role);
          this.$router.push(this.redirectRoute(response.data.role));
        } catch (err) {
          console.log("username error");
          if (!err?.response?.data?.error) {
            this.errors = err;
          } else {
            this.errors = err.response.data.error;
          }
        }
      }
    },
  },
};
</script>
<style scoped>
.login {
  display: flex;
  justify-content: center;
  min-height: calc(100vh - 75px);
  align-items: center;
}
form {
  display: flex;
  flex-direction: column;
  width: 350px;
  height: 400px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  justify-content: space-evenly;
  text-align: center;
}
input {
  padding: 10px;
  margin: 10px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 16px;
}
button {
  padding: 10px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  text-decoration: none;
  background-color: lightgreen;
  border-radius: 50px;
}
.red {
  color: red;
  margin: 0%;
  padding: 0%;
}
</style>
