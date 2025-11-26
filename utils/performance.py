"""
パフォーマンス測定とベンチマーク
"""
import time
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """パフォーマンス指標"""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration: float = 0.0
    items_processed: int = 0
    items_per_second: float = 0.0
    errors: int = 0
    retries: int = 0
    total_bytes: int = 0

    def finish(self):
        """測定を終了"""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        if self.duration > 0:
            self.items_per_second = self.items_processed / self.duration

    def to_dict(self) -> Dict:
        """辞書に変換"""
        return {
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time).isoformat() if self.end_time else None,
            "duration_seconds": round(self.duration, 2),
            "items_processed": self.items_processed,
            "items_per_second": round(self.items_per_second, 2),
            "errors": self.errors,
            "retries": self.retries,
            "total_bytes": self.total_bytes,
        }

    def __str__(self):
        return (
            f"Duration: {self.duration:.2f}s, "
            f"Items: {self.items_processed}, "
            f"Speed: {self.items_per_second:.2f} items/s, "
            f"Errors: {self.errors}"
        )


class PerformanceMonitor:
    """パフォーマンスモニター"""

    def __init__(self, name: str = "default"):
        self.name = name
        self.metrics = PerformanceMetrics()
        self.checkpoints: Dict[str, float] = {}
        self.checkpoint_durations: Dict[str, List[float]] = {}

    def start(self):
        """測定開始"""
        self.metrics = PerformanceMetrics()
        logger.info(f"Performance monitoring started: {self.name}")

    def checkpoint(self, name: str):
        """チェックポイントを記録"""
        current_time = time.time()
        self.checkpoints[name] = current_time

        # 前回のチェックポイントからの経過時間を計算
        if len(self.checkpoints) > 1:
            previous_time = list(self.checkpoints.values())[-2]
            duration = current_time - previous_time

            if name not in self.checkpoint_durations:
                self.checkpoint_durations[name] = []
            self.checkpoint_durations[name].append(duration)

    def record_item(self, count: int = 1):
        """アイテム処理数を記録"""
        self.metrics.items_processed += count

    def record_error(self):
        """エラーを記録"""
        self.metrics.errors += 1

    def record_retry(self):
        """リトライを記録"""
        self.metrics.retries += 1

    def record_bytes(self, bytes_count: int):
        """バイト数を記録"""
        self.metrics.total_bytes += bytes_count

    def finish(self) -> PerformanceMetrics:
        """測定終了"""
        self.metrics.finish()
        logger.info(f"Performance monitoring finished: {self.name} - {self.metrics}")
        return self.metrics

    def get_checkpoint_stats(self) -> Dict[str, Dict]:
        """チェックポイント統計を取得"""
        stats = {}
        for name, durations in self.checkpoint_durations.items():
            if durations:
                stats[name] = {
                    "count": len(durations),
                    "avg_duration": sum(durations) / len(durations),
                    "min_duration": min(durations),
                    "max_duration": max(durations),
                    "total_duration": sum(durations)
                }
        return stats

    def print_summary(self):
        """サマリーを表示"""
        print(f"\n=== Performance Summary: {self.name} ===")
        print(f"Duration: {self.metrics.duration:.2f}s")
        print(f"Items Processed: {self.metrics.items_processed}")
        print(f"Speed: {self.metrics.items_per_second:.2f} items/s")
        print(f"Errors: {self.metrics.errors}")
        print(f"Retries: {self.metrics.retries}")

        if self.metrics.total_bytes > 0:
            mb = self.metrics.total_bytes / (1024 * 1024)
            print(f"Total Data: {mb:.2f} MB")

        if self.checkpoint_durations:
            print("\nCheckpoint Statistics:")
            for name, stats in self.get_checkpoint_stats().items():
                print(f"  {name}:")
                print(f"    Count: {stats['count']}")
                print(f"    Avg: {stats['avg_duration']:.3f}s")
                print(f"    Min: {stats['min_duration']:.3f}s")
                print(f"    Max: {stats['max_duration']:.3f}s")


class Benchmark:
    """ベンチマーク実行"""

    @staticmethod
    async def run_async(func, *args, iterations: int = 1, warmup: int = 0, **kwargs):
        """
        非同期関数のベンチマーク実行

        Args:
            func: 測定する関数
            iterations: 実行回数
            warmup: ウォームアップ回数
            *args, **kwargs: 関数の引数
        """
        # ウォームアップ
        for _ in range(warmup):
            await func(*args, **kwargs)

        # 測定
        results = []
        for i in range(iterations):
            start = time.time()
            await func(*args, **kwargs)
            duration = time.time() - start
            results.append(duration)
            logger.info(f"Iteration {i+1}/{iterations}: {duration:.3f}s")

        # 統計
        avg = sum(results) / len(results)
        min_time = min(results)
        max_time = max(results)

        print(f"\n=== Benchmark Results ===")
        print(f"Iterations: {iterations}")
        print(f"Average: {avg:.3f}s")
        print(f"Min: {min_time:.3f}s")
        print(f"Max: {max_time:.3f}s")
        print(f"Total: {sum(results):.3f}s")

        return {
            "iterations": iterations,
            "average": avg,
            "min": min_time,
            "max": max_time,
            "total": sum(results),
            "results": results
        }

    @staticmethod
    def run(func, *args, iterations: int = 1, warmup: int = 0, **kwargs):
        """
        同期関数のベンチマーク実行

        Args:
            func: 測定する関数
            iterations: 実行回数
            warmup: ウォームアップ回数
            *args, **kwargs: 関数の引数
        """
        # ウォームアップ
        for _ in range(warmup):
            func(*args, **kwargs)

        # 測定
        results = []
        for i in range(iterations):
            start = time.time()
            func(*args, **kwargs)
            duration = time.time() - start
            results.append(duration)
            logger.info(f"Iteration {i+1}/{iterations}: {duration:.3f}s")

        # 統計
        avg = sum(results) / len(results)
        min_time = min(results)
        max_time = max(results)

        print(f"\n=== Benchmark Results ===")
        print(f"Iterations: {iterations}")
        print(f"Average: {avg:.3f}s")
        print(f"Min: {min_time:.3f}s")
        print(f"Max: {max_time:.3f}s")
        print(f"Total: {sum(results):.3f}s")

        return {
            "iterations": iterations,
            "average": avg,
            "min": min_time,
            "max": max_time,
            "total": sum(results),
            "results": results
        }
