<template>
  <button @click="$emit('click')" type="button" class="btn btn-primary">
    {{ text }}
  </button>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      required: true,
    },
  },
  emits: ["click"],
};
</script>

<style></style>
