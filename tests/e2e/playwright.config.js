const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  use: {
    baseURL: "http://localhost:5173",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  outputDir: "test-results/",
  reporter: [["list"], ["html", { outputFolder: "playwright-report" }]],
});
