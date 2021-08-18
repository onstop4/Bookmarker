<template>
  <div
    class="
      list-group-item
      d-flex
      align-items-center
      justify-content-between
      text-decoration-none
    "
  >
    <a
      :href="bookmark.url"
      :title="bookmark.name"
      class="flex-grow-1 text-truncate"
      >{{ bookmark.name }}</a
    >
    <small @click="edit" class="px-2 link-primary">Edit</small>
    <small @click="delet" class="px-2 link-primary">Delete</small>
  </div>
</template>

<script>
export default {
  methods: {
    edit() {},
    delet() {
      this.$store.dispatch("deleteBookmark", this.bookmark.id);
    },
  },
  props: {
    bookmark: {
      type: Object,
      required: true,
    },
  },
  emits: ["success", "error"],
};
</script>
