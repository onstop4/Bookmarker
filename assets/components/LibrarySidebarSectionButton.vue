<template>
  <li>
    <button
      class="btn btn-sidebar link-dark rounded my-1 text-truncate"
      :class="fontWeightClass"
    >
      <slot></slot>
    </button>
  </li>
</template>

<script>
export default {
  props: {
    buttonId: {
      type: [String, Number],
      required: false,
    },
    currentlySelected: {
      type: String,
      required: false,
    },
  },
  computed: {
    fontWeightClass() {
      // Makes button text bolder if currently selected.
      return this.buttonId && this.buttonId == this.currentlySelected
        ? "fw-bold"
        : "";
    },
  },
};
</script>

<style scoped>
.btn-sidebar {
  margin-top: 0.125rem;
  margin-left: 1.25rem;
}
.btn-sidebar:hover,
.btn-sidebar:focus {
  color: rgba(0, 0, 0, 0.85);
  background-color: #dbf1fd;
}
</style>
