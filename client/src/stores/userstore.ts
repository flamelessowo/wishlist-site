import { defineStore } from "pinia";
import {
  LOCALSTORAGE_AUTH_KEY,
  SERVER_URI,
  AUTHORIZE_PATH,
  REGISTER_PATH,
} from "@/core/constants";
import axios, { type AxiosResponse } from "axios";

interface UserI {
  username: string;
  password: string;
}

export const useUserStore = defineStore("users", {
  state: () => ({
    username: "",
    password: "",
    accessToken: "",
    refreshToken: "",
  }),
  getters: {
    isAuthenticated: (state) => {
      if (state.accessToken) {
        return true;
      }
      return false;
    },
    getUser: (state) => {
      if (state.username) {
        return {
          username: state.username,
        };
      }
      return null;
    },
    getTokens: (state) => {
      if (state.accessToken) {
        return {
          accessToken: state.accessToken,
          refreshToken: state.refreshToken,
        };
      }
      return null;
    },
  },
  actions: {
    setUser(username: string) {
      this.username = username;
    },
    setTokens(refreshToken: string, accessToken: string) {
      this.refreshToken = refreshToken;
      this.accessToken = accessToken;
    },
    destroyTokens() {
      this.refreshToken = "";
      this.accessToken = "";
    },
    async loginUser(user: UserI): Promise<boolean> {
      try {
        const response = await axios.post(`${SERVER_URI}${AUTHORIZE_PATH}`, {
          username: user.username,
          password: user.password,
        });
        this.setTokens(response.data.refresh, response.data.access);
        this.setUser(user.username);
        localStorage.setItem(
          LOCALSTORAGE_AUTH_KEY,
          JSON.stringify({ ...this.getTokens, ...this.getUser })
        );
        return true;
      } catch (err) {
        return false;
      }
    },
    async registerUser(user: UserI): Promise<AxiosResponse> {
      try {
        const response = await axios.post(`${SERVER_URI}${REGISTER_PATH}`, {
        username: user.username,
        password: user.password,
      });
        return response;
      } catch(err: any) {
        console.log(err)
        throw new Error(err.response.data.message);
      }
      
    },
    logout(): void {
      this.username = "";
      this.password = "";
      this.accessToken = "";
      this.refreshToken = "";
      localStorage.removeItem(LOCALSTORAGE_AUTH_KEY);
    },
  },
});