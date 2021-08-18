<template>
  <div class="p-3 bg-white w-25 library-scrollarea">
    <ul class="list-unstyled">
      <LibrarySidebarSection text="Bookmarks">
        <LibrarySidebarSectionButton
          buttonId="all"
          :currentlySelected="currentlySelected"
          @click="update('all')"
          >Show all</LibrarySidebarSectionButton
        >
        <LibrarySidebarSectionButton
          buttonId="unread"
          :currentlySelected="currentlySelected"
          @click="update('unread')"
          >Unread</LibrarySidebarSectionButton
        >
      </LibrarySidebarSection>
      <LibrarySidebarSection text="Lists">
        <LibrarySidebarSectionButton
          v-for="list in $store.state.library.lists"
          :key="list.id"
          :buttonId="list.id"
          :currentlySelected="currentlySelected"
          :title="list.name"
          @click="update(list.id)"
          >{{ list.name }}</LibrarySidebarSectionButton
        >
      </LibrarySidebarSection>
    </ul>
  </div>
</template>

<script>
import LibrarySidebarSection from "./LibrarySidebarSection.vue";
import LibrarySidebarSectionButton from "./LibrarySidebarSectionButton.vue";

export default {
  methods: {
    update(requested) {
      const params = {};
      if (requested === "unread") {
        params.unread = "true";
      } else if (Number(requested)) {
        params.list = requested;
      }
      this.$router.push({ name: "library", query: params });
    },
  },
  computed: {
    currentlySelected() {
      return (
        this.$store.state.library.filters.list ||
        (this.$store.state.library.filters.unread ? "unread" : "") ||
        "all"
      );
    },
  },
  components: {
    LibrarySidebarSection,
    LibrarySidebarSectionButton,
  },
};
</script>
