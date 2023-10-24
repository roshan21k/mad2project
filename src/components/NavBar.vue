<template>
  <hamburger-menu-vue v-if="isMobile" />
  <div style="height: 75px" v-else>
    <header>
      <router-link class="logo-text" to="/">
        <div class="logo-content">
          <img class="logo" src="../assets/logo.png" />
          <span class="logo-title">Grocery Store</span>
        </div>
      </router-link>
      <nav>
        <ul>
          <router-link
            v-for="link in visibleLinks"
            :key="link.to"
            :to="link.to"
            class="link"
            style="cursor: pointer"
          >
            {{ link.text }}
          </router-link>
          <router-link
            v-if="
              isAuthenticated && (userRole === 'user' || userRole === 'manager')
            "
            :to="{ name: 'cart' }"
          >
            <img class="nav-img" src="../assets/cart.png" />
          </router-link>

          <router-link
            v-if="!isAuthenticated"
            class="link"
            :to="{ name: 'login' }"
            >Login</router-link
          >
          <router-link
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
          <router-link v-if="isAuthenticated" :to="{ name: 'about' }">
            <img class="nav-img" src="../assets/user.png" />
          </router-link>
        </ul>
      </nav>
    </header>
  </div>
</template>
<script>
import axios from "axios";
import { mapState } from "vuex";
import HamburgerMenuVue from "./HamburgerMenu.vue";
export default {
  components: { HamburgerMenuVue },
  data() {
    return {
      isMobile: false,
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
    updateMobileStatus() {
      if (window.innerWidth <= 820) {
        this.isMobile = true;
      } else {
        this.isMobile = false;
      }
    },
    async handleLogout() {
      try {
        this.isOpen = false;
        const response = await axios.delete("/auth/logout");
      } catch (error) {
        console.log(error);
      }
      this.$store.dispatch("logout");
      this.$router.push("/login");
    },
  },
  created() {
    this.updateMobileStatus();
    window.addEventListener("resize", this.updateMobileStatus);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.updateMobileStatus);
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
  /* border-bottom: 1px solid rgba(0, 0, 0, 0.399); */
  /* box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2); */
  backdrop-filter: blur(5px);
  background-color: rgba(255, 255, 255, 0.75);
}
nav {
  height: 75px;
}
ul {
  list-style: none;
  display: flex;
  flex-direction: row;
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
.logo-content {
  display: flex;
  gap: 5px;
}
.logo-text {
  text-decoration: none;
  color: green;
}
.nav-img {
  height: 30px;
  width: 30px;
  position: relative;
  top: 20px;
  margin: 0px 10px;
}
.logo-title {
  font-size: 2rem;
  font-weight: 500;
}
</style>
