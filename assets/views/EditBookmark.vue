<template>
  <Centered>
    <Alert v-if="$store.state.library.errorMessage" class="alert-danger">{{
      $store.state.library.errorMessage
    }}</Alert>
    <InputField v-model="name" @submit="submit" label="Name" />
    <InputField v-model="url" @submit="submit" label="Name" />
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
      unread: false,
      selectedList: "null",
      newListName: "",
    };
  },
  methods: {
    async submit() {
      let listId = this.selectedList;
      let listFound = true;

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

      if (listFound) {
        const response = await this.$store.dispatch("editBookmark", {
          id: this.realId,
          name: this.name,
          url: this.url,
          unread: this.unread,
          list: listId,
        });

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
    this.realId = Number(this.id);
    // Goes to library if realId is 0 or NaN, which could be the case in a
    // malformed url parameter.
    if (!this.realId) {
      console.log(this.realId);
      this.$router.push({ name: "library" });
    }
    axios
      .get(`/api/bookmarks/${this.realId}/`, this.$store.state.auth.axiosConfig)
      .then((response) => {
        const data = response.data;
        this.name = data.name;
        this.url = data.url;
        this.unread = data.unread;
        this.selectedList = data.list ? data.list : "null";
      })
      .catch(() => {
        console.log("could not get data");
        this.$router.push({ name: "library" });
      });
    this.$store.dispatch("updateLists");
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
      required: true,
    },
  },
};
</script>

<style></style>
