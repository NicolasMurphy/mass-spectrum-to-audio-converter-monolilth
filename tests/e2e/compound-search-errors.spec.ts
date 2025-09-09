import { test, expect, type Page } from "@playwright/test";

test("handles invalid compound searches", async ({ page }: { page: Page }) => {
  await page.goto("/");

  // blank search does not generate
  await page.getByRole("button", { name: "Generate Audio" }).click();
  await expect(page.getByText("No spectrum data yet")).toBeVisible();

  // empty space search displays expected error message
  await page.getByRole("textbox", { name: "Compound Name" }).click();
  await page.getByRole("textbox", { name: "Compound Name" }).fill(" ");
  await page.getByRole("button", { name: "Generate Audio" }).click();
  await expect(page.getByText("Please enter a compound name.")).toBeVisible();

  // invalid search displays expected error message
  await page.getByRole("textbox", { name: "Compound Name" }).click();
  await page.getByRole("textbox", { name: "Compound Name" }).fill("invalid");
  await page.getByRole("button", { name: "Generate Audio" }).click();
  await expect(page.getByText("Error: No records found")).toBeVisible();
});
