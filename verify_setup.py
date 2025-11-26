"""
セットアップ検証スクリプト
環境が正しく構築されているかチェック
"""
import sys


def check_python_version():
    """Python バージョンチェック"""
    print("=" * 60)
    print("Python バージョンチェック")
    print("=" * 60)

    version = sys.version_info
    print(f"現在のバージョン: Python {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 8:
        print("✅ Python 3.8以上が必要です - OK\n")
        return True
    else:
        print("❌ Python 3.8以上が必要です\n")
        return False


def check_packages():
    """必須パッケージのチェック"""
    print("=" * 60)
    print("パッケージチェック")
    print("=" * 60 + "\n")

    packages = {
        "playwright": "ブラウザ自動化",
        "pandas": "データ処理",
        "openpyxl": "Excel出力"
    }

    all_ok = True
    results = []

    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✅ {package:20} - OK ({description})")
            results.append((package, True, None))
        except ImportError as e:
            print(f"❌ {package:20} - 未インストール ({description})")
            results.append((package, False, description))
            all_ok = False

    print()
    return all_ok, results


def check_playwright_browsers():
    """Playwright ブラウザのチェック"""
    print("=" * 60)
    print("Playwright ブラウザチェック")
    print("=" * 60 + "\n")

    try:
        from playwright.sync_api import sync_playwright

        print("Playwright インポート: ✅")
        print("\nブラウザの確認中...")
        print("※ ブラウザが未インストールの場合、エラーが表示されます")
        print()

        try:
            with sync_playwright() as p:
                # Chromium の確認
                try:
                    browser = p.chromium.launch(headless=True)
                    browser.close()
                    print("✅ Chromium ブラウザ - インストール済み")
                    return True
                except Exception as e:
                    print(f"❌ Chromium ブラウザ - 未インストール")
                    print(f"   エラー: {str(e)[:100]}")
                    return False
        except Exception as e:
            print(f"❌ ブラウザチェック失敗: {e}")
            return False

    except ImportError:
        print("❌ Playwright が未インストール")
        return False


def print_installation_guide(missing_packages):
    """インストールガイドを表示"""
    print("\n" + "=" * 60)
    print("インストール手順")
    print("=" * 60 + "\n")

    if missing_packages:
        print("以下のコマンドでパッケージをインストールしてください:\n")

        # 最小限のパッケージ
        print("【最小限のパッケージ】")
        print("pip3 install playwright pandas openpyxl\n")

        # Playwrightブラウザ
        print("【Playwrightブラウザ】")
        print("playwright install chromium\n")

        # または requirements.txt から
        print("【または requirements.txt から一括インストール】")
        print("pip3 install -r requirements.txt")
        print("playwright install chromium\n")

    print("=" * 60 + "\n")


def main():
    """メイン処理"""
    print("\n" + "=" * 60)
    print("求人スクレイピングシステム - セットアップ検証")
    print("=" * 60 + "\n")

    # Python バージョンチェック
    python_ok = check_python_version()

    # パッケージチェック
    packages_ok, package_results = check_packages()

    # Playwright ブラウザチェック
    browser_ok = check_playwright_browsers()

    # 結果サマリー
    print("\n" + "=" * 60)
    print("検証結果サマリー")
    print("=" * 60 + "\n")

    print(f"Python バージョン: {'✅ OK' if python_ok else '❌ NG'}")
    print(f"必須パッケージ:     {'✅ OK' if packages_ok else '❌ NG'}")
    print(f"Playwright ブラウザ: {'✅ OK' if browser_ok else '❌ NG'}")

    if python_ok and packages_ok and browser_ok:
        print("\n🎉 すべての検証に合格しました！")
        print("\n次のステップ:")
        print("  1. 動作確認: python3 minimal_test.py")
        print("  2. スクレイピング実行: python3 simple_scraper.py")
        print("  3. またはメニューから: bash run.sh")
        print("\n詳細は START_HERE.md を参照してください")
    else:
        print("\n⚠️  いくつかの問題が見つかりました")

        # 不足パッケージの収集
        missing = [pkg for pkg, ok, desc in package_results if not ok]

        if not packages_ok or not browser_ok:
            print_installation_guide(missing)

        if not python_ok:
            print("Python 3.8以上をインストールしてください")
            print("https://www.python.org/downloads/")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
