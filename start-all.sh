#!/bin/bash

echo "==========================================="
echo "求人スクレイピングシステム - 一括起動"
echo "==========================================="
echo ""

# カラーコード
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 現在のディレクトリ
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# プロセスIDを保存
BACKEND_PID=""
FRONTEND_PID=""

# クリーンアップ関数
cleanup() {
    echo ""
    echo -e "${YELLOW}終了処理中...${NC}"

    if [ ! -z "$BACKEND_PID" ]; then
        echo "バックエンドを停止中..."
        kill $BACKEND_PID 2>/dev/null
    fi

    if [ ! -z "$FRONTEND_PID" ]; then
        echo "フロントエンドを停止中..."
        kill $FRONTEND_PID 2>/dev/null
    fi

    echo -e "${GREEN}✅ 完了${NC}"
    exit 0
}

# Ctrl+C でクリーンアップ
trap cleanup SIGINT SIGTERM

echo -e "${BLUE}[1/2] バックエンドを起動中...${NC}"
cd backend
python3 main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# バックエンドの起動を待つ
echo "バックエンドの準備中（5秒待機）..."
sleep 5

# バックエンドが起動しているか確認
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✅ バックエンド起動成功 (PID: $BACKEND_PID)${NC}"
    echo "   URL: http://localhost:8000"
    echo "   ログ: backend.log"
else
    echo -e "${RED}❌ バックエンドの起動に失敗${NC}"
    echo "backend.log を確認してください"
    exit 1
fi

echo ""
echo -e "${BLUE}[2/2] フロントエンドを起動中...${NC}"
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# フロントエンドの起動を待つ
echo "フロントエンドの準備中（5秒待機）..."
sleep 5

# フロントエンドが起動しているか確認
if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${GREEN}✅ フロントエンド起動成功 (PID: $FRONTEND_PID)${NC}"
    echo "   URL: http://localhost:3000"
    echo "   ログ: frontend.log"
else
    echo -e "${RED}❌ フロントエンドの起動に失敗${NC}"
    echo "frontend.log を確認してください"
    cleanup
    exit 1
fi

echo ""
echo "==========================================="
echo -e "${GREEN}🎉 起動完了！${NC}"
echo "==========================================="
echo ""
echo "アクセス方法:"
echo "  📱 アプリ:        http://localhost:3000"
echo "  🔌 API:           http://localhost:8000"
echo "  📚 APIドキュメント: http://localhost:8000/docs"
echo ""
echo "ログ確認:"
echo "  バックエンド:  tail -f backend.log"
echo "  フロントエンド: tail -f frontend.log"
echo ""
echo -e "${YELLOW}終了するには Ctrl+C を押してください${NC}"
echo ""

# プロセスを待機
wait
