# 🚀 ここから始めてください

実際に動くコードで今すぐテスト

---

## ⚡ 超クイックスタート（3分）

### Step 1: セットアップ

```bash
cd /Users/kaz/TOWNWORK

# 依存パッケージをインストール
pip install playwright pandas openpyxl

# Playwrightブラウザをインストール
playwright install chromium
```

### Step 2: 動作確認テスト

```bash
python minimal_test.py
```

**選択: 1** (基本テスト)

**期待される動作**:
1. ブラウザが開く
2. Googleが表示される
3. スクリーンショットが保存される
4. "すべて正常に動作しました！"と表示

---

## 🎯 実際のスクレイピングを試す

### 方法1: シンプルスクレイパー（推奨）

```bash
python simple_scraper.py
```

**選択: 1** (Indeed)

**何が起こるか**:
1. ブラウザが開いてIndeedにアクセス
2. "プログラマー 東京"で検索
3. 求人データを10件取得
4. JSONファイルとスクリーンショットを保存
5. 結果がコンソールに表示される

**出力ファイル**:
- `indeed_jobs_YYYYMMDD_HHMMSS.json` - 取得データ
- `screenshot_YYYYMMDD_HHMMSS.png` - スクリーンショット

### 方法2: Indeedアクセステスト

```bash
python minimal_test.py
```

**選択: 2** (Indeedアクセステスト)

**何を確認できるか**:
- Indeedにアクセスできるか
- ブロックされていないか
- 検索ボックスが動作するか
- 求人カードが検出できるか

---

## 📊 結果の確認

### 取得データの確認

```bash
# 最新のJSONファイルを確認
ls -lt *.json | head -1

# ファイルの内容を表示
cat indeed_jobs_*.json
```

**JSONの中身例**:
```json
[
  {
    "番号": 1,
    "タイトル": "Webエンジニア（フルスタック）",
    "会社名": "株式会社Example",
    "場所": "東京都渋谷区",
    "給与": "年収500万円～800万円"
  },
  ...
]
```

### スクリーンショットの確認

```bash
# スクリーンショットを開く
open screenshot_*.png

# 最新のものを開く
open $(ls -t screenshot_*.png | head -1)
```

---

## 🔧 カスタマイズ方法

### 検索条件を変更

`simple_scraper.py` の18-19行目を編集：

```python
# 変更前
keyword = "プログラマー"
location = "東京"

# 変更後
keyword = "営業"
location = "大阪"
```

### 取得件数を変更

79行目を編集：

```python
# 変更前
for i, card in enumerate(job_cards[:10], 1):  # 10件

# 変更後
for i, card in enumerate(job_cards[:50], 1):  # 50件
```

---

## ⚠️ トラブルシューティング

### 問題1: `playwright`が見つからない

```bash
pip install playwright
playwright install chromium
```

### 問題2: ブラウザが起動しない

`simple_scraper.py` の30行目を確認：

```python
headless=False,  # これでブラウザが表示される
```

`headless=True` に変更するとバックグラウンド実行になります。

### 問題3: データが取得できない

1. **スクリーンショットを確認**
   ```bash
   open error_screenshot.png
   ```

2. **ブロックされていないか確認**
   - 画像に "Access Denied" が表示されている
   - CAPTCHAが表示されている

3. **対処法**:
   - 少し時間を置いてから再試行
   - 別のサイト（Yahoo!しごと検索）を試す

### 問題4: エラーメッセージが出る

```
TimeoutError: Timeout 30000ms exceeded
```

**解決**: ネットワーク接続を確認。タイムアウトを延長：

```python
# 90行目あたり
await page.goto(url, wait_until="domcontentloaded", timeout=60000)  # 30秒→60秒
```

---

## 📈 次のステップ

### 1. Yahoo!しごと検索も試す

```bash
python simple_scraper.py
# 選択: 2
```

### 2. 複数サイトを試す

```bash
python simple_scraper.py
# 選択: 3 (両方実行)
```

### 3. データをExcelで開く

```python
# excel_converter.py を作成して実行
import pandas as pd
import json

with open('indeed_jobs_最新のファイル名.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

df = pd.DataFrame(data)
df.to_excel('求人データ.xlsx', index=False)
print("Excelファイル保存完了: 求人データ.xlsx")
```

---

## 🎓 動作原理の理解

### シンプルスクレイパーの流れ

```
1. Playwrightでブラウザ起動
   ↓
2. Indeedにアクセス
   ↓
3. ページ読み込み待機
   ↓
4. 求人カードを探す（複数のセレクタを試す）
   ↓
5. 各カードからデータ抽出
   ↓
6. JSONファイルに保存
   ↓
7. スクリーンショット保存
   ↓
8. ブラウザを閉じる
```

### なぜ動くのか？

1. **複数のセレクタを試す**
   ```python
   selectors_to_try = [
       ".job_seen_beacon",
       ".jobsearch-SerpJobCard",
       "div[data-jk]"
   ]
   ```
   サイトの構造が変わっても対応できる

2. **エラーハンドリング**
   ```python
   try:
       # データ抽出
   except Exception as e:
       print(f"エラー: {e}")
       continue  # エラーが出ても続行
   ```

3. **人間らしい動作**
   ```python
   await asyncio.sleep(3)  # 3秒待機
   ```

---

## 💡 成功のコツ

### ✅ やるべきこと

1. **まず minimal_test.py で動作確認**
2. **少量のデータから始める**（10件程度）
3. **スクリーンショットを必ず確認**
4. **エラーが出ても慌てない**（ログを読む）

### ❌ やってはいけないこと

1. いきなり大量実行
2. エラーを無視
3. 高速すぎる実行（待機時間0秒など）
4. 同じサイトへの連続アクセス

---

## 🎉 成功の確認

以下ができればOK：

- [ ] `minimal_test.py` が正常に動作
- [ ] Googleのスクリーンショットが保存される
- [ ] `simple_scraper.py` でデータが取得できる
- [ ] JSONファイルに10件のデータが保存される
- [ ] エラーが出ても対処できる

---

## 📞 次に読むドキュメント

- `simple_scraper.py` のコードを読む
- `README_PRODUCTION.md` - より高度な機能
- `FEATURES.md` - 全機能の説明

---

**最初は simple_scraper.py から始めてください！**

**質問があれば、エラーメッセージとスクリーンショットを確認してください。**

**最終更新**: 2025-11-18
