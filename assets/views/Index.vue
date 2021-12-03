<template>
  <Centered>
    <div class="my-5 p-4 text-center container">
      <h1>Welcome to Bookmarker</h1>
      <div class="d-grid gap-2 d-sm-flex justify-content-center">
        <router-link class="btn btn-primary btn-lg" :to="{ name: 'login' }"
          >Login</router-link
        >
        <router-link class="btn btn-primary btn-lg" :to="{ name: 'register' }"
          >Register</router-link
        >
      </div>
    </div>
  </Centered>
</template>

<script>
import Centered from "../components/Centered.vue";

export default {
  components: {
    Centered,
  },
};
</script>

<style scoped>
.container {
  background-color: var(--bs-gray-400);
}
</style>
