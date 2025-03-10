// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: [
    "@nuxt/ui",
    "@pinia/nuxt",
    "@pinia-plugin-persistedstate/nuxt",
    "@nuxtjs/tailwindcss",
    "@nuxtjs/color-mode",
  ],

  tailwindcss: {
    config: {
      theme: {
        extend: {
          colors: {
            mmwgh: "#05981c",
          },
        },
      },
    },
  },

  colorMode: {
    classSuffix: "",
  },

  runtimeConfig: {
    public: {
      baseURL: process.env.NUXT_PUBLIC_BASE_URL || "http://localhost:8000",
      appName: process.env.NUXT_PUBLIC_APP_NAME || "My Nuxt App",
    },
  },

  target: "static",
  ssr: false,

  server: {
    host: "0.0.0.0",
    port: "3000", // optional
    watch: {
      usePolling: true, 
      interval: 1000,  
    },
  },

  compatibilityDate: "2024-12-10",
});