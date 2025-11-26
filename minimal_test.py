"""
最小限のテストスクリプト
確実に動作することを確認
"""
import asyncio
from playwright.async_api import async_playwright


async def test_basic():
    """基本的な動作テスト"""
    print("="*60)
    print("Playwright 動作テスト")
    print("="*60 + "\n")

    async with async_playwright() as p:
        print("✅ Playwright初期化成功")

        # ブラウザ起動
        print("ブラウザを起動中...")
        browser = await p.chromium.launch(headless=False)
        print("✅ ブラウザ起動成功\n")

        # ページ作成
        page = await browser.new_page()
        print("✅ ページ作成成功")

        # Googleにアクセス
        print("\nGoogleにアクセス中...")
        await page.goto("https://www.google.com")
        print("✅ アクセス成功")

        # タイトル取得
        title = await page.title()
        print(f"ページタイトル: {title}\n")

        # スクリーンショット
        print("スクリーンショット保存中...")
        await page.screenshot(path="test_google.png")
        print("✅ 保存完了: test_google.png\n")

        # 検索ボックスを探す
        print("検索ボックスを探しています...")
        search_box = await page.query_selector("textarea[name='q'], input[name='q']")

        if search_box:
            print("✅ 検索ボックス発見")

            # テキスト入力
            await search_box.fill("Playwright スクレイピング")
            print("✅ テキスト入力完了")

            # 少し待機
            await asyncio.sleep(2)

            # スクリーンショット
            await page.screenshot(path="test_search.png")
            print("✅ 検索後のスクリーンショット保存: test_search.png")

        else:
            print("❌ 検索ボックスが見つかりませんでした")

        print("\n5秒後に終了します...")
        await asyncio.sleep(5)

        await browser.close()
        print("\n✅ すべて正常に動作しました！\n")


async def test_indeed_access():
    """Indeed アクセステスト"""
    print("\n" + "="*60)
    print("Indeed アクセステスト")
    print("="*60 + "\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        try:
            url = "https://jp.indeed.com/"
            print(f"アクセス中: {url}")

            await page.goto(url, timeout=30000)
            await asyncio.sleep(3)

            title = await page.title()
            print(f"✅ ページタイトル: {title}\n")

            # スクリーンショット
            await page.screenshot(path="indeed_test.png", full_page=True)
            print("✅ スクリーンショット保存: indeed_test.png")

            # ページ内のテキスト確認
            body_text = await page.inner_text("body")

            if "ブロック" in body_text or "Access Denied" in body_text:
                print("\n⚠️  警告: アクセスがブロックされている可能性があります")
            else:
                print("\n✅ 正常にアクセスできています")

            # 検索ボックスを探す
            search_input = await page.query_selector("input[name='q']")
            if search_input:
                print("✅ 検索ボックスが見つかりました")
                await search_input.fill("プログラマー")
                print("✅ 検索キーワード入力完了")

                # 検索
                await asyncio.sleep(1)
                await search_input.press("Enter")
                print("✅ 検索実行")

                await asyncio.sleep(5)

                # 検索結果ページのスクリーンショット
                await page.screenshot(path="indeed_search_result.png", full_page=True)
                print("✅ 検索結果のスクリーンショット保存: indeed_search_result.png")

                # 求人カードをカウント
                cards = await page.query_selector_all("td.resultContent, div[data-jk], .job_seen_beacon")
                print(f"\n✅ 検出された求人カード数: {len(cards)}")

                if len(cards) > 0:
                    print("\n🎉 成功！求人データを取得できます")
                else:
                    print("\n⚠️  求人カードが見つかりませんでした")
                    print("別のセレクタを試す必要があります")

            else:
                print("❌ 検索ボックスが見つかりませんでした")

        except Exception as e:
            print(f"\n❌ エラー: {e}")
            await page.screenshot(path="error.png")
            print("エラー時のスクリーンショット: error.png")

        finally:
            print("\n10秒後に終了します...")
            await asyncio.sleep(10)
            await browser.close()
            print("✅ 完了\n")


def main():
    """メイン関数"""
    print("\n" + "="*60)
    print("動作確認テスト")
    print("="*60)
    print("\n選択してください:")
    print("1. 基本テスト（Google）")
    print("2. Indeedアクセステスト")
    print("3. 両方実行")
    print("="*60 + "\n")

    choice = input("選択 (1-3): ").strip()

    if choice == "1":
        asyncio.run(test_basic())
    elif choice == "2":
        asyncio.run(test_indeed_access())
    elif choice == "3":
        asyncio.run(test_basic())
        asyncio.run(test_indeed_access())
    else:
        print("無効な選択です")


if __name__ == "__main__":
    main()
