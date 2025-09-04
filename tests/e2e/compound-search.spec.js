import { test, expect } from '@playwright/test';

test('user can search for caffeine and generate audio', async ({ page }) => {
  await page.goto('/');

  // manual type and click generate
  await page.getByRole('textbox', { name: 'Compound Name' }).click();
  await page.getByRole('textbox', { name: 'Compound Name' }).fill('caffeine');
  await page.getByRole('button', { name: 'Generate Audio' }).click();

  // table titles (and correct peaks) are visible
  await expect(page.getByRole('heading', { name: 'Mass Spectrum Data (9 peaks)' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Audio Transformation Data' })).toBeVisible();

  // success message, compound, accession, download button, audio player are visible
  await expect(page.getByText('Success!')).toBeVisible();
  await expect(page.getByText('Compound: Caffeine')).toBeVisible();
  await expect(page.getByText('Accession: MSBNK-ACES_SU-')).toBeVisible();
  await expect(page.getByRole('link', { name: 'Download WAV' })).toBeVisible();
  await expect(page.locator('audio')).toBeVisible();

  // piano keys are visible (lowest and highest)
  await expect(page.getByTestId('container')).toContainText('a');
  await expect(page.getByTestId('container')).toContainText('k');
});
