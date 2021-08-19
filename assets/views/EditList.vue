<template>
  <Centered>
    <Alert v-if="$store.state.library.errorMessage" class="alert-danger">{{
      $store.state.library.errorMessage
    }}</Alert>
    <InputField v-model="name" @submit="submit" label="Name" />
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
      name: "",
    };
  },
  methods: {
    getList() {
      if (!Number(this.listId) || Number(this.listId) <= 0) {
        this.$router.push({ name: "library" });
      }
      axios.get(`/api/lists/${this.listId}/`).then((response) => {
        this.name = response.data.name;
      });
    },
    submit() {
      this.$store
        .dispatch("editList", { id: this.listId, name: this.name })
        .then((response) => {
          if (response) {
            this.$router.push({
              name: "library",
              query: { list: this.listId },
            });
          }
        });
    },
  },
  props: {
    listId: {
      type: String,
      required: true,
    },
  },
  mounted() {
    this.getList();
  },
  components: {
    Alert,
    Button,
    Centered,
    InputField,
  },
};
</script>

<style></style>
