#!/bin/bash

echo "==========================================="
echo "求人スクレイピングシステム - React版"
echo "==========================================="
echo ""

# カラーコード
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 現在のディレクトリを確認
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# メニュー表示
echo "起動オプションを選択してください:"
echo ""
echo "1. 初回セットアップ（パッケージインストール）"
echo "2. バックエンドのみ起動（FastAPI）"
echo "3. フロントエンドのみ起動（React）"
echo "4. フルスタック起動（バックエンド + フロントエンド）"
echo "5. 終了"
echo ""
echo "==========================================="
echo ""

read -p "選択 (1-5): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}初回セットアップを開始します...${NC}"
        echo ""

        # バックエンドのセットアップ
        echo -e "${YELLOW}[1/3] バックエンドの依存パッケージをインストール中...${NC}"
        cd backend
        pip3 install -r requirements.txt
        cd ..
        echo -e "${GREEN}✅ バックエンド完了${NC}"
        echo ""

        # Playwrightのインストール
        echo -e "${YELLOW}[2/3] Playwrightブラウザをインストール中...${NC}"
        playwright install chromium
        echo -e "${GREEN}✅ Playwright完了${NC}"
        echo ""

        # フロントエンドのセットアップ
        echo -e "${YELLOW}[3/3] フロントエンドの依存パッケージをインストール中...${NC}"
        cd frontend
        npm install
        cd ..
        echo -e "${GREEN}✅ フロントエンド完了${NC}"
        echo ""

        echo -e "${GREEN}🎉 セットアップ完了！${NC}"
        echo ""
        echo "次のステップ:"
        echo "  bash start-gui.sh を実行して「4」を選択"
        ;;

    2)
        echo ""
        echo -e "${BLUE}バックエンドを起動します...${NC}"
        echo ""
        echo "APIドキュメント: http://localhost:8000/docs"
        echo ""
        cd backend
        python3 main.py
        ;;

    3)
        echo ""
        echo -e "${BLUE}フロントエンドを起動します...${NC}"
        echo ""
        echo "アプリケーション: http://localhost:3000"
        echo ""
        cd frontend
        npm run dev
        ;;

    4)
        echo ""
        echo -e "${BLUE}フルスタック起動します...${NC}"
        echo ""
        echo "バックエンド: http://localhost:8000"
        echo "フロントエンド: http://localhost:3000"
        echo ""
        echo "新しいターミナルで以下を実行してください:"
        echo ""
        echo -e "${YELLOW}ターミナル1:${NC}"
        echo "  cd $SCRIPT_DIR/backend && python3 main.py"
        echo ""
        echo -e "${YELLOW}ターミナル2:${NC}"
        echo "  cd $SCRIPT_DIR/frontend && npm run dev"
        echo ""
        echo "または、tmuxを使用:"
        echo "  tmux new-session -d -s scraper 'cd $SCRIPT_DIR/backend && python3 main.py'"
        echo "  tmux split-window -h 'cd $SCRIPT_DIR/frontend && npm run dev'"
        echo "  tmux attach -t scraper"
        ;;

    5)
        echo "終了します"
        exit 0
        ;;

    *)
        echo "無効な選択です"
        exit 1
        ;;
esac

echo ""
echo "==========================================="
echo "完了"
echo "==========================================="
