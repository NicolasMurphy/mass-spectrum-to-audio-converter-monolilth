import { test, expect, type Page } from "@playwright/test";

test("user can search for caffeine and generate audio", async ({
  page,
}: {
  page: Page;
}) => {
  await page.goto("/");

  // manual type and click generate
  await page.getByRole("textbox", { name: "Compound Name" }).click();
  await page.getByRole("textbox", { name: "Compound Name" }).fill("caffeine");
  await page.getByRole("button", { name: "Generate Audio" }).click();

  // table titles (and correct peaks) are visible
  await expect(
    page.getByRole("heading", { name: "Mass Spectrum Data (9 peaks)" })
  ).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Audio Transformation Data" })
  ).toBeVisible();

  // verify first/last peaks from both tables
  await expect(
    page.getByRole("cell", { name: "56.0498", exact: true })
  ).toBeVisible();
  await expect(
    page.getByRole("cell", { name: "5,501,836", exact: true })
  ).toBeVisible();
  await expect(
    page.getByRole("cell", { name: "195.0877", exact: true })
  ).toBeVisible();
  await expect(
    page.getByRole("cell", { name: "529,785,088", exact: true })
  ).toBeVisible();
  await expect(
    page.getByRole("cell", { name: "356.0498", exact: true })
  ).toBeVisible();
  await expect(
    page.getByRole("cell", { name: "-39.6718", exact: true })
  ).toBeVisible();
  await expect(
    page.getByRole("cell", { name: "495.0877", exact: true })
  ).toBeVisible();
  await expect(
    page.getByRole("cell", { name: "0.0000", exact: true })
  ).toBeVisible();

  // success message, compound, accession, download button, audio player are visible
  await expect(page.getByText("Success!")).toBeVisible();
  await expect(page.getByText("Compound: Caffeine")).toBeVisible();
  await expect(
    page.getByText("Accession: MSBNK-ACES_SU-AS000088")
  ).toBeVisible();
  await expect(page.getByRole("link", { name: "Download WAV" })).toBeVisible();
  await expect(page.locator("audio")).toBeVisible();

  // piano keys are visible (lowest and highest)
  await expect(page.getByTestId("container")).toContainText("a");
  await expect(page.getByTestId("container")).toContainText("k");
});
