"""
エン転職専用スクレイパー
"""
from typing import Dict, Any
from playwright.async_api import Page
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class EntenshokuScraper(BaseScraper):
    """エン転職用スクレイパー"""

    def __init__(self):
        super().__init__(site_name="entenshoku")

    async def extract_detail_info(self, page: Page, url: str) -> Dict[str, Any]:
        """詳細ページから追加情報を取得"""
        detail_data = {}

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(1500)

            # 求人番号
            elem = await page.query_selector(".job-code")
            if elem:
                detail_data["job_number"] = (await elem.inner_text()).strip()

            # 郵便番号
            elem = await page.query_selector(".zip")
            if elem:
                detail_data["postal_code"] = (await elem.inner_text()).strip()

            # 電話番号
            elem = await page.query_selector(".phone-number")
            if elem:
                detail_data["phone"] = (await elem.inner_text()).strip()

            # 事業内容
            elem = await page.query_selector(".company-business")
            if elem:
                detail_data["business_content"] = (await elem.inner_text()).strip()

            # 採用人数
            elem = await page.query_selector(".recruit-number")
            if elem:
                detail_data["hiring_count"] = (await elem.inner_text()).strip()

        except Exception as e:
            logger.error(f"Error extracting detail info from {url}: {e}")

        return detail_data
