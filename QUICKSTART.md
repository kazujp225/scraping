# 🚀 クイックスタート - 起動方法まとめ

すべての起動方法を1ページにまとめました。

---

## 📱 GUI版（React + TypeScript）- 3つの起動方法

### 方法1: 一括起動スクリプト（最も簡単！）⭐

**1つのコマンドで起動：**

```bash
cd /Users/kaz/TOWNWORK
bash start-all.sh
```

**特徴：**
- ✅ 1コマンドで完結
- ✅ バックエンド・フロントエンド自動起動
- ✅ ログファイルに出力（backend.log / frontend.log）
- ✅ Ctrl+C で両方とも停止

**アクセス：**
- アプリ: http://localhost:3000
- API: http://localhost:8000

---

### 方法2: tmux版（開発者向け）

**2画面分割で起動：**

```bash
cd /Users/kaz/TOWNWORK
bash start-tmux.sh
```

**特徴：**
- ✅ 画面が左右2つに分割
- ✅ 各ログをリアルタイム表示
- ✅ Ctrl+B → d でバックグラウンド実行可能
- ✅ 見やすい

**tmux操作：**
- `Ctrl+B` → `矢印キー` : ペイン移動
- `Ctrl+B` → `d` : デタッチ（バックグラウンド）
- `Ctrl+B` → `&` : 終了

**再接続：**
```bash
tmux attach -t job-scraper
```

---

### 方法3: npm scripts（Node.js使い慣れている方向け）

**frontendディレクトリから起動：**

```bash
cd /Users/kaz/TOWNWORK/frontend
npm run dev:all
```

**特徴：**
- ✅ 1コマンドで起動
- ✅ カラフルなログ表示
- ✅ concurrently で並列実行

**初回のみ：**
```bash
cd frontend
npm install  # concurrently をインストール
```

---

## 💻 CLI版（シンプルスクリプト）

**メニュー形式：**

```bash
cd /Users/kaz/TOWNWORK
bash run.sh
```

**メニュー：**
- **0** - セットアップ検証
- **1** - 動作テスト
- **2** - スクレイピング実行（Indeed/Yahoo）
- **3** - Excel変換
- **4** - 依存パッケージインストール

---

## 🔧 初回セットアップ

### GUI版の初回セットアップ

```bash
cd /Users/kaz/TOWNWORK
bash start-gui.sh
```

メニューで **「1」** を選択 → 自動インストール（2-3分）

**インストールされるもの：**
- バックエンド依存パッケージ（FastAPI、uvicorn、websockets）
- Playwright ブラウザ（chromium）
- フロントエンド依存パッケージ（React、Vite、Tailwind）

### CLI版の初回セットアップ

```bash
cd /Users/kaz/TOWNWORK
bash run.sh
```

メニューで **「4」** を選択

---

## 📊 起動方法の比較

| 方法 | コマンド | 特徴 | おすすめ度 |
|------|---------|------|-----------|
| **start-all.sh** | `bash start-all.sh` | 最も簡単、1コマンド | ⭐⭐⭐⭐⭐ |
| **start-tmux.sh** | `bash start-tmux.sh` | 2画面分割、見やすい | ⭐⭐⭐⭐ |
| **npm run dev:all** | `cd frontend && npm run dev:all` | Node.js標準 | ⭐⭐⭐ |
| **run.sh** | `bash run.sh` | CLI版 | ⭐⭐⭐⭐⭐ |

---

## 🎯 用途別おすすめ

### 初めての方
```bash
bash run.sh  # メニュー「0」でセットアップ確認
```

### 簡単にGUI起動したい
```bash
bash start-all.sh
```

### 開発しながら使う
```bash
bash start-tmux.sh
```

### すぐにデータ取得したい
```bash
bash run.sh  # メニュー「2」
```

---

## 🛑 停止方法

### start-all.sh の停止
```bash
Ctrl+C  # 両方とも自動停止
```

### start-tmux.sh の停止
```bash
Ctrl+B → &  # セッション終了
# または
tmux kill-session -t job-scraper
```

### npm run dev:all の停止
```bash
Ctrl+C  # 両方とも停止
```

---

## ⚡ トラブルシューティング

### ポートが使用中

```bash
# 8000番ポートを使用中のプロセスを確認・終了
lsof -ti:8000 | xargs kill -9

# 3000番ポートを使用中のプロセスを確認・終了
lsof -ti:3000 | xargs kill -9
```

### tmux がない

```bash
# macOS
brew install tmux

# Linux (Ubuntu/Debian)
sudo apt install tmux
```

### npm install エラー

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📝 まとめ

**一番簡単な起動方法：**

```bash
cd /Users/kaz/TOWNWORK
bash start-all.sh
```

これだけで、バックエンド + フロントエンドが起動します！

http://localhost:3000 にアクセスして開始 🎉

---

**最終更新**: 2025-11-18
