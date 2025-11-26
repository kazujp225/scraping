/**
 * Scraper State Management (Zustand)
 */
import { create } from 'zustand';
import type { ScrapeConfig, ScrapeProgress, ScrapeResult, SiteInfo } from '@/types';

interface ScraperState {
  // Sites
  sites: SiteInfo[];
  setSites: (sites: SiteInfo[]) => void;

  // Configuration
  configs: ScrapeConfig[];
  addConfig: (config: ScrapeConfig) => void;
  removeConfig: (index: number) => void;
  clearConfigs: () => void;

  // Session
  sessionId: string | null;
  setSessionId: (id: string | null) => void;

  // Progress
  progress: ScrapeProgress[];
  setProgress: (progress: ScrapeProgress[]) => void;
  updateProgress: (siteProgress: ScrapeProgress) => void;

  // Results
  results: ScrapeResult[];
  setResults: (results: ScrapeResult[]) => void;

  // Status
  isRunning: boolean;
  setIsRunning: (running: boolean) => void;
}

export const useScraperStore = create<ScraperState>((set) => ({
  // Sites
  sites: [],
  setSites: (sites) => set({ sites }),

  // Configuration
  configs: [],
  addConfig: (config) =>
    set((state) => ({
      configs: [...state.configs, config],
    })),
  removeConfig: (index) =>
    set((state) => ({
      configs: state.configs.filter((_, i) => i !== index),
    })),
  clearConfigs: () => set({ configs: [] }),

  // Session
  sessionId: null,
  setSessionId: (id) => set({ sessionId: id }),

  // Progress
  progress: [],
  setProgress: (progress) => set({ progress }),
  updateProgress: (siteProgress) =>
    set((state) => {
      const existingIndex = state.progress.findIndex((p) => p.site === siteProgress.site);

      if (existingIndex >= 0) {
        const newProgress = [...state.progress];
        newProgress[existingIndex] = siteProgress;
        return { progress: newProgress };
      } else {
        return { progress: [...state.progress, siteProgress] };
      }
    }),

  // Results
  results: [],
  setResults: (results) => set({ results }),

  // Status
  isRunning: false,
  setIsRunning: (running) => set({ isRunning: running }),
}));
