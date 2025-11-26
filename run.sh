#!/bin/bash

echo "========================================="
echo "求人スクレイピングシステム"
echo "========================================="
echo ""

# Pythonのチェック
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 がインストールされていません"
    exit 1
fi

echo "Python: $(python3 --version)"
echo ""

# メニュー表示
echo "実行するスクリプトを選択してください:"
echo ""
echo "0. セットアップ検証 (verify_setup.py)"
echo "1. 動作確認テスト (minimal_test.py)"
echo "2. シンプルスクレイパー (simple_scraper.py)"
echo "3. Excel変換 (convert_to_excel.py)"
echo "4. 依存パッケージのインストール"
echo "5. 終了"
echo ""
echo "========================================="
echo ""

read -p "選択 (0-5): " choice

case $choice in
    0)
        echo ""
        echo "セットアップを検証します..."
        python3 verify_setup.py
        ;;
    1)
        echo ""
        echo "動作確認テストを実行します..."
        python3 minimal_test.py
        ;;
    2)
        echo ""
        echo "シンプルスクレイパーを実行します..."
        python3 simple_scraper.py
        ;;
    3)
        echo ""
        echo "Excel変換を実行します..."
        python3 convert_to_excel.py
        ;;
    4)
        echo ""
        echo "依存パッケージをインストールします..."
        pip3 install playwright pandas openpyxl
        echo ""
        echo "Playwrightブラウザをインストールします..."
        playwright install chromium
        echo ""
        echo "✅ インストール完了"
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
echo "========================================="
echo "完了"
echo "========================================="
