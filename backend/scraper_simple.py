"""
シンプルなスクレイピング関数（デモ版）
実際のスクレイピングは時間がかかるため、ダミーデータで動作確認
"""
import asyncio
from typing import List, Dict


async def scrape_indeed_demo(keyword: str = "プログラマー", location: str = "東京") -> List[Dict]:
    """Indeed スクレイピング（デモ版）"""
    # 実際のスクレイピングをシミュレート
    await asyncio.sleep(2)

    return [
        {
            "番号": 1,
            "タイトル": f"【{keyword}】Pythonエンジニア募集",
            "会社名": "株式会社テックソリューション",
            "場所": f"{location}都渋谷区",
            "給与": "年収500万円～800万円"
        },
        {
            "番号": 2,
            "タイトル": f"{keyword} - フルスタックエンジニア",
            "会社名": "株式会社Web開発",
            "場所": f"{location}都港区",
            "給与": "月給35万円～50万円"
        },
        {
            "番号": 3,
            "タイトル": f"【急募】{keyword}（リモート可）",
            "会社名": "株式会社クラウドテック",
            "場所": f"{location}都新宿区（リモート可）",
            "給与": "年収600万円～1000万円"
        },
        {
            "番号": 4,
            "タイトル": f"バックエンド{keyword}",
            "会社名": "株式会社データサイエンス",
            "場所": f"{location}都品川区",
            "給与": "年収550万円～900万円"
        },
        {
            "番号": 5,
            "タイトル": f"{keyword} - AI/機械学習エンジニア",
            "会社名": "株式会社AIラボ",
            "場所": f"{location}都千代田区",
            "給与": "年収700万円～1200万円"
        },
    ]


async def scrape_yahoo_demo(keyword: str = "プログラマー", location: str = "東京") -> List[Dict]:
    """Yahoo しごと検索スクレイピング（デモ版）"""
    await asyncio.sleep(1.5)

    return [
        {
            "番号": 1,
            "タイトル": f"{keyword}（経験者優遇）",
            "会社名": "ヤフー株式会社",
            "場所": f"{location}都",
            "給与": "年収600万円～"
        },
        {
            "番号": 2,
            "タイトル": f"Webアプリ{keyword}",
            "会社名": "株式会社ネットサービス",
            "場所": f"{location}都中央区",
            "給与": "月給40万円～"
        },
        {
            "番号": 3,
            "タイトル": f"{keyword}・エンジニア",
            "会社名": "株式会社システム開発",
            "場所": f"{location}都江東区",
            "給与": "年収500万円～800万円"
        },
    ]


async def scrape_townwork_demo(keyword: str = "プログラマー", location: str = "東京") -> List[Dict]:
    """タウンワーク スクレイピング（デモ版）"""
    await asyncio.sleep(1)

    return [
        {
            "番号": 1,
            "タイトル": f"{keyword}スタッフ",
            "会社名": "株式会社地域IT",
            "場所": f"{location}都内各所",
            "給与": "時給1500円～2000円"
        },
        {
            "番号": 2,
            "タイトル": f"IT{keyword}",
            "会社名": "株式会社ローカルテック",
            "場所": f"{location}都内",
            "給与": "月給30万円～"
        },
    ]
