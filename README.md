# Job Scraping System / 求人サイト スクレイピングシステム

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-1.40%2B-green?logo=playwright&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-GUI-red?logo=streamlit&logoColor=white)
![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript&logoColor=white)
![License](https://img.shields.io/badge/License-Educational-yellow)

**複数の求人サイトから効率的にデータを収集するためのスクレイピングシステム**

[クイックスタート](#-クイックスタート) • [機能](#-主な機能) • [GUI版](#-gui版) • [ドキュメント](#-ドキュメント)

</div>

---

## 目次

- [クイックスタート](#-クイックスタート)
- [重要な注意事項](#️-重要な注意事項)
- [主な機能](#-主な機能)
- [セットアップ](#-セットアップ)
- [使い方](#-2つの使い方)
- [GUI版](#-gui版react--typescript)
- [プロジェクト構造](#-プロジェクト構造)
- [新しいサイトの追加](#-新しいサイトの追加方法)
- [パフォーマンス](#-パフォーマンス)
- [トラブルシューティング](#️-トラブルシューティング)
- [今後の開発](#-今後の開発)
- [ライセンス](#-ライセンス)

---

## クイックスタート

**3分で実行可能！**

```bash
# 1. セットアップ検証
bash run.sh
# メニューで「0」を選択してセットアップを確認

# 2. 動作テスト
bash run.sh
# メニューで「1」を選択して基本動作を確認

# 3. 実際のスクレイピング
bash run.sh
# メニューで「2」を選択してIndeedからデータ取得
```

> 詳しい手順は **[START_HERE.md](START_HERE.md)** をご覧ください。

### GUI版クイックスタート

モダンなWeb UIで操作したい方：

```bash
bash start-gui.sh
# メニューで「1」を選択してセットアップ
# その後「4」を選択してアプリ起動
```

> 詳細: **[GUI_README.md](GUI_README.md)**

---

## 重要な注意事項

> **警告**: このシステムは**技術検証・学習目的**で開発されています。

| ルール | 詳細 |
|--------|------|
| 利用規約 | 各サイトの利用規約を必ず確認してください |
| 商用利用 | 避けてください |
| アクセス頻度 | 適切に制限してください |
| robots.txt | 尊重してください |

---

## 主な機能

### コア機能

| 機能 | 説明 |
|------|------|
| **複数サイト対応** | タウンワーク、バイトル、Indeed、Yahoo!しごと検索など |
| **並列処理** | 非同期処理による高速スクレイピング（最大50並列） |
| **柔軟な検索** | キーワード×地域の組み合わせ検索 |
| **データエクスポート** | CSV/Excel形式での出力 |

### GUI・管理機能

| 機能 | 説明 |
|------|------|
| **Streamlit GUI** | 直感的なWebインターフェース |
| **React + TypeScript GUI** | モダンなSPA（シングルページアプリ） |
| **セレクタ管理** | GUI上でセレクタの編集・管理が可能 |
| **データプレビュー** | 取得データのリアルタイムプレビュー |

### 技術的特徴

- **Stealth設定** - ヘッドレスブラウザ検出回避
- **実践的なページ待機** - 確実なデータ取得
- **セレクタ検証** - 実行前に確認
- **ブロック検出** - CAPTCHA/アクセス拒否の自動検出
- **デバッグツール** - スクリーンショット自動保存
- **詳細なロギング** - 問題の迅速な特定

---

## セットアップ

### 必要要件

- Python 3.9以上
- Node.js 18以上（GUI版を使用する場合）

### 最小限のセットアップ（シンプルスクレイパー用）

```bash
# 必須パッケージのインストール
pip3 install playwright pandas openpyxl

# Playwrightブラウザのインストール
playwright install chromium

# セットアップ検証
python3 verify_setup.py
```

### フルセットアップ（GUI版を使う場合）

```bash
# すべてのパッケージをインストール
pip3 install -r requirements.txt

# Playwrightブラウザのインストール
playwright install chromium
```

---

## 2つの使い方

### 方法1: シンプルスクリプト（推奨・初心者向け）

**特徴**:
- 1ファイル完結、すぐに実行可能
- 複雑な設定不要
- エラーに強い実装
- 実際のサイト（Indeed/Yahoo）で動作確認済み

**実行方法**:
```bash
# メニューから実行
bash run.sh

# または直接実行
python3 simple_scraper.py
```

**提供スクリプト**:

| スクリプト | 用途 |
|-----------|------|
| `verify_setup.py` | セットアップ検証 |
| `minimal_test.py` | 動作確認テスト |
| `simple_scraper.py` | シンプルスクレイパー（Indeed/Yahoo） |
| `convert_to_excel.py` | JSON→Excel変換 |
| `run.sh` | 便利なメニューランチャー |

### 方法2: Streamlit GUI版（高度な使い方）

**特徴**:
- Streamlit GUIで直感的に操作
- セレクタ管理機能
- データプレビュー機能
- 並列処理による高速化

**実行方法**:
```bash
streamlit run app.py
```

ブラウザが自動的に開き、GUIが表示されます（通常 http://localhost:8501）

---

## GUI版（React + TypeScript）

### 概要

最新のWebテクノロジーを使用したモダンなGUIを提供：

- **フロントエンド**: React 18.2 + TypeScript + Vite + Tailwind CSS
- **バックエンド**: FastAPI + Python

### GUI版の起動

```bash
# すべてを一括起動
bash start-gui.sh
# メニューで「4」を選択

# または手動で起動
# ターミナル1: バックエンド
cd backend && python main.py

# ターミナル2: フロントエンド
cd frontend && npm run dev
```

### 主な画面

1. **ダッシュボード** - 統計情報とクイックアクション
2. **スクレイピング実行** - 検索条件の設定と実行
3. **サイト管理** - セレクタの編集と管理
4. **データ確認** - 取得データの閲覧とエクスポート

---

## プロジェクト構造

```
TOWNWORK/
├── ドキュメント
│   ├── README.md                # このファイル
│   ├── START_HERE.md            # クイックスタートガイド
│   ├── README_PRODUCTION.md     # 本番運用ガイド
│   ├── GUI_README.md            # GUI版ガイド
│   └── GETTING_STARTED.md       # 詳細ガイド
│
├── シンプルスクリプト（すぐ実行可能）
│   ├── verify_setup.py          # セットアップ検証
│   ├── minimal_test.py          # 動作テスト
│   ├── simple_scraper.py        # シンプルスクレイパー
│   ├── convert_to_excel.py      # Excel変換
│   └── run.sh                   # メニューランチャー
│
├── Streamlit版
│   └── app.py                   # Streamlit GUIメインファイル
│
├── React GUI版
│   ├── frontend/                # React + TypeScript フロントエンド
│   │   ├── src/
│   │   │   ├── components/      # UIコンポーネント
│   │   │   ├── pages/           # ページコンポーネント
│   │   │   └── services/        # APIサービス
│   │   └── package.json
│   └── backend/                 # FastAPI バックエンド
│       └── main.py
│
├── コアモジュール
│   ├── config/
│   │   └── selectors.json       # サイトセレクタ設定
│   ├── scrapers/
│   │   ├── base_scraper.py      # ベーススクレイパー
│   │   ├── townwork.py          # タウンワーク
│   │   ├── baitoru.py           # バイトル
│   │   ├── indeed.py            # Indeed
│   │   └── ...                  # その他のサイト
│   └── utils/
│       ├── stealth.py           # ステルス設定
│       ├── page_utils.py        # ページユーティリティ
│       ├── retry.py             # リトライ処理
│       ├── user_agents.py       # User-Agent管理
│       ├── proxy.py             # プロキシ管理
│       └── performance.py       # パフォーマンス測定
│
└── 出力
    └── data/                    # スクレイピング結果
```

---

## 新しいサイトの追加方法

### 1. セレクタマッピングの作成

`config/selectors.json` に新しいサイトの設定を追加:

```json
{
  "new_site": {
    "name": "新サイト",
    "base_url": "https://example.com",
    "search_url_pattern": "https://example.com/search?q={keyword}&area={area}&page={page}",
    "selectors": {
      "job_cards": ".job-item",
      "title": ".job-title",
      "company": ".company-name",
      "location": ".location",
      "salary": ".salary"
    }
  }
}
```

### 2. スクレイパークラスの作成

`scrapers/new_site.py` を作成:

```python
from .base_scraper import BaseScraper

class NewSiteScraper(BaseScraper):
    def __init__(self):
        super().__init__(site_name="new_site")

    async def extract_detail_info(self, page, url):
        # 詳細ページの情報取得ロジック
        return {}
```

### 3. app.pyに登録

```python
from scrapers.new_site import NewSiteScraper

# get_scraper関数に追加
scrapers = {
    "townwork": TownworkScraper,
    "baitoru": BaitoruScraper,
    "indeed": IndeedScraper,
    "new_site": NewSiteScraper,  # 追加
}
```

---

## パフォーマンス

### 目標性能

| 条件 | 取得件数 | 目標時間 |
|------|---------|---------|
| 1サイト × 1条件 × 5ページ | 50件 | 3秒 |
| 1サイト × 10条件 × 5ページ | 500件 | 15秒 |
| 3サイト × 10条件 × 5ページ | 1,500件 | 1分 |

### 並列数の推奨設定

| 用途 | 並列数 | 安定性 |
|------|--------|--------|
| 軽量テスト | 5 | 高 |
| 通常使用 | 10-20 | 中 |
| 最大速度 | 50 | 低（リスク高） |

---

## トラブルシューティング

### セレクタが機能しない

1. サイトのHTML構造が変更された可能性があります
2. 「サイト管理」でセレクタを更新してください
3. Chrome DevToolsで正しいセレクタを確認できます

### データが取得できない

1. ブラウザのヘッドレスモードを無効にしてテスト
2. `scrapers/base_scraper.py` の `headless=False` に変更
3. 実際のブラウザ動作を確認

### アクセスが拒否される

- User-Agentの変更
- リクエスト間隔の調整
- 並列数を減らす

> 詳細なトラブルシューティングは **[README_PRODUCTION.md](README_PRODUCTION.md)** をご覧ください。

---

## 今後の開発

- [ ] エラーリトライ機能の強化
- [ ] プロキシローテーション対応
- [ ] スケジューラー機能（定期実行）
- [ ] セレクタ自動更新機能
- [ ] より詳細なログ機能
- [ ] 対応サイトの拡大

---

## ライセンス

このプロジェクトは**教育・研究目的**でのみ使用してください。

商用利用は禁止されています。

---

## コントリビューション

プルリクエスト歓迎！

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

---

<div align="center">

**開発者**: Claude Code + You

**最終更新**: 2025-11-26

---

Made with Playwright + React + FastAPI

</div>
