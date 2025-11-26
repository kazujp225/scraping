"""
スクレイパーテストスクリプト
実際のサイトで動作確認
"""
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright
from utils.stealth import StealthConfig, create_stealth_context
from utils.page_utils import PageUtils
import json

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScraperTester:
    """スクレイパーテスト用クラス"""

    def __init__(self, debug_mode: bool = True):
        self.debug_mode = debug_mode
        self.screenshots_dir = Path("data/screenshots")
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    async def test_site_access(self, site_name: str, url: str) -> dict:
        """
        サイトへのアクセステスト

        Args:
            site_name: サイト名
            url: テストするURL

        Returns:
            テスト結果の辞書
        """
        result = {
            "site": site_name,
            "url": url,
            "success": False,
            "error": None,
            "load_time": 0,
            "blocked": False,
            "captcha": False,
            "screenshot": None
        }

        async with async_playwright() as p:
            # ブラウザ起動
            browser = await p.chromium.launch(
                **StealthConfig.get_launch_args(),
                headless=not self.debug_mode  # デバッグ時はヘッドレスオフ
            )

            try:
                # Stealthコンテキスト作成
                context = await create_stealth_context(browser)
                page = await context.new_page()

                # Stealth スクリプト適用
                await StealthConfig.apply_stealth_scripts(page)

                # ページ遷移
                start_time = asyncio.get_event_loop().time()
                success = await PageUtils.safe_goto(page, url)
                load_time = asyncio.get_event_loop().time() - start_time

                result["load_time"] = round(load_time, 2)
                result["success"] = success

                if success:
                    # ブロックチェック
                    block_info = await PageUtils.check_for_block(page)
                    result["blocked"] = block_info["is_blocked"]
                    result["captcha"] = "CAPTCHA" in block_info.get("indicators", [])

                    # スクリーンショット保存
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = self.screenshots_dir / f"{site_name}_{timestamp}.png"
                    await PageUtils.take_screenshot(page, str(screenshot_path), full_page=True)
                    result["screenshot"] = str(screenshot_path)

                    logger.info(f"✅ {site_name}: Successfully accessed")
                    if result["blocked"]:
                        logger.warning(f"⚠️  {site_name}: Access blocked detected")
                    if result["captcha"]:
                        logger.warning(f"⚠️  {site_name}: CAPTCHA detected")
                else:
                    logger.error(f"❌ {site_name}: Failed to access")

                # デバッグモードでは5秒待機
                if self.debug_mode:
                    await asyncio.sleep(5)

            except Exception as e:
                result["error"] = str(e)
                logger.error(f"❌ {site_name}: Error - {e}")

            finally:
                await context.close()
                await browser.close()

        return result

    async def test_selector(self, site_name: str, url: str, selector: str) -> dict:
        """
        セレクタのテスト

        Args:
            site_name: サイト名
            url: テストするURL
            selector: テストするCSSセレクタ

        Returns:
            テスト結果の辞書
        """
        result = {
            "site": site_name,
            "selector": selector,
            "found": False,
            "count": 0,
            "sample_text": None
        }

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                **StealthConfig.get_launch_args(),
                headless=not self.debug_mode
            )

            try:
                context = await create_stealth_context(browser)
                page = await context.new_page()
                await StealthConfig.apply_stealth_scripts(page)

                if await PageUtils.safe_goto(page, url):
                    # セレクタ検証
                    result["found"] = await PageUtils.verify_selector(page, selector)

                    if result["found"]:
                        # 要素数カウント
                        result["count"] = await PageUtils.get_elements_count(page, selector)

                        # サンプルテキスト取得
                        sample = await PageUtils.extract_text_safe(page, selector)
                        result["sample_text"] = sample

                        logger.info(f"✅ Selector '{selector}': Found {result['count']} elements")
                        if sample:
                            logger.info(f"   Sample text: {sample[:100]}")
                    else:
                        logger.warning(f"⚠️  Selector '{selector}': Not found")

                # デバッグモードでは待機
                if self.debug_mode:
                    await asyncio.sleep(3)

            except Exception as e:
                logger.error(f"❌ Selector test error: {e}")

            finally:
                await context.close()
                await browser.close()

        return result

    async def test_all_selectors(self, site_name: str, config_path: str = "config/selectors.json"):
        """
        サイトの全セレクタをテスト

        Args:
            site_name: サイト名
            config_path: セレクタ設定ファイルのパス
        """
        # 設定読み込み
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        if site_name not in config:
            logger.error(f"Site '{site_name}' not found in config")
            return

        site_config = config[site_name]
        base_url = site_config.get("base_url")
        selectors = site_config.get("selectors", {})

        # テストURL生成（簡易版）
        test_url = site_config.get("search_url_pattern", base_url)
        test_url = test_url.format(keyword="IT", area="tokyo", page=1, offset=0)

        logger.info(f"\n{'='*60}")
        logger.info(f"Testing selectors for: {site_name}")
        logger.info(f"URL: {test_url}")
        logger.info(f"{'='*60}\n")

        # サイトアクセステスト
        access_result = await self.test_site_access(site_name, test_url)

        if not access_result["success"] or access_result["blocked"]:
            logger.error(f"Cannot test selectors - site access failed or blocked")
            return

        # 各セレクタをテスト
        results = []
        for selector_name, selector in selectors.items():
            logger.info(f"\nTesting: {selector_name} = '{selector}'")
            result = await self.test_selector(site_name, test_url, selector)
            result["selector_name"] = selector_name
            results.append(result)

            # レート制限回避のため少し待機
            await asyncio.sleep(2)

        # 結果サマリー
        logger.info(f"\n{'='*60}")
        logger.info(f"Test Summary for {site_name}")
        logger.info(f"{'='*60}")
        found = sum(1 for r in results if r["found"])
        logger.info(f"Selectors found: {found}/{len(results)}")

        for r in results:
            status = "✅" if r["found"] else "❌"
            logger.info(f"{status} {r['selector_name']}: {r['count']} elements")


async def main():
    """メイン関数"""
    tester = ScraperTester(debug_mode=True)  # デバッグモードON

    # テストしたいサイトを選択
    print("\n" + "="*60)
    print("スクレイパーテストツール")
    print("="*60)
    print("\n選択してください:")
    print("1. サイトアクセステスト（単一サイト）")
    print("2. セレクタテスト（全セレクタ）")
    print("3. クイックテスト（タウンワーク）")
    print("="*60 + "\n")

    choice = input("選択 (1-3): ").strip()

    if choice == "1":
        site_name = input("サイト名: ").strip()
        url = input("URL: ").strip()
        result = await tester.test_site_access(site_name, url)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif choice == "2":
        site_name = input("サイト名 (例: townwork): ").strip()
        await tester.test_all_selectors(site_name)

    elif choice == "3":
        # タウンワークのクイックテスト
        logger.info("Running quick test on Townwork...")
        url = "https://townwork.net/tokyo/search/"
        result = await tester.test_site_access("townwork", url)

        if result["success"] and not result["blocked"]:
            # 基本的なセレクタをテスト
            await tester.test_selector("townwork", url, "article")
            await tester.test_selector("townwork", url, ".list-jobListDetail")

    else:
        print("無効な選択です")


if __name__ == "__main__":
    asyncio.run(main())
