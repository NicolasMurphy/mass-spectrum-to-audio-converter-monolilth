const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  use: {
    baseURL: "http://localhost:5173",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
  outputDir: "test-results/",
  reporter: [["list"], ["html", { outputFolder: "playwright-report" }]],

  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },

    { name: "mobile-safari", use: { ...devices["iPhone 16"] } },
    { name: "mobile-chrome", use: { ...devices["Galaxy S25"] } },

    { name: "tablet", use: { ...devices["iPad Pro"] } },
  ],
});
