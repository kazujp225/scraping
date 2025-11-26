"""
プロキシ管理とローテーション
"""
import random
import logging
from typing import List, Optional, Dict
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ProxyConfig:
    """プロキシ設定"""
    server: str  # "http://proxy.example.com:8080"
    username: Optional[str] = None
    password: Optional[str] = None

    def to_playwright_format(self) -> Dict:
        """Playwright用のプロキシ設定に変換"""
        config = {"server": self.server}
        if self.username and self.password:
            config["username"] = self.username
            config["password"] = self.password
        return config

    def __str__(self):
        if self.username:
            return f"{self.username}@{self.server}"
        return self.server


class ProxyRotator:
    """プロキシローテーター"""

    def __init__(self, proxies: List[ProxyConfig] = None):
        """
        Args:
            proxies: プロキシ設定のリスト
        """
        self.proxies = proxies if proxies else []
        self.current_index = 0
        self.enabled = bool(self.proxies)
        self.failed_proxies = set()

    def add_proxy(self, server: str, username: str = None, password: str = None):
        """プロキシを追加"""
        proxy = ProxyConfig(server=server, username=username, password=password)
        self.proxies.append(proxy)
        self.enabled = True
        logger.info(f"Added proxy: {proxy}")

    def get_random(self) -> Optional[ProxyConfig]:
        """ランダムにプロキシを取得"""
        if not self.proxies:
            return None

        available = [p for p in self.proxies if str(p) not in self.failed_proxies]
        if not available:
            # 全て失敗していたらリセット
            logger.warning("All proxies failed, resetting failed list")
            self.failed_proxies.clear()
            available = self.proxies

        return random.choice(available)

    def get_next(self) -> Optional[ProxyConfig]:
        """順番にプロキシを取得（ローテーション）"""
        if not self.proxies:
            return None

        # 失敗していないプロキシを探す
        attempts = 0
        while attempts < len(self.proxies):
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)

            if str(proxy) not in self.failed_proxies:
                return proxy

            attempts += 1

        # 全て失敗していたらリセットして最初のプロキシを返す
        logger.warning("All proxies failed, resetting failed list")
        self.failed_proxies.clear()
        return self.proxies[0] if self.proxies else None

    def mark_failed(self, proxy: ProxyConfig):
        """プロキシを失敗としてマーク"""
        self.failed_proxies.add(str(proxy))
        logger.warning(f"Marked proxy as failed: {proxy}")

    def mark_success(self, proxy: ProxyConfig):
        """プロキシを成功としてマーク（失敗リストから削除）"""
        proxy_str = str(proxy)
        if proxy_str in self.failed_proxies:
            self.failed_proxies.remove(proxy_str)
            logger.info(f"Marked proxy as successful: {proxy}")

    def is_enabled(self) -> bool:
        """プロキシが有効かどうか"""
        return self.enabled

    def disable(self):
        """プロキシを無効化"""
        self.enabled = False
        logger.info("Proxy disabled")

    def enable(self):
        """プロキシを有効化"""
        if self.proxies:
            self.enabled = True
            logger.info("Proxy enabled")
        else:
            logger.warning("Cannot enable proxy: no proxies configured")


# グローバルインスタンス
proxy_rotator = ProxyRotator()


def load_proxies_from_file(filepath: str) -> List[ProxyConfig]:
    """
    ファイルからプロキシリストを読み込み

    ファイル形式:
    http://proxy1.example.com:8080
    http://username:password@proxy2.example.com:8080
    """
    proxies = []

    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # username:password@server:port 形式をパース
                if '@' in line:
                    auth, server = line.rsplit('@', 1)
                    if ':' in auth:
                        username, password = auth.split(':', 1)
                        # プロトコルがあれば除去
                        if '://' in username:
                            username = username.split('://', 1)[1]
                        server = f"http://{server}" if not server.startswith('http') else server
                        proxies.append(ProxyConfig(server=server, username=username, password=password))
                else:
                    server = line if line.startswith('http') else f"http://{line}"
                    proxies.append(ProxyConfig(server=server))

        logger.info(f"Loaded {len(proxies)} proxies from {filepath}")
    except FileNotFoundError:
        logger.warning(f"Proxy file not found: {filepath}")
    except Exception as e:
        logger.error(f"Error loading proxies from {filepath}: {e}")

    return proxies
