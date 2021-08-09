<template>
  <Centered>
    <Alert v-if="$store.state.auth.errorMessage" class="alert-danger">{{
      $store.state.auth.errorMessage
    }}</Alert>
    <InputField
      v-model="email"
      @submit="submit"
      label="Email address"
      type="email"
    />
    <InputField
      @submit="submit"
      v-model="password"
      label="Password"
      type="password"
    />
    <Button @click="submit" text="Submit" />
  </Centered>
</template>

<script>
import Alert from "../components/Alert.vue";
import Button from "../components/Button.vue";
import Centered from "../components/Centered.vue";
import InputField from "../components/InputField.vue";

export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    submit() {
      this.$store.commit("clearErrorMessage");
      this.$store.dispatch("login", {
        email: this.email,
        password: this.password,
      });
    },
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
