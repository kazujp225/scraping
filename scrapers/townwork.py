"""
タウンワーク専用スクレイパー
"""
from typing import Dict, Any, List, Union
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from playwright.async_api import Page
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class TownworkScraper(BaseScraper):
    """タウンワーク用スクレイパー"""

    def __init__(self):
        super().__init__(site_name="townwork")

    async def extract_detail_info(self, page: Page, url: str) -> Dict[str, Any]:
        """
        詳細ページから追加情報を取得

        取得項目:
        - 会社名カナ
        - 郵便番号
        - 住所詳細
        - 電話番号
        - FAX番号
        - 担当者名
        - 担当者メールアドレス
        - 求人番号
        - 事業内容
        """
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

            # 電話番号
            if self.detail_selectors.get("phone"):
                elem = await page.query_selector(self.detail_selectors["phone"])
                if elem:
                    detail_data["phone"] = (await elem.inner_text()).strip()

            # FAX
            if self.detail_selectors.get("fax"):
                elem = await page.query_selector(self.detail_selectors["fax"])
                if elem:
                    detail_data["fax"] = (await elem.inner_text()).strip()

            # 担当者
            if self.detail_selectors.get("recruiter"):
                elem = await page.query_selector(self.detail_selectors["recruiter"])
                if elem:
                    detail_data["recruiter"] = (await elem.inner_text()).strip()

            # 担当者メール
            if self.detail_selectors.get("recruiter_email"):
                elem = await page.query_selector(self.detail_selectors["recruiter_email"])
                if elem:
                    detail_data["recruiter_email"] = (await elem.inner_text()).strip()

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
        """
        タウンワーク用の検索URL生成

        エリアコード例:
        - 東京: tokyo
        - 大阪: osaka
        - 愛知: aichi
        """
        # エリア名を小文字のローマ字に変換（簡易版）
        area_map = {
            "東京": "tokyo",
            "大阪": "osaka",
            "愛知": "aichi",
            "神奈川": "kanagawa",
            "埼玉": "saitama",
            "千葉": "chiba",
        }
        area_code = area_map.get(area, area.lower())

        url_pattern = self.site_config.get("search_url_pattern")
        base_url = url_pattern.format(area=area_code, keyword=keyword, page=page)

        # フィルタ（クエリパラメータ）の付与
        filters = getattr(self, "current_filters", {}) or {}
        if not filters:
            return base_url

        parsed = urlparse(base_url)
        query_pairs = parse_qsl(parsed.query, keep_blank_values=True)

        # 設定ファイルからパラメータ名とオプション値の対応を取得
        filter_cfg = self.site_config.get("filters", {})
        param_map: Dict[str, str] = (filter_cfg.get("query_params") or {})
        option_map: Dict[str, Dict[str, str]] = (filter_cfg.get("options") or {})

        def add_param(param: str, value: Union[str, int, float, List[str]]):
            if isinstance(value, list):
                for v in value:
                    query_pairs.append((param, str(v)))
            else:
                query_pairs.append((param, str(value)))

        for key, val in filters.items():
            # パラメータ名を取得（未定義はスキップ）
            param = param_map.get(key)
            if not param:
                continue

            # オプション値の変換（例: 正社員 -> full）
            if isinstance(val, list):
                mapped_vals = [option_map.get(key, {}).get(v, v) for v in val]
                add_param(param, mapped_vals)
            else:
                mapped_val = option_map.get(key, {}).get(val, val)
                add_param(param, mapped_val)

        new_query = urlencode(query_pairs, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        return urlunparse(new_parsed)
