/**
 * Progress View Component
 */
import { useScraperStore } from '@/stores/scraper';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';

export function ProgressView() {
  const { progress } = useScraperStore();

  // 配列であることを保証
  const progressArray = Array.isArray(progress) ? progress : [];

  if (progressArray.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        進捗情報を待機中...
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {progressArray.map((item) => (
        <div key={item.site} className="border border-gray-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center space-x-3">
              {/* ステータスアイコン */}
              {item.status === 'running' && (
                <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
              )}
              {item.status === 'completed' && (
                <CheckCircle className="h-5 w-5 text-green-500" />
              )}
              {item.status === 'error' && (
                <XCircle className="h-5 w-5 text-red-500" />
              )}

              <div>
                <div className="font-semibold text-gray-900">{item.site}</div>
                {item.message && (
                  <div className="text-sm text-gray-500">{item.message}</div>
                )}
              </div>
            </div>

            <div className="text-right">
              <div className="text-sm font-medium text-gray-900">
                {item.itemsCollected} 件取得
              </div>
              <div className="text-xs text-gray-500">
                {item.currentPage} / {item.totalPages} ページ
              </div>
            </div>
          </div>

          {/* プログレスバー */}
          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
            <div
              className={`h-2 rounded-full transition-all ${
                item.status === 'completed'
                  ? 'bg-green-500'
                  : item.status === 'error'
                  ? 'bg-red-500'
                  : 'bg-blue-500'
              }`}
              style={{
                width: `${Math.min((item.currentPage / item.totalPages) * 100, 100)}%`,
              }}
            />
          </div>

          {/* エラーメッセージ */}
          {item.error && (
            <div className="mt-2 text-sm text-red-600 bg-red-50 p-2 rounded">
              {item.error}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
