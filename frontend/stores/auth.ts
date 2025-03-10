import { normalFetch } from "./../composables/useAPIFetch";
import { defineStore } from "pinia";
import { autoFetch } from "../composables/useAPIFetch";
export const useAuthStore = defineStore("auth", {
  state: () => ({
    user_data: null,
    accessToken: null,
    accessTokenExpiry: null,
    refreshToken: null,
    refreshTokenExpiry: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.user_data,
  },
  actions: {
    async getUserData() {
      if (this.accessToken) {
        const userResponse = await autoFetch(`/account/details`, {
          method: "GET",
        });
        if (!userResponse.ok) {
          const errorText = await userResponse.text();
          console.log(`User request failed: ${errorText}`);
        }
        this.user_data = await userResponse.json();
      }
    },

    async login({
      username,
      password,
    }: {
      username: string;
      password: string;
    }) {
      try {
        const loginResponse = await normalFetch(`/auth/login/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });

        if (!loginResponse.ok) {
          const errorText = await loginResponse.json();
          return { status: false, message: errorText.error };
        }

        const { access, refresh } = await loginResponse.json();

        const expirationTime = new Date().getTime() + 12 * 60 * 60 * 1000;
        const accessExpirationTime = new Date().getTime() + 5 * 60 * 1000;

        this.setTokens({
          accessToken: access,
          refreshToken: refresh,
          refreshTokenExpiry: expirationTime,
          accessTokenExpiry: accessExpirationTime,
        });
      } catch (error) {
        console.error("Login Error:", error);
        return "";
      }
    },

    async getTokens() {
      const accessExpirationTime = new Date().getTime();
      const refreshToken = this.refreshToken;
      if (refreshToken) {
        try {
          const refreshExpirationTime = this.refreshTokenExpiry;
          if (
            refreshExpirationTime &&
            new Date().getTime() > parseInt(refreshExpirationTime)
          ) {
            console.log("Token Refresh Expired");
            this.logout();
          }

          const accessExpirationTime = this.accessTokenExpiry;
          if (
            accessExpirationTime &&
            new Date().getTime() > parseInt(accessExpirationTime)
          ) {
            const refreshResponse = await normalFetch(`/auth/refresh/`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ refresh: refreshToken }),
            });

            if (!refreshResponse.ok) {
              const errorText = await refreshResponse.text();
              this.logout();
            }

            const { access } = await refreshResponse.json();
            const newAccessExpirationTime =
              new Date().getTime() + 5 * 60 * 1000;

            this.setAccessTokens({
              accessToken: access,
              accessTokenExpiry: newAccessExpirationTime,
            });
          }
        } catch (refreshError) {
          console.error("Token Refresh Error:", refreshError);
          throw refreshError;
        }
        await this.getUserData();
        return this.accessToken;
      } else {
        this.logout();
        return null;
      }
    },

    async setTokens({
      accessToken,
      refreshToken,
      refreshTokenExpiry,
      accessTokenExpiry,
    }: {
      accessToken: string;
      refreshToken: string;
      refreshTokenExpiry: string;
      accessTokenExpiry: string;
    }) {
      this.accessToken = accessToken;
      this.refreshToken = refreshToken;
      this.refreshTokenExpiry = refreshTokenExpiry;
      this.accessTokenExpiry = accessTokenExpiry;
      await this.getUserData();
      return navigateTo("/dashboard");
    },
    async setAccessTokens({
      accessToken,
      accessTokenExpiry,
    }: {
      accessToken: string;
      accessTokenExpiry: string;
    }) {
      this.accessToken = accessToken;
      this.accessTokenExpiry = accessTokenExpiry;
    },
    async logout() {
      await this.setTokens({
        accessToken: null,
        refreshToken: null,
        refreshTokenExpiry: null,
        accessTokenExpiry: null,
      });
      this.user_data = null;
      console.log("logout");
      return navigateTo("/");
    },
  },
  persist: true,
});
