"""
JSONデータをExcelに変換
"""
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import glob


def convert_json_to_excel():
    """JSONファイルをExcelに変換"""
    print("\n" + "="*60)
    print("JSON → Excel 変換ツール")
    print("="*60 + "\n")

    # JSONファイルを探す
    json_files = glob.glob("*_jobs_*.json")

    if not json_files:
        print("❌ JSONファイルが見つかりません")
        print("\n先に simple_scraper.py を実行してデータを取得してください")
        return

    print("見つかったJSONファイル:")
    for i, file in enumerate(json_files, 1):
        size = Path(file).stat().st_size
        print(f"{i}. {file} ({size} bytes)")

    if len(json_files) == 1:
        selected_file = json_files[0]
        print(f"\n自動選択: {selected_file}")
    else:
        print("\n変換するファイルの番号を入力してください")
        choice = input(f"選択 (1-{len(json_files)}): ").strip()

        try:
            index = int(choice) - 1
            if 0 <= index < len(json_files):
                selected_file = json_files[index]
            else:
                print("無効な番号です")
                return
        except ValueError:
            print("無効な入力です")
            return

    print(f"\n処理中: {selected_file}")

    try:
        # JSONファイル読み込み
        with open(selected_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✅ データ読み込み完了: {len(data)} 件")

        if not data:
            print("❌ データが空です")
            return

        # DataFrameに変換
        df = pd.DataFrame(data)

        # 出力ファイル名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_file = f"求人データ_{timestamp}.xlsx"

        # Excel保存
        df.to_excel(excel_file, index=False, engine='openpyxl')

        print(f"\n✅ Excel保存完了: {excel_file}")
        print(f"📊 行数: {len(df)}")
        print(f"📋 列数: {len(df.columns)}")
        print(f"\n列名:")
        for col in df.columns:
            print(f"  - {col}")

        print(f"\nデータプレビュー:")
        print(df.head(3).to_string())

        print(f"\n💡 ファイルを開くには:")
        print(f"   open {excel_file}")

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")


def main():
    convert_json_to_excel()


if __name__ == "__main__":
    main()
