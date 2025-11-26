#!/bin/bash

echo "==========================================="
echo "求人スクレイピングシステム - tmux起動"
echo "==========================================="
echo ""

# 現在のディレクトリ
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SESSION_NAME="job-scraper"

# tmuxがインストールされているか確認
if ! command -v tmux &> /dev/null; then
    echo "❌ tmux がインストールされていません"
    echo ""
    echo "インストール方法:"
    echo "  macOS: brew install tmux"
    echo "  Linux: sudo apt install tmux"
    echo ""
    echo "または start-all.sh を使用してください"
    exit 1
fi

# 既存のセッションを終了
tmux kill-session -t $SESSION_NAME 2>/dev/null

echo "tmuxセッションを作成中..."
echo ""

# 新しいセッションを作成してバックエンドを起動
tmux new-session -d -s $SESSION_NAME -n "Job Scraper" \
    "cd $SCRIPT_DIR/backend && echo '🔌 バックエンド起動中...' && python3 main.py"

# ウィンドウを分割してフロントエンドを起動
tmux split-window -h -t $SESSION_NAME \
    "cd $SCRIPT_DIR/frontend && echo '⚛️  フロントエンド起動中...' && sleep 3 && npm run dev"

# レイアウトを調整
tmux select-layout -t $SESSION_NAME even-horizontal

echo "✅ tmuxセッション作成完了"
echo ""
echo "==========================================="
echo "起動情報"
echo "==========================================="
echo ""
echo "📱 アプリ:          http://localhost:3000"
echo "🔌 API:             http://localhost:8000"
echo "📚 APIドキュメント:  http://localhost:8000/docs"
echo ""
echo "==========================================="
echo "tmux操作方法"
echo "==========================================="
echo ""
echo "  Ctrl+B → 矢印キー : ペインの移動"
echo "  Ctrl+B → d        : デタッチ（バックグラウンド実行）"
echo "  Ctrl+B → &        : セッション終了"
echo ""
echo "デタッチ後に再接続:"
echo "  tmux attach -t $SESSION_NAME"
echo ""
echo "セッションを終了:"
echo "  tmux kill-session -t $SESSION_NAME"
echo ""

# セッションにアタッチ
tmux attach -t $SESSION_NAME
