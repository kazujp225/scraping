"""
実際のスクレイピング関数（バックエンド用）
"""
import asyncio
from typing import List, Dict
from playwright.async_api import async_playwright
import json
from datetime import datetime
import logging
import os
import sys

# プロジェクトルートをパスに追加（scrapers を利用するため）
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

logger = logging.getLogger(__name__)


async def scrape_indeed_real(keyword: str = "プログラマー", location: str = "東京", max_items: int = 10):
    """
    Indeedから求人情報を取得
    """
    logger.info(f"      Indeed: ブラウザ起動中...")
    async with async_playwright() as p:
        # ブラウザ起動
        browser = await p.chromium.launch(
            headless=True,  # バックグラウンド実行
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
            logger.info(f"      Indeed: ページアクセス中... {url}")

            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            logger.info(f"      Indeed: ページ読み込み完了")

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
            logger.info(f"      Indeed: 求人カードを検索中...")
            for selector in selectors_to_try:
                job_cards = await page.query_selector_all(selector)
                if len(job_cards) > 0:
                    logger.info(f"      Indeed: セレクタ '{selector}' で {len(job_cards)}件発見")
                    break

            if not job_cards:
                logger.warning(f"      Indeed: 求人カードが見つかりませんでした")
                return []

            # データ抽出
            logger.info(f"      Indeed: データ抽出中... (最大{max_items}件)")
            jobs = []
            for i, card in enumerate(job_cards[:max_items], 1):
                try:
                    # タイトル取得
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

                    if title:
                        job = {
                            "番号": i,
                            "タイトル": title.strip() if title else "N/A",
                            "会社名": company.strip() if company else "N/A",
                            "場所": location_text.strip(),
                            "給与": salary.strip()
                        }
                        jobs.append(job)

                except Exception as e:
                    logger.debug(f"      Indeed: カード{i}の抽出エラー (スキップ): {e}")
                    continue

            logger.info(f"      Indeed: 抽出完了 - {len(jobs)}件")
            return jobs

        except Exception as e:
            logger.error(f"      Indeed: エラー発生 - {e}")
            return []

        finally:
            logger.info(f"      Indeed: ブラウザクローズ")
            await browser.close()


async def scrape_yahoo_real(keyword: str = "プログラマー", location: str = "東京", max_items: int = 10):
    """
    Yahoo!しごと検索から求人情報を取得
    """
    logger.info(f"      Yahoo: ブラウザ起動中...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Yahoo!しごと検索にアクセス
            url = f"https://shigoto.yahoo.co.jp/search/?query={keyword}"
            logger.info(f"      Yahoo: ページアクセス中... {url}")

            await page.goto(url, timeout=30000)
            logger.info(f"      Yahoo: ページ読み込み完了")
            await asyncio.sleep(3)

            # 求人カード取得
            logger.info(f"      Yahoo: 求人カードを検索中...")
            job_cards = await page.query_selector_all("article")

            if not job_cards:
                logger.warning(f"      Yahoo: 求人カードが見つかりませんでした")
                return []

            logger.info(f"      Yahoo: {len(job_cards)}件発見")

            jobs = []
            for i, card in enumerate(job_cards[:max_items], 1):
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
                        "会社名": company.strip(),
                        "場所": location,
                        "給与": "N/A"
                    }
                    jobs.append(job)

                except Exception as e:
                    logger.debug(f"      Yahoo: カード{i}の抽出エラー (スキップ): {e}")
                    continue

            logger.info(f"      Yahoo: 抽出完了 - {len(jobs)}件")
            return jobs

        except Exception as e:
            logger.error(f"      Yahoo: エラー発生 - {e}")
            return []

        finally:
            logger.info(f"      Yahoo: ブラウザクローズ")
            await browser.close()


async def scrape_townwork_real(keyword: str = "プログラマー", location: str = "東京", max_items: int = 10) -> List[Dict]:
    """
    タウンワークから求人情報を取得（scrapers.TownworkScraper を利用）
    """
    logger.info(f"      Townwork: スクレイパー起動中...")

    try:
        # 遅延インポート（パス設定後）
        from scrapers.townwork import TownworkScraper

        scraper = TownworkScraper()
        # タウンワークのページ数は控えめに（検出回避）
        max_pages = max(1, min(5, (max_items // 20) + 1))

        results = await scraper.scrape([keyword], [location], max_pages=max_pages, parallel=1)

        jobs: List[Dict] = []
        for i, job in enumerate(results[:max_items], 1):
            jobs.append({
                "番号": i,
                "タイトル": job.get("title", ""),
                "会社名": job.get("company", ""),
                "場所": job.get("location", ""),
                "給与": job.get("salary", ""),
            })

        logger.info(f"      Townwork: 抽出完了 - {len(jobs)}件")
        return jobs

    except Exception as e:
        logger.error(f"      Townwork: エラー発生 - {e}")
        return []
