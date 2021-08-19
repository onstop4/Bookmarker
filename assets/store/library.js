import axios from "axios";

const bookmarkSaveErrorMessage =
  "Error saving bookmark. Please check the fields and try again.";
const listSaveErrorMessage =
  "Error creating new list. Please check the fields and try again.";

const state = {
  bookmarks: [],
  lists: [],
  filters: {
    list: undefined,
    unread: undefined,
    search: undefined,
  },
  errorMessage: "",
  loading: false,
};

const getters = {};

const actions = {
  updateBookmarks({ commit }, payload) {
    // "params" stores values that will be used to filter the query results.
    const params = [];
    if (payload.list) {
      params.push(`list=${payload.list}`);
    }
    if (payload.unread) {
      params.push("unread=true");
    }
    if (payload.search) {
      params.push(`search=${payload.search}`);
    }
    return axios
      .get(`/api/bookmarks/${params ? `?${params.join("&")}` : ""}`)
      .then((response) => {
        commit("updateBookmarks", { data: response.data, filters: payload });
        commit("setLibraryError", "");
      })
      .catch(() => {
        commit("setLibraryError", "Error fetching data.");
      });
  },
  updateLists({ commit }) {
    return axios
      .get("/api/lists/")
      .then((response) => {
        commit("updateLists", response.data);
        commit("setLibraryError", "");
      })
      .catch(() => {
        commit("setLibraryError", "Error fetching data.");
      });
  },
  createList({ commit, rootState }, listName) {
    return axios
      .post("/api/lists/", { name: listName }, rootState.auth.axiosConfig)
      .catch(() => {
        commit("setLibraryError", listSaveErrorMessage);
      });
  },
  editBookmark({ commit, rootState }, payload) {
    return axios
      .patch(
        `/api/bookmarks/${payload.id}/`,
        payload,
        rootState.auth.axiosConfig
      )
      .catch(() => {
        commit("setLibraryError", bookmarkSaveErrorMessage);
      });
  },
  deleteBookmark({ commit, rootState }, bookmarkId) {
    return axios
      .delete(`/api/bookmarks/${bookmarkId}/`, rootState.auth.axiosConfig)
      .then(() => {
        commit("deleteBookmark", bookmarkId);
        commit("setLibraryError", "");
      })
      .catch(() => {
        commit("setLibraryError", "Error deleting bookmark.");
      });
  },
};

const mutations = {
  updateBookmarks(state, payload) {
    state.bookmarks = payload.data;
    state.filters = payload.filters;
  },
  updateLists(state, data) {
    state.lists = data;
  },
  deleteBookmark(state, bookmarkId) {
    state.bookmarks.splice(
      state.bookmarks.findIndex((i) => i.id === bookmarkId),
      1
    );
  },
  setLibraryError(state, errorMessage) {
    state.errorMessage = errorMessage;
  },
  setLoading(state, loading) {
    state.loading = loading;
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
