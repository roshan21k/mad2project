import { createStore } from "vuex";

export default createStore({
  state: {
    isAuthenticated: false,
    userRole: null,
  },
  getters: {},
  mutations: {
    setAuthenticated(state, status) {
      state.isAuthenticated = status;
    },
    setUserRole(state, role) {
      state.userRole = role;
    },
    logoutUser(state) {
      (state.isAuthenticated = false), (state.userRole = false);
      localStorage.removeItem("userRole");
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
    },
  },
  actions: {
    logout({ commit }) {
      commit("logoutUser");
    },
  },
  modules: {},
});
