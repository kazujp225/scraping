"""
リトライ機能とエラーハンドリング
"""
import asyncio
import logging
from typing import TypeVar, Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar('T')


class RetryConfig:
    """リトライ設定"""

    def __init__(
        self,
        max_attempts: int = 3,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        exceptions: tuple = (Exception,)
    ):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.exceptions = exceptions


def async_retry(config: RetryConfig = None):
    """
    非同期関数用のリトライデコレータ

    使用例:
    @async_retry(RetryConfig(max_attempts=5))
    async def my_function():
        ...
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            delay = config.initial_delay

            for attempt in range(1, config.max_attempts + 1):
                try:
                    return await func(*args, **kwargs)

                except config.exceptions as e:
                    last_exception = e

                    if attempt == config.max_attempts:
                        logger.error(
                            f"{func.__name__} failed after {config.max_attempts} attempts: {e}"
                        )
                        raise

                    logger.warning(
                        f"{func.__name__} attempt {attempt}/{config.max_attempts} failed: {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )

                    await asyncio.sleep(delay)

                    # 指数バックオフ
                    delay = min(delay * config.exponential_base, config.max_delay)

            if last_exception:
                raise last_exception

        return wrapper
    return decorator


class ErrorCounter:
    """エラーカウンター（統計用）"""

    def __init__(self):
        self.total_attempts = 0
        self.successful = 0
        self.failed = 0
        self.retried = 0
        self.errors_by_type = {}

    def record_attempt(self):
        """試行を記録"""
        self.total_attempts += 1

    def record_success(self):
        """成功を記録"""
        self.successful += 1

    def record_failure(self, error: Exception):
        """失敗を記録"""
        self.failed += 1
        error_type = type(error).__name__
        self.errors_by_type[error_type] = self.errors_by_type.get(error_type, 0) + 1

    def record_retry(self):
        """リトライを記録"""
        self.retried += 1

    def get_stats(self) -> dict:
        """統計情報を取得"""
        return {
            "total_attempts": self.total_attempts,
            "successful": self.successful,
            "failed": self.failed,
            "retried": self.retried,
            "success_rate": self.successful / self.total_attempts if self.total_attempts > 0 else 0,
            "errors_by_type": self.errors_by_type
        }

    def __str__(self):
        stats = self.get_stats()
        return (
            f"Attempts: {stats['total_attempts']}, "
            f"Success: {stats['successful']}, "
            f"Failed: {stats['failed']}, "
            f"Retried: {stats['retried']}, "
            f"Success Rate: {stats['success_rate']:.1%}"
        )


# グローバルエラーカウンター
global_error_counter = ErrorCounter()
