<template>
  <div class="signup">
    <form @submit.prevent="handleSubmit">
      <h1>Sign-Up</h1>
      <p class="red" v-if="errors.length != 0">{{ errors }}</p>

      <input type="text" v-model="username" placeholder="Enter Your Username" />

      <input type="email" v-model="email" placeholder="Enter Your Email" />

      <p class="pass" :style="passStrength" v-if="strength.length != 0">
        {{ strength }}
      </p>
      <input
        type="password"
        v-model="password"
        placeholder="Enter Your Password"
      />
      <input
        type="password"
        v-model="password2"
        placeholder="Confirm Password"
      />
      <button>Sign-Up</button>
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
      email: "",
      password: "",
      password2: "",
      errors: "",
      strength: "",
      passStrength: "",
      labelActive: true,
    };
  },
  // computed: {
  //   ...mapState(["isAuthenticated", "userRole"]),
  // },
  methods: {
    ...mapMutations(["setAuthenticated", "setUserRole"]),
    isValidUsername() {
      const regex = /^[a-zA-Z0-9]+$/;
      return regex.test(this.username);
    },
    async handleSubmit() {
      if (this.username.length < 6) {
        this.errors = `Username Must be of 6 characters Atleast`;
      } else if (!this.isValidUsername()) {
        this.errors = `Username Can't have special characters`;
      } else if (this.email.length == 0) {
        this.errors = `Email Can't be empty`;
      } else if (this.password.length == 0 || this.password2.length == 0) {
        this.errors = `Passwords Can't be empty`;
      } else if (this.password !== this.password2) {
        this.errors = `Passwords Doesn't Match`;
      } else {
        try {
          const response = await axios.post("auth/register", {
            username: this.username,
            email: this.email,
            password: this.password,
          });
          console.log(response.data.tokens.access);
          localStorage.setItem("accessToken", response.data.tokens.access);
          localStorage.setItem("refreshToken", response.data.tokens.refresh);
          localStorage.setItem("userRole", "user");
          this.setAuthenticated(true);
          this.setUserRole("user");
          this.$router.push("/");
        } catch (err) {
          if (!err.response.data.error) {
            this.errors = err;
          } else {
            this.errors = err.response.data.error;
          }
        }
      }
    },
  },
  watch: {
    password(val) {
      if (val.length < 6) {
        this.strength = "Password Strength : Weak ";
        this.passStrength = "color : red";
      } else if (val.length < 10) {
        this.strength = "Password Strength : Good";
        this.passStrength = "color : orange";
      } else {
        this.strength = "Password Strength : Excellent";
        this.passStrength = "color : green";
      }
    },
    password2(val) {
      if (this.password !== this.password2) {
        this.strength = "Passwords Don't Match";
        this.passStrength = "color : red";
      } else {
        this.strength = "";
      }
    },
    username(val) {
      if (!this.isValidUsername()) {
        this.errors = "Username Can't have special characters";
      } else {
        this.errors = "";
      }
    },
  },
};
</script>
<style scoped>
* {
  margin: 0;
  padding: 0;
}
.signup {
  display: flex;
  justify-content: center;
  min-height: calc(100vh - 75px);
  align-items: center;
}
form {
  display: flex;
  flex-direction: column;
  width: 400px;
  height: 500px;
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
  border: 0;
  border-bottom: 1px solid #ccc;
  border-radius: 3px;
  font-size: 16px;
  outline: None;
}
button {
  padding: 10px; /* Adjust padding as needed */
  font-size: 16px; /* Adjust font size as needed */
  font-weight: bold; /* Adjust font weight as needed */
  text-align: center;
  text-decoration: none;
  background-color: lightgreen;
  border-radius: 5px;
}
.red {
  color: red;
  margin: 0%;
  padding: 0%;
}
.pass {
  margin: 0%;
  padding: 0%;
}
.active {
  position: relative;
  left: -130px;
  font-size: 12px;
}
</style>
