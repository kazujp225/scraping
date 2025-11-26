"""
ハローワーク専用スクレイパー
"""
from typing import Dict, Any
from playwright.async_api import Page
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class HelloworkScraper(BaseScraper):
    """ハローワーク用スクレイパー"""

    def __init__(self):
        super().__init__(site_name="hellowork")

    async def extract_detail_info(self, page: Page, url: str) -> Dict[str, Any]:
        """詳細ページから追加情報を取得"""
        detail_data = {}

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(1000)

            # ハローワークは公的機関なので詳細情報が充実
            # 求人番号
            elem = await page.query_selector(".kyujin-number")
            if elem:
                detail_data["job_number"] = (await elem.inner_text()).strip()

            # 事業所名カナ
            elem = await page.query_selector(".employer-kana")
            if elem:
                detail_data["company_kana"] = (await elem.inner_text()).strip()

            # 郵便番号
            elem = await page.query_selector(".postal-code")
            if elem:
                detail_data["postal_code"] = (await elem.inner_text()).strip()

            # 電話番号
            elem = await page.query_selector(".tel-number")
            if elem:
                detail_data["phone"] = (await elem.inner_text()).strip()

            # 事業内容
            elem = await page.query_selector(".business-content")
            if elem:
                detail_data["business_content"] = (await elem.inner_text()).strip()

            # 就業場所
            elem = await page.query_selector(".workplace")
            if elem:
                detail_data["workplace"] = (await elem.inner_text()).strip()

            # 雇用形態
            elem = await page.query_selector(".employment-type")
            if elem:
                detail_data["employment_type"] = (await elem.inner_text()).strip()

        except Exception as e:
            logger.error(f"Error extracting detail info from {url}: {e}")

        return detail_data
