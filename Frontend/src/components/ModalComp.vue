<template>
  <div class="modal">
    <div class="modal-container">
      <div class="modal-content">
        <button class="close-button" @click="closeModal">x</button>
        <h1>Description</h1>
        <p>
          {{ this.content }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ModalComp",
  props: ["content", "showModal"],
  methods: {
    closeModal() {
      this.$emit("modal-closed");
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  z-index: 100;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
}
.modal-hide {
  display: none;
}
.modal-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.modal-content {
  background-color: white;
  border: 1px solid ghostwhite;
  width: 400px;
  padding: 10px;
}
.close-button {
  float: right;
  font-size: 28px;
  font-weight: bold;
  background-color: none;
  border: none;
  margin: 5px;
  cursor: pointer;
}
</style>
