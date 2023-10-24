<template>
  <div class="center">
    <div class="not-found">
      <span class="number">404</span>
      <spa class="text">Not Found</spa>
      <span>The page you are looking for is not found in our server!</span>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.center {
  display: flex;
  min-height: calc(100vh - 80px);
  justify-content: center;
  align-items: center;
}
.not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.number {
  font-weight: bold;
  font-size: 10rem;
}
.text {
  font-weight: lighter;
  font-size: 2rem;
}
</style>
