/**
 * Configuration Form Component
 */
import { useState } from 'react';
import { useScraperStore } from '@/stores/scraper';
import { api } from '@/services/api';
import { Play, Loader2 } from 'lucide-react';

export function ConfigForm() {
  const { sites, configs, addConfig, setSessionId, setIsRunning, isRunning } = useScraperStore();

  const [keyword, setKeyword] = useState('プログラマー');
  const [location, setLocation] = useState('東京');
  const [maxPages, setMaxPages] = useState(5);

  const enabledSites = sites.filter((s) => s.enabled);

  const handleStart = async () => {
    if (enabledSites.length === 0) {
      alert('サイトを選択してください');
      return;
    }

    if (!keyword.trim()) {
      alert('キーワードを入力してください');
      return;
    }

    try {
      setIsRunning(true);

      // 設定を作成
      const scrapeConfigs = enabledSites.map((site) => ({
        site: site.id,
        keyword,
        location,
        maxPages,
      }));

      // スクレイピング開始
      const { sessionId } = await api.startScraping(scrapeConfigs);
      setSessionId(sessionId);
    } catch (error) {
      console.error('Failed to start scraping:', error);
      setIsRunning(false);
      alert('スクレイピングの開始に失敗しました');
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* キーワード */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            キーワード
          </label>
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="例: プログラマー、営業"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={isRunning}
          />
        </div>

        {/* 地域 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            地域
          </label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="例: 東京、大阪"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={isRunning}
          />
        </div>

        {/* 最大ページ数 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            最大ページ数
          </label>
          <input
            type="number"
            value={maxPages}
            onChange={(e) => setMaxPages(Number(e.target.value))}
            min="1"
            max="50"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            disabled={isRunning}
          />
        </div>
      </div>

      {/* 実行ボタン */}
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-600">
          選択中のサイト: <span className="font-semibold">{enabledSites.length}個</span>
        </div>

        <button
          onClick={handleStart}
          disabled={isRunning || enabledSites.length === 0}
          className={`
            px-6 py-3 rounded-lg font-semibold flex items-center space-x-2
            ${
              isRunning || enabledSites.length === 0
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-primary-500 text-white hover:bg-primary-600'
            }
          `}
        >
          {isRunning ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              <span>実行中...</span>
            </>
          ) : (
            <>
              <Play className="h-5 w-5" />
              <span>スクレイピング開始</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
