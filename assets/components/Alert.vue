<template>
  <div class="alert" role="alert">
    <slot></slot>
    <button
      v-if="closable"
      @click="$emit('close')"
      type="button"
      class="btn-close"
      aria-label="Close"
    ></button>
  </div>
</template>

<script>
export default {
  props: {
    closable: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["close"],
};
</script>

<style></style>
