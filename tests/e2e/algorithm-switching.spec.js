import { test, expect } from '@playwright/test';

test('user can switch between algorithms and get different results', async ({ page }) => {
  await page.goto('/');

  // search for biotin (default linear) (clicking on most generated tag), search with enter key, verify first hz value
  await page.getByText('BIOTIN').first().click();
  await page.locator('body').press('Enter');
  await expect(page.getByRole('cell', { name: '355.0534' })).toBeVisible();

  // switch to inverse, verify first hz value
  await page.getByRole('radio', { name: 'Inverse: scale / (mz + shift)' }).check();
  await page.getByRole('radio', { name: 'Inverse: scale / (mz + shift)' }).press('Enter');
  await expect(page.getByRole('cell', { name: '406.3458' })).toBeVisible();

  // switch to modulo, verify first hz value
  await page.getByRole('radio', { name: 'Modulo: ((mz * factor) % modulus) + base' }).check();
  await page.getByRole('radio', { name: 'Modulo: ((mz * factor) % modulus) + base' }).press('Enter');
  await expect(page.getByRole('cell', { name: '100.1820' })).toBeVisible();
});
