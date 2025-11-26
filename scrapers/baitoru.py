"""
バイトル専用スクレイパー
"""
from typing import Dict, Any
from playwright.async_api import Page
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class BaitoruScraper(BaseScraper):
    """バイトル用スクレイパー"""

    def __init__(self):
        super().__init__(site_name="baitoru")

    async def extract_detail_info(self, page: Page, url: str) -> Dict[str, Any]:
        """詳細ページから追加情報を取得"""
        detail_data = {}

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(1000)

            # 会社名カナ
            if self.detail_selectors.get("company_kana"):
                elem = await page.query_selector(self.detail_selectors["company_kana"])
                if elem:
                    detail_data["company_kana"] = (await elem.inner_text()).strip()

            # 郵便番号
            if self.detail_selectors.get("postal_code"):
                elem = await page.query_selector(self.detail_selectors["postal_code"])
                if elem:
                    detail_data["postal_code"] = (await elem.inner_text()).strip()

            # FAX
            if self.detail_selectors.get("fax"):
                elem = await page.query_selector(self.detail_selectors["fax"])
                if elem:
                    detail_data["fax"] = (await elem.inner_text()).strip()

            # 求人番号
            if self.detail_selectors.get("job_number"):
                elem = await page.query_selector(self.detail_selectors["job_number"])
                if elem:
                    detail_data["job_number"] = (await elem.inner_text()).strip()

            # 事業内容
            if self.detail_selectors.get("business_content"):
                elem = await page.query_selector(self.detail_selectors["business_content"])
                if elem:
                    detail_data["business_content"] = (await elem.inner_text()).strip()

        except Exception as e:
            logger.error(f"Error extracting detail info from {url}: {e}")

        return detail_data

    def generate_search_url(self, keyword: str, area: str, page: int = 1) -> str:
        """バイトル用の検索URL生成"""
        # 都道府県コード（簡易マッピング）
        pref_map = {
            "東京": "tokyo",
            "大阪": "osaka",
            "愛知": "aichi",
            "神奈川": "kanagawa",
            "埼玉": "saitama",
            "千葉": "chiba",
        }
        pref_code = pref_map.get(area, area.lower())

        url_pattern = self.site_config.get("search_url_pattern")
        return url_pattern.format(keyword=keyword, area=pref_code, page=page)
