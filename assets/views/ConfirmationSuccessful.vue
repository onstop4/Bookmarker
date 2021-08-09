<template>
  <Centered class="text-center">
    <h2>Your email has been confirmed.</h2>
    <h3>Please login to continue.</h3>
    <router-link class="btn btn-primary btn-lg" :to="{ name: 'login' }"
      >Login</router-link
    >
  </Centered>
</template>

<script>
import Button from "../components/Button.vue";
import Centered from "../components/Centered.vue";

export default {
  components: {
    Button,
    Centered,
  },
};
</script>
