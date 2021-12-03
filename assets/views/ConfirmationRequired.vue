<template>
  <Centered class="text-center">
    <h2>Email address confirmation required.</h2>
    <h3>Please check your email.</h3>
    <Button @click="resendEmail" text="Resend confirmation email" />
  </Centered>
</template>

<script>
import axios from "axios";
import Button from "../components/Button.vue";
import Centered from "../components/Centered.vue";

export default {
  methods: {
    resendEmail() {
      axios.post(
        "/api/resend-confirmation/",
        {},
        this.$store.state.auth.axiosConfig
      );
    },
  },
  components: {
    Button,
    Centered,
  },
};
</script>
