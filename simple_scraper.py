"""
シンプルで確実に動くスクレイパー
1ファイル完結・すぐに実行可能
"""
import asyncio
from playwright.async_api import async_playwright
import json
from datetime import datetime


async def scrape_indeed_simple():
    """
    Indeedから求人情報を取得
    シンプルで確実に動く実装
    """
    print("\n" + "="*60)
    print("求人スクレイピング - シンプル版")
    print("="*60 + "\n")

    # 検索条件
    keyword = "プログラマー"
    location = "東京"

    print(f"検索条件: {keyword} in {location}")
    print("ブラウザを起動中...\n")

    async with async_playwright() as p:
        # ブラウザ起動（ヘッドレスモード）
        browser = await p.chromium.launch(
            headless=False,  # ブラウザを表示（動作確認用）
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )

        # ページ作成
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            # Indeed検索ページにアクセス
            url = f"https://jp.indeed.com/jobs?q={keyword}&l={location}"
            print(f"アクセス中: {url}")

            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            print("✅ ページ読み込み完了\n")

            # 少し待機
            await asyncio.sleep(3)

            # 求人カードを取得（複数のセレクタを試す）
            selectors_to_try = [
                ".job_seen_beacon",
                ".jobsearch-SerpJobCard",
                "div[data-jk]",
                ".slider_item",
                "td.resultContent"
            ]

            job_cards = []
            used_selector = None

            for selector in selectors_to_try:
                job_cards = await page.query_selector_all(selector)
                if len(job_cards) > 0:
                    used_selector = selector
                    print(f"✅ セレクタ '{selector}' で {len(job_cards)} 件見つかりました\n")
                    break
                else:
                    print(f"⏭️  セレクタ '{selector}' では見つかりませんでした")

            if not job_cards:
                print("\n❌ 求人カードが見つかりませんでした")
                print("スクリーンショットを保存します...")
                await page.screenshot(path="error_screenshot.png", full_page=True)
                print("保存完了: error_screenshot.png")
                return []

            print(f"データ抽出を開始します...\n")

            # データ抽出
            jobs = []
            for i, card in enumerate(job_cards[:10], 1):  # 最初の10件のみ
                try:
                    # タイトル取得（複数パターンを試す）
                    title = None
                    title_selectors = ["h2.jobTitle", ".jobTitle", "h2 a", ".jcs-JobTitle"]
                    for ts in title_selectors:
                        elem = await card.query_selector(ts)
                        if elem:
                            title = await elem.inner_text()
                            break

                    # 会社名取得
                    company = None
                    company_selectors = [".companyName", "[data-testid='company-name']", ".company"]
                    for cs in company_selectors:
                        elem = await card.query_selector(cs)
                        if elem:
                            company = await elem.inner_text()
                            break

                    # 場所取得
                    location_elem = await card.query_selector(".companyLocation")
                    location_text = await location_elem.inner_text() if location_elem else "N/A"

                    # 給与取得
                    salary_elem = await card.query_selector(".salary-snippet")
                    salary = await salary_elem.inner_text() if salary_elem else "N/A"

                    if title:  # タイトルがあれば追加
                        job = {
                            "番号": i,
                            "タイトル": title.strip() if title else "N/A",
                            "会社名": company.strip() if company else "N/A",
                            "場所": location_text.strip(),
                            "給与": salary.strip()
                        }
                        jobs.append(job)
                        print(f"{i}. {job['タイトル'][:40]}... - {job['会社名'][:30]}")

                except Exception as e:
                    print(f"⚠️  カード {i} の抽出でエラー: {e}")
                    continue

            print(f"\n✅ 合計 {len(jobs)} 件のデータを取得しました")

            # 結果をJSONファイルに保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"indeed_jobs_{timestamp}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, ensure_ascii=False, indent=2)

            print(f"\n💾 結果を保存しました: {filename}")

            # スクリーンショット保存
            screenshot_file = f"screenshot_{timestamp}.png"
            await page.screenshot(path=screenshot_file, full_page=True)
            print(f"📸 スクリーンショット保存: {screenshot_file}")

            return jobs

        except Exception as e:
            print(f"\n❌ エラーが発生しました: {e}")

            # エラー時もスクリーンショット保存
            try:
                await page.screenshot(path="error_screenshot.png", full_page=True)
                print("エラー時のスクリーンショット保存: error_screenshot.png")
            except:
                pass

            return []

        finally:
            # ブラウザを閉じる（5秒後）
            print("\n5秒後にブラウザを閉じます...")
            await asyncio.sleep(5)
            await browser.close()
            print("✅ 完了\n")


async def scrape_yahoo_jobs():
    """
    Yahoo!しごと検索から求人情報を取得
    よりシンプルで動作しやすい実装
    """
    print("\n" + "="*60)
    print("Yahoo!しごと検索 - スクレイピング")
    print("="*60 + "\n")

    keyword = "プログラマー"

    print(f"検索条件: {keyword}")
    print("ブラウザを起動中...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Yahoo!しごと検索にアクセス
            url = f"https://shigoto.yahoo.co.jp/search/?query={keyword}"
            print(f"アクセス中: {url}")

            await page.goto(url, timeout=30000)
            await asyncio.sleep(3)

            print("✅ ページ読み込み完了\n")

            # 求人カード取得
            job_cards = await page.query_selector_all("article")

            if not job_cards:
                print("❌ 求人が見つかりませんでした")
                await page.screenshot(path="error_yahoo.png")
                return []

            print(f"✅ {len(job_cards)} 件の求人が見つかりました\n")

            jobs = []
            for i, card in enumerate(job_cards[:10], 1):
                try:
                    # タイトル
                    title_elem = await card.query_selector("h2, h3")
                    title = await title_elem.inner_text() if title_elem else "N/A"

                    # 会社名
                    company_elem = await card.query_selector(".company, .corp")
                    company = await company_elem.inner_text() if company_elem else "N/A"

                    job = {
                        "番号": i,
                        "タイトル": title.strip(),
                        "会社名": company.strip()
                    }
                    jobs.append(job)
                    print(f"{i}. {job['タイトル'][:50]}...")

                except Exception as e:
                    print(f"⚠️  エラー: {e}")
                    continue

            # 保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"yahoo_jobs_{timestamp}.json"

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, ensure_ascii=False, indent=2)

            print(f"\n💾 保存完了: {filename}")
            print(f"📸 スクリーンショット保存中...")
            await page.screenshot(path=f"yahoo_{timestamp}.png")

            return jobs

        except Exception as e:
            print(f"\n❌ エラー: {e}")
            return []

        finally:
            await asyncio.sleep(5)
            await browser.close()
            print("\n✅ 完了")


def main():
    """メイン関数"""
    print("\n" + "="*60)
    print("シンプル求人スクレイパー")
    print("="*60)
    print("\n選択してください:")
    print("1. Indeed（推奨）")
    print("2. Yahoo!しごと検索")
    print("3. 両方実行")
    print("="*60 + "\n")

    choice = input("選択 (1-3): ").strip()

    if choice == "1":
        asyncio.run(scrape_indeed_simple())
    elif choice == "2":
        asyncio.run(scrape_yahoo_jobs())
    elif choice == "3":
        print("\n【Indeed】")
        asyncio.run(scrape_indeed_simple())
        print("\n【Yahoo!しごと検索】")
        asyncio.run(scrape_yahoo_jobs())
    else:
        print("無効な選択です")


if __name__ == "__main__":
    main()
