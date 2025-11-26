# 🚀 はじめに - 実際に動かす手順

本番環境で実際に動作するシステムの使い方

---

## ⚡ クイックスタート（5分）

### Step 1: セットアップ

```bash
cd /Users/kaz/TOWNWORK

# 依存パッケージをインストール
bash setup.sh

# スクリーンショット用ディレクトリ作成
mkdir -p data/screenshots
```

### Step 2: テストツールで動作確認

```bash
python test_scraper.py
```

**選択: 3** (クイックテスト)を選んでEnter

**確認事項**:
- ✅ ブラウザが起動してタウンワークにアクセスするか
- ✅ スクリーンショットが保存されるか (`data/screenshots/`)
- ✅ エラーが出ないか

### Step 3: 結果確認

```bash
# スクリーンショットを確認
open data/screenshots/

# 最新のスクリーンショットを開く
open data/screenshots/townwork_*.png
```

---

## 🎯 次のステップ

### 実際のサイトでセレクタを確認

1. **ブラウザでタウンワークを開く**
   ```
   https://townwork.net/tokyo/search/
   ```

2. **Chrome DevToolsを開く** (F12またはCmd+Opt+I)

3. **求人カード要素を調査**
   - 求人カードを右クリック → 「検証」
   - セレクタを確認

4. **Console で動作確認**
   ```javascript
   // 求人カードの数を確認
   document.querySelectorAll('.list-jobListDetail').length

   // タイトルを確認
   document.querySelector('.list-jobListDetail__title').innerText
   ```

5. **セレクタが機能していれば次へ**

---

## 📝 セレクタのテスト

### 全セレクタの動作確認

```bash
python test_scraper.py
```

**選択: 2** (セレクタテスト)
**サイト名: townwork**

**実行結果の見方**:
```
✅ job_cards: 20 elements     # → OK! 求人カードが取得できている
✅ title: 20 elements         # → OK!
❌ company: 0 elements        # → NG! セレクタが間違っている
```

### セレクタの修正

`config/selectors.json`を編集：

```json
{
  "townwork": {
    "selectors": {
      "company": ".list-jobListDetail__company"  // 正しいセレクタに修正
    }
  }
}
```

---

## 🔧 デバッグモード

### ブラウザを表示して確認

`test_scraper.py` の19行目を編集：

```python
# 変更前
tester = ScraperTester(debug_mode=True)

# 変更後（ヘッドレスモード）
tester = ScraperTester(debug_mode=False)
```

`debug_mode=True` の場合：
- ブラウザが表示される
- 動作を目視確認できる
- CAPTCHAが出たら手動で対応可能

---

## 🎨 GUI版の実行

セレクタのテストが完了したら、GUI版を起動：

```bash
streamlit run app.py
```

### 小規模テスト実行

1. **サイト選択**: ☑ タウンワーク
2. **検索条件**:
   - キーワード: `アルバイト`
   - 地域: `東京`
3. **設定**:
   - 最大ページ数: `2`
   - 並列数: `3`
4. **🚀 スクレイピング開始**

**期待結果**:
- 30秒〜1分で完了
- 10-40件程度のデータ取得
- エラー率 < 10%

---

## ⚠️ トラブルシューティング

### 問題: データが取得できない

**症状**:
```
WARNING - Job cards selector not found
```

**解決**:
1. Chrome DevToolsでセレクタを確認
2. スクリーンショットを確認 (`data/screenshots/`)
3. `config/selectors.json`のセレクタを更新
4. 再度テスト実行

### 問題: CAPTCHAが表示される

**症状**:
```
WARNING - CAPTCHA detected
```

**解決**:
1. デバッグモードで実行
2. 手動でCAPTCHAを解決
3. アクセス頻度を下げる（並列数を3以下に）
4. 待機時間を増やす

### 問題: アクセスがブロックされる

**症状**:
```
ERROR - Access blocked
```

**解決**:
1. User-Agentを確認（自動ローテーション済み）
2. 並列数を減らす（3〜5）
3. 待機時間を増やす（3〜5秒）
4. プロキシを使用

---

## 📊 実行結果の確認

### ログの見方

```
INFO - Scraping: https://townwork.net/tokyo/search/
INFO - Found 20 job cards
INFO - Successfully extracted 18 jobs
```

**解釈**:
- 20個の求人カード検出
- 18個のデータを抽出（成功率90%）
- 2個は情報不足でスキップ

### スクリーンショットの活用

```bash
# 最新のスクリーンショットを確認
ls -lt data/screenshots/ | head -5
open data/screenshots/townwork_*.png
```

**確認事項**:
- ページが正常に表示されているか
- CAPTCHAが表示されていないか
- 求人カードが表示されているか
- ブロックメッセージが表示されていないか

---

## 🎯 本番実行の推奨設定

### 安全な設定（推奨）

```
サイト数: 1-2
キーワード数: 1-3
地域数: 1-2
最大ページ数: 2-5
並列数: 3-5
```

**期待結果**:
- 実行時間: 1-3分
- 取得件数: 20-100件
- エラー率: < 10%
- ブロック率: ほぼ0%

### バランス型

```
サイト数: 3-5
キーワード数: 3-5
地域数: 2-3
最大ページ数: 3-5
並列数: 5-10
```

**期待結果**:
- 実行時間: 3-10分
- 取得件数: 100-500件
- エラー率: < 15%
- ブロック率: < 5%

### 高速型（リスク高）

```
サイト数: 5-11
キーワード数: 5-10
地域数: 3-5
最大ページ数: 5-10
並列数: 10-20
```

**リスク**:
- ブロックされる可能性が高い
- CAPTCHA が表示される可能性
- IP BAN のリスク

---

## 📈 成功の指標

### テスト段階

- [x] test_scraper.py が正常に動作
- [x] セレクタが要素を検出
- [x] スクリーンショットが正常に保存
- [x] ブロックされない

### 本番実行

- [x] エラー率 < 15%
- [x] 取得件数が期待値の70%以上
- [x] ブロック検出なし
- [x] 実行完了

---

## 🔄 継続的な運用

### セレクタのメンテナンス

**頻度**: 1-3ヶ月ごと

1. `test_scraper.py` でテスト実行
2. 動作しないセレクタを特定
3. Chrome DevToolsで新しいセレクタを調査
4. `config/selectors.json` を更新

### パフォーマンス監視

各実行後に確認：
- エラー率
- 取得件数
- 実行時間
- ブロック回数

エラー率が20%を超えたら設定見直し。

---

## 📞 次のステップ

### 詳細ドキュメント

- `README_PRODUCTION.md` - 本番環境の詳細
- `FEATURES.md` - 全機能の説明
- `PROJECT_SUMMARY.md` - プロジェクト概要

### 高度な機能

- プロキシの設定
- カスタムセレクタの追加
- 新サイトの追加
- パフォーマンスチューニング

---

**重要**: まずは小規模なテストから始めて、徐々にスケールアップしてください。

**最終更新**: 2025-11-18
