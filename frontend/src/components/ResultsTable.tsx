/**
 * Results Table Component
 */
import { useState } from 'react';
import { useScraperStore } from '@/stores/scraper';
import { api } from '@/services/api';
import { Download, FileJson, FileSpreadsheet } from 'lucide-react';
import type { JobData } from '@/types';

export function ResultsTable() {
  const { results, sessionId } = useScraperStore();
  const [downloading, setDownloading] = useState(false);

  // 全データを結合
  const allJobs: JobData[] = results.flatMap((r) => r.jobs);

  const handleExport = async (format: 'json' | 'excel') => {
    if (!sessionId) return;

    try {
      setDownloading(true);
      const blob = await api.exportResults(sessionId, format);

      // ダウンロード
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `求人データ_${new Date().toISOString().split('T')[0]}.${
        format === 'json' ? 'json' : 'xlsx'
      }`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Export failed:', error);
      alert('エクスポートに失敗しました');
    } finally {
      setDownloading(false);
    }
  };

  if (allJobs.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        データがまだありません。スクレイピングを実行してください。
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* サマリー */}
      <div className="flex items-center justify-between">
        <div>
          <div className="text-2xl font-bold text-gray-900">{allJobs.length} 件</div>
          <div className="text-sm text-gray-500">{results.length} サイトから取得</div>
        </div>

        {/* エクスポートボタン */}
        <div className="flex space-x-2">
          <button
            onClick={() => handleExport('json')}
            disabled={downloading}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg flex items-center space-x-2"
          >
            <FileJson className="h-4 w-4" />
            <span>JSON</span>
          </button>

          <button
            onClick={() => handleExport('excel')}
            disabled={downloading}
            className="px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg flex items-center space-x-2"
          >
            <FileSpreadsheet className="h-4 w-4" />
            <span>Excel</span>
          </button>
        </div>
      </div>

      {/* テーブル */}
      <div className="overflow-x-auto border border-gray-200 rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                No
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                タイトル
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                会社名
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                場所
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                給与
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {allJobs.map((job, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {index + 1}
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  <div className="max-w-md truncate">{job.タイトル}</div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  {job.会社名}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {job.場所}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {job.給与}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
