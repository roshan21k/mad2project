<template>
  <h1>Welcome Admin</h1>
  <div class="container">
    <router-link class="router" :to="{ name: 'role' }">
      <div class="request">
        <h2>Role Requests</h2>
      </div>
    </router-link>
    <router-link class="router" :to="{ name: 'categoryRequests' }">
      <div class="request">
        <h2 class="">
          Manager Requests: <span class="sub-title"> Category</span>
        </h2>
      </div>
    </router-link>
    <router-link class="router" :to="{ name: 'productRequests' }">
      <div class="request">
        <h2 class="">
          Manager Requests: <span class="sub-title"> Product</span>
        </h2>
      </div>
    </router-link>
  </div>
</template>

<script>
export default {
  name: "AdminView",
};
</script>
<style scoped>
.container {
  display: flex;
  justify-content: space-evenly;
  flex-wrap: wrap;
  gap: 25px;
  margin-bottom: 50px;
}
.request {
  border: 1px solid black;
  border-radius: 75px;
  width: 300px;
  height: 150px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: aliceblue;
}
.request:hover {
  background-color: lightblue;
}
.sub-title {
  font-weight: lighter;
}
h1 {
  text-align: center;
  margin: 100px 0px;
}
h2 {
  text-align: center;
}
.router {
  text-decoration: none;
  color: black;
}
</style>
