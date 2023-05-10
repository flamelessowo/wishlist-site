import { defineStore } from "pinia";
import {
  LOCALSTORAGE_AUTH_KEY,
  SERVER_URI,
  AUTHORIZE_PATH,
  REGISTER_PATH,
  USER_PROFILE_PATH,
  VERIFY_TOKEN_PATH,
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
    email: "",
    date_joined: null,
    birth_date: null,
    description: "",
    first_name: "",
    last_name: "",
    photo: "",
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

    async getUserAndProfile(username: string) {
      try {
        const response = await axios.get(`${SERVER_URI}${USER_PROFILE_PATH}${username}`);
        const user = response.data;
        this.username = user.username;
        this.birth_date = user.birth_date;
        this.email = user.email;
        this.date_joined = user.date_joined;
        this.first_name = user.first_name;
        this.last_name = user.last_name;
        this.description = user.description;
        this.photo = SERVER_URI + user.photo.substring(1);

        console.log(response);
      } catch(err: any) {

      }

    },
    async verifyToken(accessToken: string): Promise<boolean> {
        const response = await axios.post(`${SERVER_URI}${VERIFY_TOKEN_PATH}`, {}, {headers: {Authorization: `Bearer ${accessToken}`}});
        if (response.status = 200) {
          return true;
        }
        return false;
    },
    async loginUser(user: UserI): Promise<AxiosResponse> {
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
        return response;
      } catch (err: any) {
        throw new Error(err.response.data.message);
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
      this.email = "";
      this.date_joined = null;
      this.first_name = "";
      this.last_name = "";
      this.photo = "";
      this.accessToken = "";
      this.refreshToken = "";
      localStorage.removeItem(LOCALSTORAGE_AUTH_KEY);
    },
  },
});