const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  use: {
    baseURL: "http://localhost:5173",
  },
});
