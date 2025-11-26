#!/bin/bash

echo "========================================="
echo "求人スクレイピングシステム セットアップ"
echo "========================================="
echo ""

# Python バージョン確認
echo "1. Python バージョン確認..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 がインストールされていません"
    exit 1
fi

echo "✅ Python 確認完了"
echo ""

# 仮想環境の作成（推奨）
echo "2. 仮想環境を作成しますか？ (y/n)"
read -p "> " create_venv

if [ "$create_venv" = "y" ]; then
    echo "仮想環境を作成中..."
    python3 -m venv venv

    echo "仮想環境を有効化中..."
    source venv/bin/activate

    echo "✅ 仮想環境作成完了"
else
    echo "⏭️  仮想環境作成をスキップ"
fi

echo ""

# 依存パッケージのインストール
echo "3. 依存パッケージをインストール中..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ パッケージインストール失敗"
    exit 1
fi

echo "✅ パッケージインストール完了"
echo ""

# Playwright ブラウザのインストール
echo "4. Playwright ブラウザをインストール中..."
playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Playwrightインストール失敗"
    exit 1
fi

echo "✅ Playwright インストール完了"
echo ""

# 出力ディレクトリの作成
echo "5. 出力ディレクトリを作成中..."
mkdir -p data/output

echo "✅ ディレクトリ作成完了"
echo ""

echo "========================================="
echo "✅ セットアップ完了！"
echo "========================================="
echo ""
echo "起動方法:"
echo "  streamlit run app.py"
echo ""
echo "仮想環境を有効化した場合は、次回以降:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
