import { expect, test } from '@playwright/test';

test('ラクスのサイトが表示されているか', async ({ page }) => {
  // Google検索エンジンを開く
  await page.goto('https://www.google.com/');
  // 検索欄に「株式会社ラクス」を入力
  await page.getByLabel('検索', { exact: true }).click();
  await page.getByLabel('検索', { exact: true }).fill('株式会社ラクス');
  // Enterを押す
  await page.getByRole('combobox', { name: '検索' }).press('Enter');
  // 検索結果から公式サイトをクリック
  await page.getByRole('link', { name: '企業の成長を支援するクラウドサービス | 株式会社ラクス ラクス https://www.rakus.co.jp' }).click();
  // テスト：公式サイトが表示されているか
  await expect(page).toHaveURL("https://www.rakus.co.jp/");
});
