// https://nuxt.com/docs/api/configuration/nuxt-config

import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: ['@nuxt/ui'],
  vite: {
    plugins: [
      tailwindcss()
    ]
  },
  runtimeConfig: {
    public: {
      urlAPI: process.env.API_URL,
      ApiKey: process.env.API_KEY
     },
  },
  app: {
    head: {
      link: [{ rel: 'icon', type: 'image/png', 'href': '/bot.png'}]
    }
  }
})
