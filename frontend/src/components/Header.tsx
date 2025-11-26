/**
 * Header Component
 */
import { Search } from 'lucide-react';

export function Header() {
  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-500 p-2 rounded-lg">
              <Search className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">求人スクレイピングシステム</h1>
              <p className="text-sm text-gray-500 mt-1">React + TypeScript版</p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="text-right">
              <div className="text-sm text-gray-500">高速・並列処理対応</div>
              <div className="text-xs text-gray-400">複数サイト同時スクレイピング</div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
