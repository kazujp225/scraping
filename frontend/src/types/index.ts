/**
 * Type Definitions for Job Scraper
 */

export interface JobData {
  番号: number;
  タイトル: string;
  会社名: string;
  場所: string;
  給与: string;
  URL?: string;
  雇用形態?: string;
  仕事内容?: string;
}

export interface ScrapeConfig {
  site: SiteName;
  keyword: string;
  location: string;
  maxPages: number;
}

export type SiteName =
  | 'indeed'
  | 'yahoo'
  | 'townwork'
  | 'baitoru'
  | 'hellowork'
  | 'mahhabaito'
  | 'linebaito'
  | 'rikunavi'
  | 'mynavi'
  | 'entenshoku'
  | 'kaigojob'
  | 'jobmedley';

export interface SiteInfo {
  id: SiteName;
  name: string;
  description: string;
  enabled: boolean;
  icon: string;
}

export interface ScrapeProgress {
  site: SiteName;
  status: 'pending' | 'running' | 'completed' | 'error';
  currentPage: number;
  totalPages: number;
  itemsCollected: number;
  message?: string;
  error?: string;
}

export interface ScrapeResult {
  site: SiteName;
  jobs: JobData[];
  totalItems: number;
  duration: number;
  timestamp: string;
  success: boolean;
  error?: string;
}

export interface ScrapeSession {
  id: string;
  config: ScrapeConfig[];
  progress: ScrapeProgress[];
  results: ScrapeResult[];
  startTime: string;
  endTime?: string;
  status: 'running' | 'completed' | 'cancelled';
}
