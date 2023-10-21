<template>
  <div class="filterbox">
    <button
      :class="{ 'filter-button': true, selected: isCurrentSelected }"
      @click="showCurrent"
    >
      {{ this.currentName }}
    </button>
    <button
      :class="{ 'filter-button': true, selected: isPreviousSelected }"
      @click="showPrevious"
    >
      {{ this.previousName }}
    </button>
  </div>
</template>

<script>
export default {
  name: "RequestBar",
  emits: ["selected-option"],
  data() {
    return {
      showRequest: true,
      isCurrentSelected: true,
      isPreviousSelected: false,
    };
  },
  methods: {
    showCurrent() {
      this.showRequest = true;
      this.isCurrentSelected = true;
      this.isPreviousSelected = false;
      this.$emit("selected-option", this.isCurrentSelected);
    },
    showPrevious() {
      this.showRequest = false;
      this.isCurrentSelected = false;
      this.isPreviousSelected = true;
      this.$emit("selected-option", this.isCurrentSelected);
    },
  },
  props: ["currentName", "previousName"],
};
</script>

<style scoped>
.filterbox {
  display: flex;
  justify-content: center;
  gap: 50px;
  margin-top: 50px;
}
.filter-button {
  padding: 15px;
  background-color: white;
  cursor: pointer;
}
.filter-button:hover {
  background-color: lightblue;
}
.selected {
  background-color: lightblue;
}
</style>
