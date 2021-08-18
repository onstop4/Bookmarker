import { createStore } from "vuex";
import auth from "./auth.js";
import library from "./library.js";

export default createStore({
  modules: {
    auth,
    library,
  },
});
