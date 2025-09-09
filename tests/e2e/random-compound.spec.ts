import { test, expect, type Page } from "@playwright/test";

// test is a bit flaky ~25% fail, usually on chrome, doesn't seem to be a user facing bug
test("random compound button generates audio successfully", async ({
  page,
}: {
  page: Page;
}) => {
  await page.goto("/");

  // click random and generate
  await page.getByRole("button", { name: "🎲" }).click();
  await page.getByRole("button", { name: "Generate Audio" }).click();

  // table titles are visible
  await expect(
    page.getByRole("heading", { name: "Mass Spectrum Data" })
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Audio Transformation Data" })
  ).toBeVisible();

  // success message, compound, accession, download button, audio player are visible
  await expect(page.getByText("Success!")).toBeVisible();
  await expect(page.getByText("Compound: ")).toBeVisible();
  await expect(page.getByText("Accession: ")).toBeVisible();
  await expect(page.getByRole("link", { name: "Download WAV" })).toBeVisible();
  await expect(page.locator("audio")).toBeVisible();

  // compound name is visible in recently generated
  const compoundName: string = await page
    .getByRole("textbox", { name: "Compound Name" })
    .inputValue();
  await expect(
    page.getByTestId("recently-generated-list").getByText(compoundName)
  ).toBeVisible();

  // piano keys are visible (lowest and highest)
  await expect(page.getByTestId("container")).toContainText("a");
  await expect(page.getByTestId("container")).toContainText("k");
});
