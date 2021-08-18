<template>
  <div class="library-main">
    <LibrarySidebar />
    <LibraryDivider />
    <LibraryBookmarkDisplay />
  </div>
</template>

<script>
import LibraryBookmarkDisplay from "../components/LibraryBookmarkDisplay.vue";
import LibraryDivider from "../components/LibraryDivider.vue";
import LibrarySidebar from "../components/LibrarySidebar.vue";

export default {
  methods: {
    update(query) {
      this.$store.commit("setLoading", true);
      const payload = {
        unread: query.unread,
        list: query.list,
        search: query.search,
      };
      this.$store
        .dispatch("updateBookmarks", payload)
        .then(() => {
          this.$store.commit("setLoading", false);
        })
        .catch(() => {
          this.$store.commit("setLoading", false);
          this.$store.commit("setLibraryError", "Error fetching data.");
        });
    },
  },
  mounted() {
    this.$store.dispatch("updateLists");
    this.update(this.$route.query);
  },
  beforeRouteUpdate(to) {
    this.update(to.query);
  },
  components: {
    LibraryBookmarkDisplay,
    LibraryDivider,
    LibrarySidebar,
  },
};
</script>

<style>
.library-main {
  display: flex;
  flex-wrap: nowrap;
  height: 100vh;
  height: -webkit-fill-available;
  max-height: 100vh;
  overflow-x: auto;
  overflow-y: hidden;
}

.library-scrollarea {
  overflow-y: auto;
}
</style>
