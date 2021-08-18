<template>
  <div class="d-flex flex-column align-items-stretch flex-grow-1 bg-white p-3">
    <Alert v-if="$store.state.library.errorMessage" class="alert-danger">{{
      $store.state.library.errorMessage
    }}</Alert>
    <div
      class="
        d-flex
        align-items-center
        flex-shrink-0
        p-3
        link-dark
        text-decoration-none
        border-bottom
      "
    >
      <InputField v-model="searchText" label="Search" />
    </div>
    <div
      v-if="$store.state.library.loading"
      class="d-flex flex-column align-items-center p-3"
    >
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div
      v-else-if="$store.state.library.bookmarks.length"
      class="list-group list-group-flush border-bottom library-scrollarea"
    >
      <LibraryBookmarkDisplayItem
        v-for="bookmark in $store.state.library.bookmarks"
        :key="bookmark.id"
        :bookmark="bookmark"
      />
    </div>
    <p v-else class="p-3 text-center">No bookmarks found.</p>
  </div>
</template>

<script>
import Alert from "./Alert.vue";
import InputField from "./InputField.vue";
import LibraryBookmarkDisplayItem from "./LibraryBookmarkDisplayItem.vue";

let searchTimer;
const searchDelay = 500;

export default {
  data() {
    return {
      searchText: this.$route.query.search,
    };
  },
  methods: {
    search() {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(() => {
        const params = Object.assign(
          {
            unread: this.$store.state.library.filters.unread,
            list: this.$store.state.library.filters.list,
          },
          this.searchText ? { search: this.searchText } : {}
        );
        this.$router.push({ name: "library", query: params });
      }, searchDelay);
    },
  },
  watch: {
    searchText() {
      this.search();
    },
  },
  components: {
    Alert,
    InputField,
    LibraryBookmarkDisplayItem,
  },
};
</script>

<style scoped></style>
