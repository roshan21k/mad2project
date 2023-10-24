<template>
  <div style="height: 75px">
    <header>
      <router-link to="/" @click="isOpen = false">
        <img class="logo" src="../assets/logo.png" />
      </router-link>
      <button @click="isOpen = !isOpen" class="hamburger-button">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
      </button>
    </header>
  </div>
  <nav>
    <ul :class="{ open: isOpen, close: !isOpen }">
      <router-link
        @click="isOpen = false"
        v-for="link in visibleLinks"
        :key="link.to"
        :to="link.to"
        class="link"
        style="cursor: pointer"
      >
        {{ link.text }}
      </router-link>
      <router-link
        @click="isOpen = false"
        v-if="
          isAuthenticated && (userRole === 'user' || userRole === 'manager')
        "
        :to="{ name: 'cart' }"
        class="link"
      >
        <img class="nav-img" src="../assets/cart.png" />
      </router-link>
      <router-link
        @click="isOpen = false"
        v-if="!isAuthenticated"
        class="link"
        :to="{ name: 'login' }"
        >Login</router-link
      >
      <router-link
        @click="isOpen = false"
        v-if="!isAuthenticated"
        class="link"
        :to="{ name: 'signup' }"
        >Sign-Up</router-link
      >

      <a
        v-if="isAuthenticated"
        class="link"
        @click="handleLogout"
        style="cursor: pointer"
      >
        Logout
      </a>
      <router-link
        v-if="isAuthenticated"
        :to="{ name: 'about' }"
        class="link"
        @click="isOpen = false"
      >
        <img class="nav-img" src="../assets/user.png" />
      </router-link>
    </ul>
  </nav>
</template>
<script>
import axios from "axios";
import { mapState } from "vuex";
export default {
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    ...mapState(["isAuthenticated", "userRole"]),
    visibleLinks() {
      const links = [];

      if (this.isAuthenticated) {
        if (this.userRole === "admin") {
          links.push({ to: { name: "admin" }, text: "Home" });
        } else if (this.userRole === "user") {
          links.push({ to: { name: "apply" }, text: "Apply" });
          links.push({ to: { name: "home" }, text: "Home" });
          links.push({ to: { name: "order" }, text: "Orders" });
        } else if (this.userRole === "manager") {
          links.push({ to: { name: "home" }, text: "Home" });
          links.push({ to: { name: "order" }, text: "Orders" });
          links.push({ to: { name: "manage" }, text: "Manage" });
          links.push({ to: { name: "export" }, text: "Export" });
        }
      }

      return links;
    },
  },
  methods: {
    async handleLogout() {
      this.isOpen = false;
      try {
        const response = await axios.delete("/auth/logout");
      } catch (error) {
        console.log(error);
      }
      this.$store.dispatch("logout");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body {
  margin: 0;
  padding: 0;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0px 20px 0px 20px;
  position: fixed;
  width: 100%;
  z-index: 1;
  backdrop-filter: blur(5px);
  background-color: rgba(255, 255, 255, 0.75);
  height: 75px;
}
ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;
  width: 100%;
  border-bottom: 1px solid rgba(0, 0, 0, 0.399);
  backdrop-filter: blur(5px);
  background-color: rgba(255, 255, 255, 0.75);
  gap: 20px;
}
.link {
  text-decoration: none;
  color: grey;
  line-height: 75px;
  transition: all 0.3s ease;
}
.link:hover {
  color: rgb(0, 0, 0);
  text-decoration: underline;
}
.logo {
  height: 40px;
  width: 40px;
}
.nav-img {
  height: 30px;
  width: 30px;
  position: relative;
  top: 20px;
}
.hamburger-button {
  cursor: pointer;
  background: none;
  border: none;
}

.bar {
  width: 30px;
  height: 3px;
  background: #000000;
  margin: 6px 0;
  transition: 0.4s;
}
.open {
  transform: translateX(0%);
  transition: transform 0.5s ease-in-out;
}

.close {
  transform: translateX(-100%);
  transition: transform 0.5s ease-in-out;
}
</style>
