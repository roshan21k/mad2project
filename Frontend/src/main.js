import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import store from "./store";
import './registerServiceWorker'
axios.interceptors.request.use((config) => {
  config.baseURL = "http://127.0.0.1:5000/";
  if (config.url === "auth/refresh") {
    config.headers.Authorization = `Bearer ${localStorage.getItem(
      "refreshToken"
    )}`;
  } else {
    config.headers.Authorization = `Bearer ${localStorage.getItem(
      "accessToken"
    )}`;
  }

  return config;
});

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (
      error.response?.status === 401 &&
      error.response?.statusText === "UNAUTHORIZED" &&
      error.response.data.msg === "Token has expired"
    ) {
      console.log("Authentication error, trying to refresh");
      try {
        const response = await axios.get("auth/refresh");
        console.log(response);
        localStorage.setItem("accessToken", response.data.access);
        error.config.headers.Authorization = `Bearer ${response.data.access}`;
        return axios(error.config);
      } catch (refreshError) {
        console.log(refreshError);
        store.dispatch("logout");
        router.push("/login");
      }
    }
    return Promise.reject(error);
  }
);
createApp(App).use(store).use(router).mount("#app");
