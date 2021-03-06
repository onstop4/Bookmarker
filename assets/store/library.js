import axios from "axios";

const bookmarkSaveErrorMessage =
  "Error saving bookmark. Please check the fields and try again.";
const listSaveErrorMessage =
  "Error saving list. Please check the fields and try again.";

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
        return response;
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
        return response;
      })
      .catch(() => {
        commit("setLibraryError", "Error fetching data.");
      });
  },
  createBookmark({ commit, rootState }, payload) {
    return axios
      .post("/api/bookmarks/", payload, rootState.auth.axiosConfig)
      .then((response) => {
        commit("setLibraryError", "");
        return response;
      })
      .catch(() => {
        commit("setLibraryError", bookmarkSaveErrorMessage);
      });
  },
  createList({ commit, rootState }, listName) {
    return axios
      .post("/api/lists/", { name: listName }, rootState.auth.axiosConfig)
      .then((response) => {
        commit("setLibraryError", "");
        return response;
      })
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
      .then((response) => {
        commit("setLibraryError", "");
        return response;
      })
      .catch(() => {
        commit("setLibraryError", bookmarkSaveErrorMessage);
      });
  },
  editList({ commit, rootState }, payload) {
    return axios
      .patch(
        `/api/lists/${payload.id}/`,
        { name: payload.name },
        rootState.auth.axiosConfig
      )
      .then((response) => {
        commit("setLibraryError", "");
        return response;
      })
      .catch(() => {
        commit("setLibraryError", listSaveErrorMessage);
      });
  },
  deleteBookmark({ commit, rootState }, bookmarkId) {
    return axios
      .delete(`/api/bookmarks/${bookmarkId}/`, rootState.auth.axiosConfig)
      .then((response) => {
        commit("deleteBookmark", bookmarkId);
        commit("setLibraryError", "");
        return response;
      })
      .catch(() => {
        commit("setLibraryError", "Error deleting bookmark.");
      });
  },
  deleteList({ commit, state, rootState, dispatch }, includeRelated) {
    const currentList = state.filters.list;
    return axios
      .delete(
        `/api/lists/${currentList}/` +
          (includeRelated ? "include-related/" : ""),
        rootState.auth.axiosConfig
      )
      .then((response) => {
        commit("setLibraryError", "");
        commit("deleteList", currentList);
        return response;
      })
      .catch((e) => {
        commit("setLibraryError", "Error deleting list.");
        throw e;
      });
  },
  markAsRead({ rootState }, bookmarkId) {
    return axios
      .patch(
        `/api/bookmarks/${bookmarkId}/`,
        { unread: false },
        Object.assign({ timeout: 1000 }, rootState.auth.axiosConfig)
      )
      .catch(() => {
        // There is no point displaying an error message since the method that
        // called markAsRead should still go to the bookmark's url regardless of
        // any error.
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
  deleteList(state, listId) {
    state.lists.splice(
      state.lists.findIndex((i) => i.id === listId),
      1
    );
  },
  setLibraryError(state, errorMessage) {
    state.errorMessage = errorMessage;
  },
  useDefaultLibraryError(state) {
    state.errorMessage = bookmarkSaveErrorMessage;
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
