import axios from "axios";
import router from "../router";

function createURLParams(obj) {
  const params = new URLSearchParams();
  for (const property in obj) {
    params.append(property, obj[property]);
  }
  return params;
}

const state = {
  authenticated: localStorage.getItem("authenticated") || "",
  userData: {},
  axiosConfig: { headers: { "X-CSRFToken": undefined } },
  errorMessage: "",
  route: undefined,
};

const getters = {};

const actions = {
  setCSRFToken({ commit }) {
    return axios.get("/api/set-cookie/").then(() => {
      const tokenCookie = document.cookie
        .split("; ")
        .find((row) => row.startsWith("csrftoken="))
        .split("=")[1];
      commit("setCSRFToken", tokenCookie);
    });
  },
  login({ dispatch, commit, state }, payload) {
    return axios
      .post("/api/login/", createURLParams(payload), state.axiosConfig)
      .then(() => dispatch("updateUserData"))
      .then(() => {
        commit("login");
      })
      .catch((err) => {
        commit("authError", err);
      });
  },
  register({ dispatch, commit, state }, payload) {
    return axios
      .post("/api/register/", createURLParams(payload), state.axiosConfig)
      .then(() => dispatch("updateUserData"))
      .then(() => {
        commit("register");
      })
      .catch((err) => {
        commit("authError", err);
      });
  },
  updateUserData({ commit }) {
    return axios
      .get("/api/user/", state.axiosConfig)
      .then((response) => {
        commit("updateUserData", response.data);
      })
      .catch((err) => {
        commit("authError", err);
      });
  },
  logout({ commit }) {
    return axios
      .post("/api/logout/", createURLParams({}), state.axiosConfig)
      .then(() => {
        commit("logout");
      });
  },
};

const mutations = {
  clearErrorMessage(state) {
    state.errorMessage = "";
  },
  setCSRFToken(state, token) {
    state.axiosConfig.headers["X-CSRFToken"] = token;
  },
  login(state) {
    if (state.route.query) {
      if (state.route.query.save) {
        router.push({
          name: "createBookmark",
          query: { save: state.route.query.save },
        });
        return;
      } else if (state.route.query.to) {
        router.push(state.route.query.to);
        return;
      }
    }
    router.push({ name: "library" });
  },
  register() {
    router.push({ name: "confirm" });
  },
  updateUserData(state, data) {
    state.authenticated = true;
    localStorage.setItem("authenticated", "true");
    state.userData = data;
  },
  authError(state, err) {
    state.authenticated = "";
    localStorage.setItem("authenticated", "");
    try {
      if (err.response.status === 403) {
        state.errorMessage = "";
      } else {
        state.errorMessage =
          err.response.data.error || err.response.data.detail;
      }
    } catch (e) {
      state.errorMessage = "An unknown error occurred during authentication.";
    }
  },
  setRoute(state, route) {
    state.route = route;
  },
  logout() {
    router.push({ name: "index" });
  },
};

const modules = {};

export default {
  state,
  getters,
  actions,
  mutations,
  modules,
};
