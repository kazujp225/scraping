"""
Indeed専用スクレイパー
"""
from typing import Dict, Any
from playwright.async_api import Page
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class IndeedScraper(BaseScraper):
    """Indeed用スクレイパー"""

    def __init__(self):
        super().__init__(site_name="indeed")

    async def extract_detail_info(self, page: Page, url: str) -> Dict[str, Any]:
        """詳細ページから追加情報を取得"""
        detail_data = {}

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(1500)

            # 電話番号
            if self.detail_selectors.get("phone"):
                elem = await page.query_selector(self.detail_selectors["phone"])
                if elem:
                    detail_data["phone"] = (await elem.inner_text()).strip()

            # 詳細な仕事内容
            if self.detail_selectors.get("full_description"):
                elem = await page.query_selector(self.detail_selectors["full_description"])
                if elem:
                    detail_data["full_description"] = (await elem.inner_text()).strip()

            # 求人番号
            if self.detail_selectors.get("job_number"):
                elem = await page.query_selector(self.detail_selectors["job_number"])
                if elem:
                    detail_data["job_number"] = (await elem.inner_text()).strip()

        except Exception as e:
            logger.error(f"Error extracting detail info from {url}: {e}")

        return detail_data

    def generate_search_url(self, keyword: str, area: str, page: int = 1) -> str:
        """
        Indeed用の検索URL生成
        Indeedはoffset方式を使用
        """
        offset = (page - 1) * 10  # Indeedは1ページ10件
        url_pattern = self.site_config.get("search_url_pattern")
        return url_pattern.format(keyword=keyword, area=area, offset=offset)
