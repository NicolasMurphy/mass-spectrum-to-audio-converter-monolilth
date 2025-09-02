const { test, expect } = require("@playwright/test");

test("has title", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle("Mass Spectrum to Audio Converter");
});
