"""
ヘッドレスブラウザ検出回避（Stealth設定）
"""
from typing import Dict, Any
from playwright.async_api import BrowserContext, Page
import logging

logger = logging.getLogger(__name__)


class StealthConfig:
    """Stealth設定マネージャー"""

    @staticmethod
    async def apply_stealth_scripts(page: Page):
        """
        ページにステルススクリプトを適用
        ヘッドレスモード検出を回避
        """
        # WebDriverプロパティを隠蔽
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        # Chrome特有のプロパティを追加
        await page.add_init_script("""
            window.chrome = {
                runtime: {}
            };
        """)

        # Permissions APIの上書き
        await page.add_init_script("""
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)

        # プラグインの追加
        await page.add_init_script("""
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
        """)

        # 言語設定
        await page.add_init_script("""
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ja-JP', 'ja', 'en-US', 'en']
            });
        """)

        logger.debug("Stealth scripts applied")

    @staticmethod
    def get_browser_context_args() -> Dict[str, Any]:
        """
        ブラウザコンテキストの設定を取得
        より自然なブラウザに見せる
        """
        return {
            "viewport": {"width": 1920, "height": 1080},
            "locale": "ja-JP",
            "timezone_id": "Asia/Tokyo",
            "permissions": ["geolocation"],
            "geolocation": {"latitude": 35.6762, "longitude": 139.6503},  # 東京
            "color_scheme": "light",
            "reduced_motion": "no-preference",
            "forced_colors": "none",
        }

    @staticmethod
    def get_launch_args() -> Dict[str, Any]:
        """
        ブラウザ起動時の引数を取得
        検出回避のための設定
        """
        return {
            "headless": True,
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--window-size=1920,1080",
                "--start-maximized",
                "--disable-infobars",
                "--disable-notifications",
                "--disable-popup-blocking",
            ]
        }


async def create_stealth_context(browser, user_agent: str = None, proxy: Dict = None) -> BrowserContext:
    """
    Stealth設定を適用したブラウザコンテキストを作成

    Args:
        browser: Playwrightブラウザインスタンス
        user_agent: カスタムUser-Agent（オプション）
        proxy: プロキシ設定（オプション）

    Returns:
        設定済みのBrowserContext
    """
    context_args = StealthConfig.get_browser_context_args()

    if user_agent:
        context_args["user_agent"] = user_agent

    if proxy:
        context_args["proxy"] = proxy

    context = await browser.new_context(**context_args)

    # 全ページにステルススクリプトを適用
    context.on("page", lambda page: StealthConfig.apply_stealth_scripts(page))

    logger.info("Stealth context created")
    return context
