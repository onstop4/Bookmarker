import { createRouter, createWebHistory } from "vue-router";
import store from "../store";
import ConfirmationRequired from "../views/ConfirmationRequired.vue";
import ConfirmationSuccessful from "../views/ConfirmationSuccessful.vue";
import EditBookmark from "../views/EditBookmark.vue";
import EditList from "../views/EditList.vue";
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
    beforeEnter: () => {
      if (store.state.auth.authenticated) {
        return "/app/";
      }
      return true;
    },
  },
  {
    path: "/:url(http.*)",
    redirect: (to) => {
      return { name: "createBookmark", query: { save: to.params.url } };
    },
  },
  {
    path: "/app/",
    name: "library",
    component: Library,
    beforeEnter: requireLogin,
  },
  {
    path: "/app/edit/:id/",
    name: "editBookmark",
    component: EditBookmark,
    beforeEnter: requireLogin,
    props: true,
  },
  {
    path: "/app/create/",
    name: "createBookmark",
    component: EditBookmark,
    beforeEnter: requireLogin,
    props: true,
  },
  {
    path: "/app/rename/:listId/",
    name: "renameList",
    component: EditList,
    beforeEnter: requireLogin,
    props: true,
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
