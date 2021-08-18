import { createRouter, createWebHistory } from "vue-router";
import store from "../store";
import ConfirmationRequired from "../views/ConfirmationRequired.vue";
import ConfirmationSuccessful from "../views/ConfirmationSuccessful.vue";
import Index from "../views/Index.vue";
import Library from "../views/Library.vue";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";

function requireLogin(to) {
  return store.state.auth.authenticated
    ? true
    : { path: "login", query: { to: to.path } };
}

function handleExistingLogin() {
  if (store.state.auth.authenticated) {
    store.commit("login");
  } else {
    return true;
  }
}

const routes = [
  {
    path: "/",
    component: Index,
    beforeEnter: (to, from) => {
      if (store.state.auth.authenticated) {
        return "/app/";
      }
      return true;
    },
  },
  {
    path: "/app/",
    name: "library",
    component: Library,
    beforeEnter: requireLogin,
  },
  {
    path: "/login/",
    name: "login",
    component: Login,
    beforeEnter: handleExistingLogin,
  },
  {
    path: "/register/",
    name: "register",
    component: Register,
    beforeEnter: handleExistingLogin,
  },
  {
    path: "/confirm/",
    name: "confirm",
    component: ConfirmationRequired,
  },
  {
    path: "/confirmed/",
    name: "confirmSuccess",
    component: ConfirmationSuccessful,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from) => {
  if (to.name && to.name === from.name) {
    return;
  }
  await store.dispatch("setCSRFToken");
  await store.dispatch("updateUserData");
});

export default router;
