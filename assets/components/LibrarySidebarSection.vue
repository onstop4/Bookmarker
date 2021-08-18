<template>
  <li class="mb-1">
    <button
      @click="expanded = !expanded"
      class="btn btn-sidebar btn-toggle rounded collapsed"
      :aria-expanded="expanded"
    >
      {{ text }}
    </button>
    <div v-if="expanded">
      <ul class="btn-toggle-nav list-unstyled pb-3">
        <slot></slot>
      </ul>
    </div>
  </li>
</template>

<script>
export default {
  data() {
    return { expanded: this.expandedByDefault };
  },
  props: {
    text: {
      type: String,
      required: true,
    },
    expandedByDefault: {
      type: String,
      default: "true",
    },
  },
};
</script>

<style>
.btn-sidebar {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background-color: transparent;
  border: 0;
}
.btn-sidebar:hover,
.btn-sidebar:focus {
  color: rgba(0, 0, 0, 0.85);
  background-color: #dbf1fd;
}

.btn-toggle::before {
  width: 1.25em;
  line-height: 0;
  content: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='rgba%280,0,0,.5%29' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 14l6-6-6-6'/%3e%3c/svg%3e");
  transition: transform 0.35s ease;
  transform-origin: 0.5em 50%;
}

.btn-toggle[aria-expanded="true"] {
  color: rgba(0, 0, 0, 0.85);
}
.btn-toggle[aria-expanded="true"]::before {
  transform: rotate(90deg);
}
</style>
