# 🚀 本番環境向けセットアップガイド

実際に動作するスクレイピングシステムの構築手順

---

## ⚠️ 重要な改善点

従来版からの主な変更：

### ✅ 実装した本番対応機能

1. **Stealth設定** - ヘッドレスブラウザ検出回避
2. **実践的なページ待機** - 確実なデータ取得
3. **セレクタ検証** - 実行前に確認
4. **ブロック検出** - CAPTCHA/アクセス拒否の自動検出
5. **デバッグツール** - スクリーンショット自動保存
6. **詳細なロギング** - 問題の迅速な特定

---

## 📋 セットアップ手順

### 1. 基本インストール

```bash
cd /Users/kaz/TOWNWORK
bash setup.sh
```

### 2. スクリーンショットディレクトリ作成

```bash
mkdir -p data/screenshots
```

---

## 🧪 テスト実行（重要！）

**本番実行前に必ずテストしてください**

### テストツールの実行

```bash
python test_scraper.py
```

#### オプション1: サイトアクセステスト

```
選択: 1
サイト名: townwork
URL: https://townwork.net/tokyo/search/
```

**確認事項**:
- ✅ ページが正常に読み込まれるか
- ✅ ブロックされていないか
- ✅ CAPTCHAが表示されていないか
- ✅ スクリーンショットが保存されるか

#### オプション2: セレクタテスト

```
選択: 2
サイト名: townwork
```

**確認事項**:
- 各セレクタが実際のサイトで機能するか
- 取得できる要素数
- サンプルテキストの内容

#### オプション3: クイックテスト

```
選択: 3
```

タウンワークの基本的な動作確認

---

## 🔧 実サイトでのセレクタ調査

### Chrome DevToolsを使用

1. **対象サイトを開く**
   ```
   https://townwork.net/tokyo/search/
   ```

2. **DevToolsを開く** (F12 または Cmd+Opt+I)

3. **Elements タブで要素を調査**
   - 求人カードを右クリック → 検証
   - セレクタをコピー

4. **Console で確認**
   ```javascript
   // 要素数を確認
   document.querySelectorAll('.list-jobListDetail').length

   // テキスト取得テスト
   document.querySelector('.list-jobListDetail__title').innerText
   ```

5. **`config/selectors.json` を更新**

---

## 🎯 実際のセレクタ例（タウンワーク）

```json
{
  "townwork": {
    "name": "タウンワーク",
    "base_url": "https://townwork.net",
    "search_url_pattern": "https://townwork.net/{area}/search/?keyword={keyword}",
    "selectors": {
      "job_cards": ".list-jobListDetail",
      "title": ".list-jobListDetail__title a",
      "company": ".list-jobListDetail__company",
      "location": ".list-jobListDetail__access",
      "salary": ".list-jobListDetail__salary",
      "employment_type": ".list-jobListDetail__tag",
      "detail_link": ".list-jobListDetail__title a"
    }
  }
}
```

**※ 実際のサイトで確認して更新してください**

---

## 🛠️ デバッグモード

### ヘッドレスモードをオフにして確認

`test_scraper.py` を編集：

```python
tester = ScraperTester(debug_mode=True)  # ブラウザが表示される
```

**メリット**:
- ブラウザの動作を目視確認
- CAPTCHAの手動対応
- セレクタの動作確認

---

## 🔍 トラブルシューティング

### 問題1: セレクタが見つからない

**症状**:
```
WARNING - Job cards selector not found: .job-item
```

**解決方法**:
1. テストツールでセレクタを確認
2. スクリーンショットを確認 (`data/screenshots/`)
3. Chrome DevToolsで実際のセレクタを調査
4. `config/selectors.json` を更新

### 問題2: アクセスがブロックされる

**症状**:
```
ERROR - Access blocked: ['Access Denied']
```

**解決方法**:
1. User-Agentを確認
2. アクセス頻度を下げる（並列数を減らす）
3. プロキシを使用
4. 待機時間を増やす

```python
# base_scraper.py の待機時間を調整
await asyncio.sleep(3)  # 1秒 → 3秒
```

### 問題3: CAPTCHAが表示される

**症状**:
```
WARNING - CAPTCHA detected
```

**対応**:
1. 一時的にアクセスを停止
2. 手動でCAPTCHAを解決
3. アクセス頻度を大幅に下げる
4. デバッグモードで手動対応

---

## 📊 実行モード

### 開発モード（推奨 - 初回）

```python
# test_scraper.py
tester = ScraperTester(debug_mode=True)
```

- ヘッドレスオフ
- 詳細ログ
- スクリーンショット自動保存
- ブラウザ表示

### 本番モード

```python
# デバッグモードオフ
tester = ScraperTester(debug_mode=False)
```

- ヘッドレスオン
- 高速実行
- リソース節約

---

## 🎛️ パフォーマンスチューニング

### 並列数の調整

```python
# 低速だが安定
parallel = 3

# バランス型
parallel = 5-10

# 高速だがリスク高
parallel = 20+
```

### 待機時間の調整

```python
# 検出回避重視
wait_time = 3.0 + random.random() * 2.0  # 3-5秒

# 速度重視
wait_time = 0.5  # 0.5秒
```

---

## 📝 実行ログの確認

### ログレベルの調整

```python
# base_scraper.py
logging.basicConfig(level=logging.DEBUG)  # 詳細ログ
logging.basicConfig(level=logging.INFO)   # 通常
logging.basicConfig(level=logging.WARNING) # 警告のみ
```

### ログファイルへの出力

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🔐 セキュリティ対策

### プロキシの使用

```python
from utils import proxy_rotator

# プロキシ追加
proxy_rotator.add_proxy("http://proxy.example.com:8080")
proxy_rotator.enable()
```

### User-Agentのローテーション

自動的に適用されますが、カスタマイズも可能：

```python
from utils import ua_rotator

# Chrome系のみ使用
ua_rotator.USER_AGENTS = [
    ua for ua in ua_rotator.USER_AGENTS
    if "Chrome" in ua
]
```

---

## 📈 成功の指標

### テスト段階

- ✅ サイトアクセステストが成功
- ✅ セレクタが要素を検出
- ✅ ブロックされない
- ✅ スクリーンショットが正常

### 本番実行

- ✅ エラー率 < 10%
- ✅ 取得件数が期待値の80%以上
- ✅ ブロック検出なし
- ✅ 実行時間が許容範囲内

---

## 🚀 本番実行の流れ

### 1. テスト実行

```bash
python test_scraper.py
# → 選択: 2 (全セレクタテスト)
# → サイト名: townwork
```

### 2. 結果確認

- ログを確認
- スクリーンショットを確認 (`data/screenshots/`)
- 取得できたデータを確認

### 3. 設定調整

問題があれば`config/selectors.json`を更新

### 4. GUI実行

```bash
streamlit run app.py
```

- 小規模テスト（1サイト × 1キーワード × 2ページ）
- 結果を確認
- 問題なければスケールアップ

---

## ⚠️ 本番運用の注意点

### 1. アクセス頻度

- **推奨**: 並列5-10、ページ間2-3秒待機
- **非推奨**: 並列50、待機なし

### 2. エラーハンドリング

- エラー率が10%超えたら停止
- ブロック検出されたら即停止
- CAPTCHAが出たら手動対応

### 3. データ品質

- 取得データの検証
- 欠損データの確認
- 重複データの除去

### 4. 法的・倫理的配慮

- 利用規約の遵守
- 適切なアクセス頻度
- データの適切な利用

---

## 📞 サポート

### デバッグ情報の収集

問題が発生した場合：

1. エラーログをコピー
2. スクリーンショットを確認
3. 再現手順を記録
4. 使用したセレクタを記録

### 確認事項チェックリスト

- [ ] Playwrightがインストールされているか
- [ ] ブラウザがインストールされているか (`playwright install chromium`)
- [ ] セレクタが最新か
- [ ] サイトがアクセス可能か
- [ ] ネットワーク接続は正常か

---

**重要**: このシステムは技術検証目的です。商用利用や大量アクセスは避けてください。

**最終更新**: 2025-11-18
