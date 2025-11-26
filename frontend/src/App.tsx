/**
 * Main App Component
 */
import { useEffect, useState } from 'react';
import { Header } from '@/components/Header';
import { SiteSelector } from '@/components/SiteSelector';
import { ConfigForm } from '@/components/ConfigForm';
import { ProgressView } from '@/components/ProgressView';
import { ResultsTable } from '@/components/ResultsTable';
import { useScraperStore } from '@/stores/scraper';
import { api, ScraperWebSocket } from '@/services/api';

function App() {
  const [ws, setWs] = useState<ScraperWebSocket | null>(null);
  const { setSites, sessionId, setSessionId, setProgress, setResults, isRunning, setIsRunning } =
    useScraperStore();

  // サイト一覧を取得
  useEffect(() => {
    const loadSites = async () => {
      try {
        const sites = await api.getSites();
        setSites(sites);
      } catch (error) {
        console.error('Failed to load sites:', error);
      }
    };
    loadSites();
  }, [setSites]);

  // WebSocket接続管理
  useEffect(() => {
    if (sessionId && isRunning) {
      const websocket = new ScraperWebSocket(sessionId);

      websocket.connect(
        // onProgress
        (progress) => {
          setProgress(progress);
        },
        // onComplete
        () => {
          setIsRunning(false);
          // 結果を取得
          api.getScrapeStatus(sessionId).then((results) => {
            setResults(results);
          });
        },
        // onError
        (error) => {
          console.error('Scraping error:', error);
          setIsRunning(false);
        }
      );

      setWs(websocket);

      return () => {
        websocket.disconnect();
      };
    }
  }, [sessionId, isRunning, setProgress, setResults, setIsRunning]);

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* サイト選択 */}
          <section className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">対象サイト選択</h2>
            <SiteSelector />
          </section>

          {/* 検索条件設定 */}
          <section className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">検索条件</h2>
            <ConfigForm />
          </section>

          {/* 進捗表示 */}
          {isRunning && (
            <section className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">実行中...</h2>
              <ProgressView />
            </section>
          )}

          {/* 結果表示 */}
          <section className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">取得結果</h2>
            <ResultsTable />
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;
