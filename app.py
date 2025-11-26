"""
求人サイトスクレイピングGUIシステム
Streamlit ベース
"""
import streamlit as st
import asyncio
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sys
import logging

# スクレイパーのインポート（タウンワーク限定）
from scrapers.townwork import TownworkScraper

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ページ設定
st.set_page_config(
    page_title="求人スクレイピングシステム",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# スタイル設定
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)


def load_config():
    """セレクタ設定を読み込み"""
    config_path = Path("config/selectors.json")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_config(config):
    """セレクタ設定を保存"""
    config_path = Path("config/selectors.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def get_scraper(site_name: str):
    """サイト名からスクレイパーインスタンスを取得"""
    # タウンワーク以外は無効化
    scrapers = {
        "townwork": TownworkScraper,
    }
    scraper_class = scrapers.get(site_name)
    if scraper_class:
        return scraper_class()
    return None


def main():
    """メインアプリケーション"""

    # ヘッダー
    st.markdown('<p class="main-header">🔍 求人サイト スクレイピングシステム</p>', unsafe_allow_html=True)
    st.markdown("---")

    # サイドバー
    with st.sidebar:
        st.header("⚙️ 設定")

        # タブ選択
        page = st.radio(
            "メニュー",
            ["🚀 スクレイピング実行", "🛠️ サイト管理", "📊 データ確認"],
            label_visibility="collapsed"
        )

    # 設定読み込み
    config = load_config()

    # ===== スクレイピング実行タブ =====
    if page == "🚀 スクレイピング実行":
        st.header("🚀 スクレイピング実行")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("対象サイト選択")

            # タウンワークのみ選択可能
            available_sites = {
                "townwork": "タウンワーク",
            }

            selected_sites = []
            for site_key, site_name in available_sites.items():
                # タウンワークをデフォルト選択
                if st.checkbox(site_name, key=f"site_{site_key}", value=True):
                    selected_sites.append(site_key)

        with col2:
            st.subheader("検索条件")

            # キーワード入力
            keywords_input = st.text_area(
                "検索キーワード（1行1キーワード）",
                value="IT\n営業\n飲食",
                height=100
            )
            keywords = [k.strip() for k in keywords_input.split('\n') if k.strip()]

            # 地域入力
            areas_input = st.text_area(
                "地域（1行1地域）",
                value="東京\n大阪",
                height=80
            )
            areas = [a.strip() for a in areas_input.split('\n') if a.strip()]

            # ページ数
            max_pages = st.slider("最大ページ数", min_value=1, max_value=20, value=5)

            # 並列数
            parallel = st.select_slider(
                "並列実行数",
                options=[1, 5, 10, 20, 50],
                value=10
            )

        # 絞り込み
        with st.expander("🔎 絞り込み（タウンワーク）", expanded=False):
            colf1, colf2, colf3 = st.columns(3)

            with colf1:
                employment_types = st.multiselect(
                    "雇用形態",
                    options=["アルバイト", "パート", "正社員"],
                    default=["アルバイト", "パート", "正社員"],
                )

            with colf2:
                salary_min = st.number_input(
                    "最低給与（円/時）",
                    min_value=0,
                    max_value=10000,
                    value=0,
                    step=50,
                )

            with colf3:
                shifts = st.multiselect(
                    "シフト",
                    options=["日勤", "夜勤"],
                    default=[],
                )

            # フィルタ辞書を組み立て
            filters = {}
            if employment_types:
                filters["employment_type"] = employment_types
            if salary_min and salary_min > 0:
                filters["salary_min"] = int(salary_min)
            if shifts:
                filters["shift"] = shifts

        st.markdown("---")

        # 実行設定サマリー
        st.subheader("📋 実行サマリー")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("対象サイト数", len(selected_sites))
        with col2:
            st.metric("キーワード数", len(keywords))
        with col3:
            st.metric("地域数", len(areas))
        with col4:
            total_tasks = len(selected_sites) * len(keywords) * len(areas)
            st.metric("総タスク数", total_tasks)

        st.markdown("---")

        # 実行ボタン
        if st.button("🚀 スクレイピング開始", type="primary", use_container_width=True):
            if not selected_sites:
                st.error("❌ 少なくとも1つのサイトを選択してください")
            elif not keywords:
                st.error("❌ 検索キーワードを入力してください")
            elif not areas:
                st.error("❌ 地域を入力してください")
            else:
                run_scraping(selected_sites, keywords, areas, max_pages, parallel, filters)

    # ===== サイト管理タブ =====
    elif page == "🛠️ サイト管理":
        st.header("🛠️ サイト管理")

        st.info("💡 各サイトのセレクタ設定を管理します。サイトのHTML構造が変わった場合、ここで更新できます。")

        # サイト選択
        # 管理対象サイトをタウンワークに限定
        site_keys = [k for k in config.keys() if k == "townwork"]
        if site_keys:
            selected_site = st.selectbox("サイト選択", site_keys)

            if selected_site:
                st.subheader(f"📝 {config[selected_site].get('name', selected_site)} の設定")

                # 基本情報
                with st.expander("基本情報", expanded=True):
                    site_name = st.text_input("サイト名", value=config[selected_site].get('name', ''))
                    base_url = st.text_input("ベースURL", value=config[selected_site].get('base_url', ''))
                    search_url = st.text_area(
                        "検索URLパターン",
                        value=config[selected_site].get('search_url_pattern', ''),
                        height=80
                    )

                # セレクタ設定
                with st.expander("セレクタ設定", expanded=True):
                    st.markdown("#### 一覧ページ用セレクタ")
                    selectors = config[selected_site].get('selectors', {})

                    col1, col2 = st.columns(2)

                    with col1:
                        selectors['job_cards'] = st.text_input(
                            "求人カード",
                            value=selectors.get('job_cards', '')
                        )
                        selectors['title'] = st.text_input(
                            "タイトル",
                            value=selectors.get('title', '')
                        )
                        selectors['company'] = st.text_input(
                            "会社名",
                            value=selectors.get('company', '')
                        )
                        selectors['location'] = st.text_input(
                            "勤務地",
                            value=selectors.get('location', '')
                        )

                    with col2:
                        selectors['salary'] = st.text_input(
                            "給与",
                            value=selectors.get('salary', '')
                        )
                        selectors['employment_type'] = st.text_input(
                            "雇用形態",
                            value=selectors.get('employment_type', '')
                        )
                        selectors['detail_link'] = st.text_input(
                            "詳細リンク",
                            value=selectors.get('detail_link', '')
                        )

                # 保存ボタン
                if st.button("💾 設定を保存", type="primary"):
                    config[selected_site]['name'] = site_name
                    config[selected_site]['base_url'] = base_url
                    config[selected_site]['search_url_pattern'] = search_url
                    config[selected_site]['selectors'] = selectors

                    save_config(config)
                    st.success("✅ 設定を保存しました")

                # セレクタテスト機能
                st.markdown("---")
                st.subheader("🧪 セレクタテスト")
                test_url = st.text_input("テストURL")
                if st.button("テスト実行") and test_url:
                    st.info("テスト機能は実装中です...")

    # ===== データ確認タブ =====
    elif page == "📊 データ確認":
        st.header("📊 取得データ確認")

        # 保存済みデータの一覧
        output_dir = Path("data/output")
        if output_dir.exists():
            csv_files = list(output_dir.glob("*.csv"))
            excel_files = list(output_dir.glob("*.xlsx"))

            all_files = csv_files + excel_files

            if all_files:
                st.subheader("📁 保存済みファイル")

                file_names = [f.name for f in all_files]
                selected_file = st.selectbox("ファイル選択", file_names)

                if selected_file:
                    file_path = output_dir / selected_file

                    try:
                        if selected_file.endswith('.csv'):
                            df = pd.read_csv(file_path)
                        else:
                            df = pd.read_excel(file_path)

                        st.success(f"✅ 読み込み成功: {len(df)} 件のデータ")

                        # データプレビュー
                        st.dataframe(df, use_container_width=True)

                        # 統計情報
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("総レコード数", len(df))
                        with col2:
                            if 'site' in df.columns:
                                st.metric("サイト数", df['site'].nunique())
                        with col3:
                            if 'company' in df.columns:
                                st.metric("企業数", df['company'].nunique())

                    except Exception as e:
                        st.error(f"❌ ファイル読み込みエラー: {e}")
            else:
                st.info("💡 まだデータが保存されていません。スクレイピングを実行してください。")
        else:
            st.info("💡 出力フォルダが存在しません。")


def run_scraping(selected_sites, keywords, areas, max_pages, parallel, filters):
    """スクレイピング実行"""

    st.subheader("🔄 実行中...")

    # 進捗バー
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_container = st.container()

    all_results = []
    total_sites = len(selected_sites)

    try:
        for idx, site_key in enumerate(selected_sites):
            status_text.text(f"📡 {site_key} を処理中... ({idx + 1}/{total_sites})")

            scraper = get_scraper(site_key)
            if not scraper:
                with log_container:
                    st.warning(f"⚠️ {site_key} のスクレイパーが見つかりません")
                continue

            # 非同期実行
            with log_container:
                st.info(f"🚀 {site_key} スクレイピング開始")

            try:
                results = asyncio.run(
                    scraper.scrape(keywords, areas, max_pages, parallel, filters=filters)
                )

                all_results.extend(results)

                with log_container:
                    st.success(f"✅ {site_key} 完了: {len(results)} 件取得")

            except Exception as e:
                with log_container:
                    st.error(f"❌ {site_key} エラー: {str(e)}")
                logger.error(f"Scraping error for {site_key}: {e}", exc_info=True)

            # 進捗更新
            progress_bar.progress((idx + 1) / total_sites)

        # 結果をDataFrameに変換
        if all_results:
            df = pd.DataFrame(all_results)

            st.markdown("---")
            st.subheader("📊 取得結果")

            # 統計情報
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("総取得件数", len(df))
            with col2:
                st.metric("サイト数", df['site'].nunique() if 'site' in df.columns else 0)
            with col3:
                st.metric("企業数", df['company'].nunique() if 'company' in df.columns else 0)

            # データプレビュー
            st.dataframe(df.head(50), use_container_width=True)

            # エクスポート
            st.subheader("💾 エクスポート")
            col1, col2 = st.columns(2)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            with col1:
                csv_data = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 CSV でダウンロード",
                    data=csv_data,
                    file_name=f"scraping_results_{timestamp}.csv",
                    mime="text/csv"
                )

            with col2:
                # Excel保存
                output_path = Path("data/output") / f"scraping_results_{timestamp}.xlsx"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                df.to_excel(output_path, index=False, engine='openpyxl')
                st.success(f"✅ Excel保存: {output_path.name}")

            st.success("🎉 スクレイピング完了！")

        else:
            st.warning("⚠️ データが取得できませんでした")

    except Exception as e:
        st.error(f"❌ エラーが発生しました: {str(e)}")
        logger.error(f"Scraping execution error: {e}", exc_info=True)
    finally:
        progress_bar.progress(100)
        status_text.text("✅ 完了")


if __name__ == "__main__":
    main()
