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
    <a :href="bookmark.url" class="flex-grow-1">{{ bookmark.name }}</a>
    <router-link
      class="small text-decoration-none px-2 link-primary"
      :to="{ name: 'editBookmark', params: { id: bookmark.id } }"
      >Edit</router-link
    >
    <a
      @click.prevent="delet"
      class="small text-decoration-none px-2 link-primary"
      href=""
      >Delete</a
    >
  </div>
</template>

<script>
export default {
  methods: {
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
