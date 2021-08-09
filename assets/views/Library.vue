<template>
  You are logged in as {{ email }}.
  <div>Confirmed status: {{ $store.state.auth.userData.is_confirmed }}</div>
</template>

<script>
export default {
  computed: {
    email() {
      return this.$store.state.auth.userData.email;
    },
  },
};
</script>

<style></style>
