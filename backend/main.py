"""
FastAPI Backend for Job Scraper
"""
import asyncio
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import sys
import os

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# スクレイパーのインポート
from scraper_real import scrape_indeed_real, scrape_yahoo_real, scrape_townwork_real
from scraper_simple import scrape_indeed_demo, scrape_yahoo_demo, scrape_townwork_demo

# デモモードフラグ（環境変数で制御可能）
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

logger.info("=" * 60)
logger.info("Job Scraper API Starting...")
logger.info(f"Mode: {'DEMO' if DEMO_MODE else 'REAL SCRAPING'}")
logger.info("=" * 60)

app = FastAPI(title="Job Scraper API", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データモデル
class ScrapeConfig(BaseModel):
    site: str
    keyword: str
    location: str
    maxPages: int = 5

class ScrapeRequest(BaseModel):
    configs: List[ScrapeConfig]

# セッション管理
sessions: Dict[str, Dict] = {}
websocket_connections: Dict[str, WebSocket] = {}

# サイト情報
SITES = [
    {"id": "townwork", "name": "タウンワーク", "description": "地域密着型求人", "enabled": True, "icon": "🏪"},
]

@app.get("/api/sites")
async def get_sites():
    """サイト一覧を取得"""
    logger.info("📋 サイト一覧を取得")
    return SITES

@app.post("/api/scrape/start")
async def start_scraping(request: ScrapeRequest):
    """スクレイピング開始"""
    session_id = str(uuid.uuid4())

    logger.info("=" * 60)
    logger.info(f"🚀 スクレイピング開始 - Session: {session_id}")
    logger.info(f"   サイト数: {len(request.configs)}")
    for config in request.configs:
        logger.info(f"   - {config.site}: キーワード={config.keyword}, 地域={config.location}, ページ数={config.maxPages}")
    logger.info("=" * 60)

    sessions[session_id] = {
        "configs": [c.model_dump() for c in request.configs],
        "results": [],
        "status": "running",
        "startTime": datetime.now().isoformat(),
    }

    # バックグラウンドでスクレイピング実行
    asyncio.create_task(run_scraping(session_id, request.configs))

    return {"sessionId": session_id}

async def run_scraping(session_id: str, configs: List[ScrapeConfig]):
    """スクレイピング実行"""
    logger.info(f"🔄 Session {session_id}: スクレイピング処理開始")
    try:
        results = []

        for idx, config in enumerate(configs, 1):
            logger.info(f"📍 [{idx}/{len(configs)}] {config.site} の処理開始...")
            # WebSocket経由で進捗を送信
            if session_id in websocket_connections:
                await websocket_connections[session_id].send_json({
                    "type": "progress",
                    "data": {
                        "site": config.site,
                        "status": "running",
                        "currentPage": 1,
                        "totalPages": config.maxPages,
                        "itemsCollected": 0,
                        "message": f"{config.site}でスクレイピング開始",
                    }
                })

            # スクレイピング実行
            jobs = []
            start_time = datetime.now()

            try:
                logger.info(f"   キーワード: {config.keyword}, 地域: {config.location}")
                logger.info(f"   モード: {'DEMO' if DEMO_MODE else 'REAL'}")

                if DEMO_MODE:
                    # デモモード（テスト用）
                    logger.info(f"   🎭 デモモードで実行中...")
                    if config.site == "townwork":
                        jobs = await scrape_townwork_demo(config.keyword, config.location)
                    else:
                        jobs = await scrape_townwork_demo(config.keyword, config.location)
                else:
                    # 実際のスクレイピング
                    logger.info(f"   🌐 実際のサイトにアクセス中...")
                    if config.site == "townwork":
                        jobs = await scrape_townwork_real(config.keyword, config.location, config.maxPages * 10)
                    else:
                        logger.warning(f"   ⚠️  {config.site} は未対応です（タウンワーク限定モード）")
                        jobs = []

                duration = (datetime.now() - start_time).total_seconds()

                result = {
                    "site": config.site,
                    "jobs": jobs,
                    "totalItems": len(jobs),
                    "duration": duration,
                    "timestamp": datetime.now().isoformat(),
                    "success": True,
                }

                results.append(result)

                logger.info(f"   ✅ {config.site} 完了: {len(jobs)}件取得 ({duration:.2f}秒)")

                # 完了通知
                if session_id in websocket_connections:
                    await websocket_connections[session_id].send_json({
                        "type": "progress",
                        "data": {
                            "site": config.site,
                            "status": "completed",
                            "currentPage": config.maxPages,
                            "totalPages": config.maxPages,
                            "itemsCollected": len(jobs),
                            "message": f"{len(jobs)}件取得完了",
                        }
                    })

            except Exception as e:
                # エラー通知
                logger.error(f"   ❌ {config.site} でエラー発生: {str(e)}")
                if session_id in websocket_connections:
                    await websocket_connections[session_id].send_json({
                        "type": "progress",
                        "data": {
                            "site": config.site,
                            "status": "error",
                            "currentPage": 0,
                            "totalPages": config.maxPages,
                            "itemsCollected": 0,
                            "error": str(e),
                        }
                    })

        # セッション更新
        sessions[session_id]["results"] = results
        sessions[session_id]["status"] = "completed"
        sessions[session_id]["endTime"] = datetime.now().isoformat()

        total_jobs = sum(r["totalItems"] for r in results)
        logger.info("=" * 60)
        logger.info(f"🎉 Session {session_id}: 全処理完了")
        logger.info(f"   合計取得件数: {total_jobs}件")
        logger.info("=" * 60)

        # 完了通知
        if session_id in websocket_connections:
            await websocket_connections[session_id].send_json({
                "type": "complete",
                "data": results,
            })

    except Exception as e:
        logger.error(f"❌ Session {session_id}: 致命的エラー発生: {str(e)}")
        sessions[session_id]["status"] = "error"
        sessions[session_id]["error"] = str(e)

        if session_id in websocket_connections:
            await websocket_connections[session_id].send_json({
                "type": "error",
                "error": str(e),
            })

@app.get("/api/scrape/status/{session_id}")
async def get_scrape_status(session_id: str):
    """スクレイピング状態取得"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return sessions[session_id].get("results", [])

@app.post("/api/scrape/stop/{session_id}")
async def stop_scraping(session_id: str):
    """スクレイピング停止"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    sessions[session_id]["status"] = "cancelled"
    return {"message": "Scraping stopped"}

@app.get("/api/export/{session_id}/{format}")
async def export_results(session_id: str, format: str):
    """結果のエクスポート"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    results = sessions[session_id].get("results", [])

    # 全データを結合
    all_jobs = []
    for result in results:
        all_jobs.extend(result["jobs"])

    if format == "json":
        # JSON出力
        output_path = Path(f"export_{session_id}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_jobs, f, ensure_ascii=False, indent=2)

        return FileResponse(
            output_path,
            media_type="application/json",
            filename=f"求人データ_{datetime.now().strftime('%Y%m%d')}.json"
        )

    elif format == "excel":
        # Excel出力
        import pandas as pd

        df = pd.DataFrame(all_jobs)
        output_path = Path(f"export_{session_id}.xlsx")
        df.to_excel(output_path, index=False, engine="openpyxl")

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=f"求人データ_{datetime.now().strftime('%Y%m%d')}.xlsx"
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid format")

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket接続"""
    await websocket.accept()
    websocket_connections[session_id] = websocket

    try:
        while True:
            # クライアントからのメッセージを待つ
            data = await websocket.receive_text()

    except WebSocketDisconnect:
        if session_id in websocket_connections:
            del websocket_connections[session_id]

@app.get("/")
async def root():
    """ルート"""
    return {
        "message": "Job Scraper API",
        "version": "1.0.0",
        "mode": "DEMO" if DEMO_MODE else "REAL",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
