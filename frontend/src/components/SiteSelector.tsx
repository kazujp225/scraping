/**
 * Site Selector Component
 */
import { useScraperStore } from '@/stores/scraper';
import { Check } from 'lucide-react';

export function SiteSelector() {
  const { sites, setSites } = useScraperStore();

  const toggleSite = (siteId: string) => {
    setSites(
      sites.map((site) =>
        site.id === siteId ? { ...site, enabled: !site.enabled } : site
      )
    );
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {sites.map((site) => (
        <button
          key={site.id}
          onClick={() => toggleSite(site.id)}
          className={`
            relative p-4 rounded-lg border-2 transition-all
            ${
              site.enabled
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-200 bg-white hover:border-gray-300'
            }
          `}
        >
          <div className="flex items-start justify-between">
            <div className="text-left flex-1">
              <div className="text-lg font-semibold text-gray-900">{site.icon} {site.name}</div>
              <div className="text-xs text-gray-500 mt-1">{site.description}</div>
            </div>

            {site.enabled && (
              <div className="ml-2">
                <div className="bg-primary-500 rounded-full p-1">
                  <Check className="h-4 w-4 text-white" />
                </div>
              </div>
            )}
          </div>
        </button>
      ))}
    </div>
  );
}
