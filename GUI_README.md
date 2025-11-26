# React + TypeScript GUI 版

モダンなWeb UIで求人スクレイピングシステムを操作できます。

## 🎨 特徴

- **React + TypeScript** - 型安全な開発
- **Vite** - 高速なビルドとHMR
- **Tailwind CSS** - モダンなデザイン
- **FastAPI** - 高速バックエンドAPI
- **WebSocket** - リアルタイム進捗表示
- **zustand** - シンプルな状態管理

---

## 🚀 クイックスタート

### ステップ1: 初回セットアップ

```bash
cd /Users/kaz/TOWNWORK
bash start-gui.sh
```

メニューで **「1」** を選択 → 依存パッケージを自動インストール

所要時間: 2-3分

### ステップ2: アプリケーション起動

2つのターミナルを開いて実行：

**ターミナル1（バックエンド）:**
```bash
cd /Users/kaz/TOWNWORK/backend
python3 main.py
```

**ターミナル2（フロントエンド）:**
```bash
cd /Users/kaz/TOWNWORK/frontend
npm run dev
```

または、`start-gui.sh` でメニューから個別起動も可能。

---

## 📱 アクセス方法

起動後、以下のURLにアクセス：

- **フロントエンド（UI）**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **API ドキュメント**: http://localhost:8000/docs

---

## 🎯 使い方

### 1. サイト選択

トップページで対象サイトをクリックして選択：
- ✅ Indeed（動作確認済み）
- ✅ Yahoo!しごと検索（動作確認済み）
- ⏳ その他のサイト（準備中）

### 2. 検索条件入力

- **キーワード**: 例「プログラマー」「営業」
- **地域**: 例「東京」「大阪」
- **最大ページ数**: 1〜50

### 3. スクレイピング開始

**「スクレイピング開始」** ボタンをクリック

### 4. リアルタイム進捗確認

- 各サイトの進捗状況をリアルタイム表示
- プログレスバーで進行度を確認
- 取得件数をライブ更新

### 5. 結果確認とエクスポート

- テーブルで結果を確認
- **JSON** または **Excel** でダウンロード

---

## 📂 プロジェクト構造

```
TOWNWORK/
├── frontend/                 # React フロントエンド
│   ├── src/
│   │   ├── components/      # UI コンポーネント
│   │   │   ├── Header.tsx
│   │   │   ├── SiteSelector.tsx
│   │   │   ├── ConfigForm.tsx
│   │   │   ├── ProgressView.tsx
│   │   │   └── ResultsTable.tsx
│   │   ├── stores/          # Zustand 状態管理
│   │   │   └── scraper.ts
│   │   ├── services/        # API クライアント
│   │   │   └── api.ts
│   │   ├── types/           # TypeScript 型定義
│   │   │   └── index.ts
│   │   ├── App.tsx          # メインアプリ
│   │   └── main.tsx         # エントリーポイント
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── backend/                  # FastAPI バックエンド
│   ├── main.py              # API サーバー
│   └── requirements.txt
│
└── start-gui.sh              # 起動スクリプト
```

---

## 🔧 開発モード

### フロントエンド開発

```bash
cd frontend
npm run dev      # 開発サーバー起動
npm run build    # プロダクションビルド
npm run preview  # ビルド結果をプレビュー
```

### バックエンド開発

```bash
cd backend
python3 main.py  # APIサーバー起動（自動リロード有効）
```

### ホットリロード

- フロントエンド: ファイル保存で自動更新
- バックエンド: `uvicorn --reload` で自動再起動

---

## 🌐 API エンドポイント

### GET /api/sites
サイト一覧を取得

### POST /api/scrape/start
スクレイピング開始
```json
{
  "configs": [
    {
      "site": "indeed",
      "keyword": "プログラマー",
      "location": "東京",
      "maxPages": 5
    }
  ]
}
```

### GET /api/scrape/status/{sessionId}
スクレイピング状態取得

### WebSocket /ws/{sessionId}
リアルタイム進捗通知

詳細: http://localhost:8000/docs

---

## 🎨 カスタマイズ

### サイトの追加

**1. backend/main.py の SITES に追加:**
```python
{
    "id": "new_site",
    "name": "新サイト",
    "description": "説明",
    "enabled": True,
    "icon": "🔥"
}
```

**2. スクレイパー関数を作成**

**3. backend/main.py の run_scraping() に統合**

### デザインの変更

`frontend/tailwind.config.js` でカラーテーマを編集：

```javascript
colors: {
  primary: {
    500: '#0ea5e9',  // メインカラー
    600: '#0284c7',
    // ...
  },
}
```

---

## 🐛 トラブルシューティング

### ポートが使用中

```bash
# 8000番ポートを使用中のプロセスを確認
lsof -ti:8000

# プロセスを終了
kill -9 $(lsof -ti:8000)

# または別のポートを使用
# backend/main.py の最終行を変更
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### WebSocket 接続エラー

1. バックエンドが起動しているか確認
2. CORS設定を確認（backend/main.py）
3. ブラウザのコンソールでエラーを確認

### npm install エラー

```bash
# キャッシュクリア
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 パフォーマンス

### 期待される性能

| サイト数 | 取得件数 | 所要時間 |
|---------|---------|---------|
| 1サイト | 10件 | 5-10秒 |
| 2サイト | 20件 | 10-15秒 |
| 5サイト | 50件 | 30-40秒 |

※ ネットワーク環境により変動

---

## 🔐 セキュリティ

### 本番環境への展開

**環境変数を設定:**
```bash
# frontend/.env
VITE_API_URL=https://api.example.com

# backend/.env
ALLOWED_ORIGINS=https://app.example.com
```

**CORS設定を更新:**
```python
# backend/main.py
allow_origins=["https://app.example.com"]
```

---

## 📝 今後の拡張

- [ ] ユーザー認証機能
- [ ] 保存した検索条件の再利用
- [ ] スケジューラー（定期実行）
- [ ] データ分析・可視化
- [ ] 通知機能（メール/Slack）
- [ ] 複数ページの並列取得
- [ ] 残り8サイトの対応

---

## 💡 Tips

### 高速化のコツ

1. **並列実行**: 複数サイトを同時実行
2. **ページ数制限**: 必要最小限のページ数に
3. **キーワード最適化**: 具体的なキーワードで検索

### データ活用

1. **Excel でフィルタリング**
2. **給与データで並べ替え**
3. **地域でグループ化**

---

**開発者**: Claude Code + You
**バージョン**: 1.0.0
**最終更新**: 2025-11-18
