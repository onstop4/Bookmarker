<template>
  <Centered>
    <Alert v-if="$store.state.library.errorMessage" class="alert-danger">{{
      $store.state.library.errorMessage
    }}</Alert>
    <InputField v-model="name" @submit="submit" label="Name" />
    <InputField v-model="url" @submit="submit" label="URL" />
    <div class="form-check">
      <input
        class="form-check-input"
        type="checkbox"
        value=""
        id="unread-status"
        v-model="unread"
      />
      <label class="form-check-label" for="unread-status">Unread</label>
    </div>
    <label for="select-list" class="form-label">List</label>
    <select v-model="selectedList" id="select-list" class="form-select mb-3">
      <option value="null">No list</option>
      <option value="new list">Create new list</option>
      <option disabled>----------</option>
      <option
        v-for="list in $store.state.library.lists"
        :key="list.id"
        :value="list.id"
      >
        {{ list.name }}
      </option>
    </select>
    <InputField
      v-if="selectedList === 'new list'"
      v-model="newListName"
      @submit="submit"
      label="New list name"
    />
    <Button @click="submit" text="Submit" />
  </Centered>
</template>

<script>
import axios from "axios";
import Alert from "../components/Alert.vue";
import Button from "../components/Button.vue";
import Centered from "../components/Centered.vue";
import InputField from "../components/InputField.vue";

export default {
  data() {
    return {
      realId: undefined,
      name: "",
      url: "",
      unread: true,
      selectedList: "null",
      newListName: "",
    };
  },
  methods: {
    setUpCreate() {
      this.url = this.$route.query.save;
    },
    setUpEdit() {
      this.realId = Number(this.id);
      // Goes to library if realId is 0 or NaN, which could be the case in a
      // malformed url parameter.
      if (!this.realId) {
        this.$router.push({ name: "library" });
      }
      axios
        .get(
          `/api/bookmarks/${this.realId}/`,
          this.$store.state.auth.axiosConfig
        )
        .then((response) => {
          const data = response.data;
          this.name = data.name;
          this.url = data.url;
          this.unread = data.unread;
          this.selectedList = data.list ? data.list : "null";
        })
        .catch(() => {
          this.$router.push({ name: "library" });
        });
      this.$store.dispatch("updateLists");
    },
    async submit() {
      if (
        !(this.url.startsWith("http://") || this.url.startsWith("https://"))
      ) {
        this.$store.commit("useDefaultLibraryError");
        return;
      }

      let listId = this.selectedList;
      let listFound = true;

      // Attempts to create a new list (or uses existing one or null).
      if (listId === "null") {
        listId = null;
      } else if (listId === "new list") {
        try {
          listId = (await this.$store.dispatch("createList", this.newListName))
            .data.id;
        } catch (e) {
          listFound = false;
        }
      } else {
        listId = Number(listId);
      }

      // Only creates bookmark if the previous step (of using an existing list
      // or creating a new one) didn't fail.
      if (listFound) {
        const response = await this.$store.dispatch(
          this.realId ? "editBookmark" : "createBookmark",
          Object.assign(
            {
              name: this.name,
              url: this.url,
              unread: this.unread,
              list: listId,
            },
            this.realId ? { id: this.realId } : {}
          )
        );

        if (response) {
          this.$router.push(
            Object.assign(
              { name: "library" },
              listId ? { query: { list: listId } } : {}
            )
          );
        }
      }
    },
  },
  mounted() {
    this.$store.dispatch("updateLists");
    if (this.$route.query.save) {
      this.setUpCreate();
    } else {
      this.setUpEdit();
    }
  },
  components: {
    Alert,
    Button,
    Centered,
    InputField,
  },
  props: {
    id: {
      type: String,
      default: "0",
    },
  },
};
</script>

<style></style>
