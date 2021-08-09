<template>
  <Centered>
    <Alert v-if="getError" class="alert-danger">{{ getError }}</Alert>
    <InputField
      v-model="email"
      @submit="submit"
      label="Email address"
      type="email"
    />
    <InputField
      v-model="password"
      @submit="submit"
      label="Password"
      type="password"
    />
    <InputField
      v-model="passwordRepeated"
      @submit="submit"
      label="Re-enter password"
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
      passwordRepeated: "",
      errorMessage: "",
    };
  },
  methods: {
    submit() {
      this.errorMessage = "";
      this.$store.commit("clearErrorMessage");
      if (this.password === this.passwordRepeated) {
        this.$store.dispatch("register", {
          email: this.email,
          password: this.password,
        });
      } else {
        this.errorMessage = "The passwords you entered don't match";
      }
    },
  },
  computed: {
    getError() {
      return this.errorMessage || this.$store.state.auth.errorMessage;
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
