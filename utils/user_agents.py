"""
User-Agent管理とローテーション
"""
import random
from typing import List


class UserAgentRotator:
    """User-Agentローテーター"""

    # 実際のブラウザから取得したUser-Agentリスト
    USER_AGENTS: List[str] = [
        # Chrome (Windows)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",

        # Chrome (Mac)
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",

        # Firefox (Windows)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",

        # Firefox (Mac)
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",

        # Safari (Mac)
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",

        # Edge (Windows)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    ]

    def __init__(self, user_agents: List[str] = None):
        """
        Args:
            user_agents: カスタムUser-Agentリスト（Noneの場合はデフォルトを使用）
        """
        self.user_agents = user_agents if user_agents else self.USER_AGENTS
        self.current_index = 0

    def get_random(self) -> str:
        """ランダムにUser-Agentを取得"""
        return random.choice(self.user_agents)

    def get_next(self) -> str:
        """順番にUser-Agentを取得（ローテーション）"""
        ua = self.user_agents[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.user_agents)
        return ua

    def get_chrome(self) -> str:
        """Chrome系のUser-Agentをランダムに取得"""
        chrome_agents = [ua for ua in self.user_agents if "Chrome" in ua]
        return random.choice(chrome_agents) if chrome_agents else self.get_random()

    def get_firefox(self) -> str:
        """Firefox系のUser-Agentをランダムに取得"""
        firefox_agents = [ua for ua in self.user_agents if "Firefox" in ua]
        return random.choice(firefox_agents) if firefox_agents else self.get_random()

    def add_custom(self, user_agent: str):
        """カスタムUser-Agentを追加"""
        if user_agent not in self.user_agents:
            self.user_agents.append(user_agent)


# グローバルインスタンス
ua_rotator = UserAgentRotator()
