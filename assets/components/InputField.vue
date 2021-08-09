<template>
  <div class="mb-3">
    <label v-if="label" :for="fieldId" class="form-label">{{ label }}</label>
    <input
      v-model="inputVal"
      @keyup.enter="$emit('submit')"
      class="form-control"
      :id="fieldId"
      :type="type"
    />
  </div>
</template>

<script>
let uuid = 0;

export default {
  data() {
    return {
      fieldId: "",
    };
  },
  props: {
    modelValue: {
      type: String,
    },
    label: {
      type: String,
      default: "",
    },
    type: {
      type: String,
      default: "text",
    },
  },
  mounted() {
    this.fieldId = `input-${uuid++}`;
  },
  computed: {
    inputVal: {
      get() {
        return this.modelValue;
      },
      set(val) {
        this.$emit("update:modelValue", val);
      },
    },
  },
  emits: ["submit", "update:modelValue"],
};
</script>

<style></style>
