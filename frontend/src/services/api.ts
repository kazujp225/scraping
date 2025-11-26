/**
 * API Service
 */
import axios from 'axios';
import type { ScrapeConfig, ScrapeResult, SiteInfo } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // サイト一覧取得
  async getSites(): Promise<SiteInfo[]> {
    const response = await apiClient.get<SiteInfo[]>('/api/sites');
    return response.data;
  },

  // スクレイピング開始
  async startScraping(configs: ScrapeConfig[]): Promise<{ sessionId: string }> {
    const response = await apiClient.post<{ sessionId: string }>('/api/scrape/start', {
      configs,
    });
    return response.data;
  },

  // スクレイピング状態取得
  async getScrapeStatus(sessionId: string): Promise<ScrapeResult[]> {
    const response = await apiClient.get<ScrapeResult[]>(`/api/scrape/status/${sessionId}`);
    return response.data;
  },

  // スクレイピング停止
  async stopScraping(sessionId: string): Promise<void> {
    await apiClient.post(`/api/scrape/stop/${sessionId}`);
  },

  // 結果のエクスポート
  async exportResults(sessionId: string, format: 'json' | 'excel'): Promise<Blob> {
    const response = await apiClient.get(`/api/export/${sessionId}/${format}`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // 過去の結果一覧
  async getHistory(): Promise<ScrapeResult[]> {
    const response = await apiClient.get<ScrapeResult[]>('/api/history');
    return response.data;
  },
};

// WebSocket接続
export class ScraperWebSocket {
  private ws: WebSocket | null = null;
  private sessionId: string;

  constructor(sessionId: string) {
    this.sessionId = sessionId;
  }

  connect(onProgress: (progress: any) => void, onComplete: () => void, onError: (error: string) => void) {
    const wsUrl = API_BASE_URL.replace('http', 'ws');
    this.ws = new WebSocket(`${wsUrl}/ws/${this.sessionId}`);

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'progress') {
        onProgress(data.data);
      } else if (data.type === 'complete') {
        onComplete();
      } else if (data.type === 'error') {
        onError(data.error);
      }
    };

    this.ws.onerror = () => {
      onError('WebSocket connection error');
    };

    this.ws.onclose = () => {
      console.log('WebSocket closed');
    };
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
